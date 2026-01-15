from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.job import Job, JobStatus
from app.services.resume_optimizer import ResumeAgent
from app.tools.scraping_tools import scrape_job_description

router = APIRouter()

@router.post("/apply-workflow")
async def start_application_workflow(
    job_url: str,
    user_resume_text: str,  # In a real app, retrieve this from DB
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # 1. Create Job Entry
    new_job = Job(url=job_url, status=JobStatus.ANALYZING)
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)

    # 2. Trigger Async Task (Optimization & Application)
    background_tasks.add_task(process_application, new_job.id, job_url, user_resume_text, db)
    
    return {"message": "Application workflow started", "job_id": new_job.id}

async def process_application(job_id, url, resume_text, db: AsyncSession):
    # Note: In production, use Celery/Redis for this, not BackgroundTasks
    # Re-fetch DB session for background task context if needed or pass ID to worker
    
    # A. Scrape
    jd_text = await scrape_job_description.ainvoke(url)
    
    # B. Optimize
    agent = ResumeAgent()
    tailored_data = await agent.tailor_resume(resume_text, jd_text)
    
    # C. Update DB (Mocking update logic here)
    print(f"Drafted Cover Letter for {url}: \n {tailored_data['cover_letter'][:100]}...")
    
    # D. Auto-Submit Logic
    # This is where you would call a Selenium/Playwright script to fill forms
    # await fill_application_form(url, tailored_data)