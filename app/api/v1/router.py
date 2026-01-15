import os
import traceback
import shutil # Add this to imports at top
import pdfkit
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse
from app.services.scraper_service import scrape_job_text
from app.services.llm_service import generate_tailored_application

router = APIRouter()

def generate_resume_html(job_id, ai_data):
    if not ai_data: return ""
    
    personal = ai_data.get('personal_info', {})
    summary = ai_data.get('professional_summary', '')
    skills_list = ai_data.get('skills', [])
    skills = ", ".join(skills_list) if isinstance(skills_list, list) else str(skills_list)
    cover_letter = ai_data.get('cover_letter', '').replace('\n', '<br>')
    
    # HTML Builders
    def build_list(items):
        if not items: return ""
        if isinstance(items, str): return f"<li>{items}</li>"
        return "".join([f"<li>{i}</li>" for i in items])

    exp_html = ""
    for exp in ai_data.get('experience', []):
        exp_html += f"""
        <div class="job-block">
            <div class="job-header">
                <span class="job-title"><strong>{exp.get('company', '')}</strong> | {exp.get('role', '')}</span>
                <span class="job-date">{exp.get('duration', '')}</span>
            </div>
            <ul>{build_list(exp.get('description', []))}</ul>
        </div>"""

    proj_html = ""
    for proj in ai_data.get('projects', []):
        proj_html += f"""
        <div class="job-block">
            <div class="job-header">
                <span class="job-title"><strong>{proj.get('name', '')}</strong></span>
                <span class="job-stack">[{proj.get('tech_stack', '')}]</span>
            </div>
            <ul>{build_list(proj.get('description', []))}</ul>
        </div>"""

    edu_html = ""
    for edu in ai_data.get('education', []):
        edu_html += f"""
        <div class="job-block">
            <div class="job-header">
                <span class="job-title"><strong>{edu.get('institution', '')}</strong></span>
                <span class="job-date">{edu.get('year', '')}</span>
            </div>
            <div>{edu.get('degree', '')}</div>
        </div>"""

    # HARVARD STYLE TEMPLATE
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: "Times New Roman", Times, serif; font-size: 12pt; line-height: 1.3; color: #000; max-width: 800px; margin: 0 auto; padding: 40px; }}
            h1 {{ font-size: 20pt; text-transform: uppercase; text-align: center; margin-bottom: 5px; }}
            .contact {{ text-align: center; font-size: 10pt; margin-bottom: 20px; border-bottom: 1px solid #000; padding-bottom: 10px; }}
            h2 {{ font-size: 12pt; text-transform: uppercase; border-bottom: 1px solid #000; margin-top: 15px; margin-bottom: 8px; font-weight: bold; }}
            .job-block {{ margin-bottom: 10px; }}
            .job-header {{ display: flex; justify-content: space-between; }}
            ul {{ margin: 2px 0 5px 20px; padding: 0; }}
            li {{ margin-bottom: 2px; text-align: justify; }}
            .page-break {{ page-break-before: always; }}
            
            /* Cover Letter */
            .cl-body {{ font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.5; margin-top: 40px; }}
        </style>
    </head>
    <body>
        <!-- PAGE 1: RESUME -->
        <h1>{personal.get('name', 'Candidate')}</h1>
        <div class="contact">
            {personal.get('email', '')} | {personal.get('phone', '')} | {personal.get('linkedin', '')}
        </div>

        <h2>Professional Summary</h2>
        <p style="text-align: justify;">{summary}</p>

        <h2>Skills</h2>
        <p style="text-align: justify;">{skills}</p>

        <h2>Experience</h2>
        {exp_html}

        <h2>Projects</h2>
        {proj_html}

        <h2>Education</h2>
        {edu_html}

        <!-- PAGE 2: COVER LETTER -->
        <div class="page-break"></div>
        <h1>Cover Letter</h1>
        <div class="cl-body">
            {cover_letter}
        </div>
    </body>
    </html>
    """

def save_application_files(job_id, ai_data):
    if not ai_data: return None
    folder = "generated_applications"
    os.makedirs(folder, exist_ok=True)
    
    html_content = generate_resume_html(job_id, ai_data)
    html_path = f"{folder}/{job_id}.html"
    pdf_path = f"{folder}/{job_id}.pdf"
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    try:
        # DYNAMIC PATH DETECTION
        # Checks if we are on Windows or Linux and finds the binary automatically
        path_wkhtmltopdf = shutil.which("wkhtmltopdf")
        
        # Fallback for local Windows dev if not in PATH
        if not path_wkhtmltopdf and os.name == 'nt':
             path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

        if not path_wkhtmltopdf:
            raise EnvironmentError("wkhtmltopdf binary not found in system PATH")

        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        options = {
            'page-size': 'Letter',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'encoding': "UTF-8",
            'enable-local-file-access': None
        }
        pdfkit.from_file(html_path, pdf_path, configuration=config, options=options)
        return pdf_path
    except Exception as e:
        print(f"⚠️ PDF Generation Error: {e}")
        return html_path

async def process_job_application(job_id, url, resume_text, db_session_factory):
    async with db_session_factory() as db:
        try:
            jd_text = await scrape_job_text(url)
            ai_data = await generate_tailored_application(resume_text, jd_text)
            
            if not ai_data: raise Exception("AI generation returned empty")
            
            file_path = save_application_files(job_id, ai_data)
            
            result = await db.execute(select(Job).where(Job.id == job_id))
            job = result.scalar_one_or_none()
            if job:
                job.raw_job_description = jd_text
                job.tailored_resume_content = ai_data
                job.cover_letter = ai_data.get('cover_letter')
                job.status = "SUCCESS"
                await db.commit()
        except Exception as e:
            traceback.print_exc()
            result = await db.execute(select(Job).where(Job.id == job_id))
            job = result.scalar_one_or_none()
            if job:
                job.status = f"FAILED: {str(e)[:50]}"
                await db.commit()

# --- ENDPOINTS ---
@router.post("/apply", response_model=JobResponse)
async def create_application(job_data: JobCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    new_job = Job(url=job_data.url, original_resume=job_data.original_resume_text, status="PROCESSING")
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    from app.db.session import AsyncSessionLocal
    background_tasks.add_task(process_job_application, new_job.id, new_job.url, new_job.original_resume, AsyncSessionLocal)
    return new_job

@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job_status(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job: raise HTTPException(status_code=404, detail="Job not found")
    return job