# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from pydantic import BaseModel, Field
# from app.core.config import settings

# # Define the expected JSON structure
# class ResumeOutput(BaseModel):
#     professional_summary: str = Field(description="Rewritten summary tailored to the job")
#     skills: list[str] = Field(description="List of relevant skills from the JD")
#     experience_bullets: dict[str, list[str]] = Field(description="Dictionary: Key=Company Name, Value=List of rewritten bullets")
#     cover_letter: str = Field(description="A professional cover letter")

# async def generate_tailored_application(resume_text: str, job_description: str):
#     # Initialize Gemini Pro
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash", # Faster and cheaper, use "gemini-1.5-pro" for higher quality
#         google_api_key=settings.GOOGLE_API_KEY,
#         temperature=0.2,
#         convert_system_message_to_human=True
#     )
    
#     parser = JsonOutputParser(pydantic_object=ResumeOutput)

#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are an expert career coach. Your goal is to maximize ATS compatibility."),
#         ("human", """
#         I need you to tailor my resume for a specific job application.
        
#         JOB DESCRIPTION:
#         {jd}
        
#         MY RESUME:
#         {resume}
        
#         INSTRUCTIONS:
#         1. Rewrite my summary to match the job persona.
#         2. extract the top skills from the JD that I likely have.
#         3. Rewrite my experience bullet points to emphasize impact and keywords from the JD.
#         4. Write a strong cover letter.
        
#         Response must be valid JSON.
#         {format_instructions}
#         """)
#     ])

#     chain = prompt | llm | parser

#     try:
#         response = await chain.ainvoke({
#             "jd": job_description,
#             "resume": resume_text,
#             "format_instructions": parser.get_format_instructions()
#         })
#         return response
#     except Exception as e:
#         print(f"Gemini Error: {e}")
#         raise e


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
from app.core.config import settings
import asyncio

# --- DATA STRUCTURES ---
class ExperienceItem(BaseModel):
    company: str
    role: str
    duration: str
    description: List[str] = Field(description="3-5 bullet points using STAR method (Situation, Task, Action, Result).")

class EducationItem(BaseModel):
    institution: str
    degree: str
    year: str

class ProjectItem(BaseModel):
    name: str
    tech_stack: str
    description: List[str] = Field(description="2-3 bullet points highlighting technical difficulty and impact.")

class FullResumeResponse(BaseModel):
    personal_info: dict
    professional_summary: str = Field(description="A powerful 3-4 sentence summary tailored to the JD.")
    skills: List[str]
    experience: List[ExperienceItem]
    projects: List[ProjectItem]
    education: List[EducationItem]
    cover_letter: str

async def generate_tailored_application(resume_text: str, job_description: str):
    # Try high-quality model first, fall back to stable
    models_to_try = ["gemini-2.5-flash", "gemini-pro"]
    
    for model_name in models_to_try:
        try:
            # Increased temperature for more creative/better writing
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.4, 
                convert_system_message_to_human=True
            )
            
            parser = JsonOutputParser(pydantic_object=FullResumeResponse)

            prompt = ChatPromptTemplate.from_messages([
                ("human", """
                You are a Senior Technical Resume Writer & Career Coach.
                
                YOUR GOAL: 
                Rewrite the candidate's resume to significantly increase their chances of getting an interview for the target job.
                
                TARGET JOB DESCRIPTION (JD):
                {jd}
                
                CANDIDATE'S OLD RESUME:
                {resume}
                
                INSTRUCTIONS:
                1. **Professional Summary:** Write a completely new, punchy summary (max 4 lines) that explicitly connects the candidate's background to the JD's biggest pain points.
                2. **Experience & Projects:** Do NOT just copy the old resume. REWRITE the bullet points using the **STAR Method** (Situation, Task, Action, Result).
                   - Use strong action verbs (Architected, Engineered, Optimized, Led).
                   - QUANTIFY results wherever possible (e.g., "reduced latency by 20%", "handled 10k requests/sec").
                   - If the JD asks for a specific skill (e.g., "Redis") and the candidate has it, ensure it appears in a bullet point.
                3. **Skills:** Reorder and select skills to match the JD keywords.
                4. **Cover Letter:** Write a confident, specific cover letter that references the company's mission.
                
                IMPORTANT:
                - Return VALID JSON only.
                - Do not make up fake experiences, but you can polish/rephrase existing ones to sound more impressive.
                
                {format_instructions}
                """)
            ])

            chain = prompt | llm | parser

            # Truncate inputs to avoid context limits
            response = await chain.ainvoke({
                "jd": job_description[:15000],
                "resume": resume_text[:25000],
                "format_instructions": parser.get_format_instructions()
            })
            
            return response

        except Exception as e:
            print(f"⚠️ Model {model_name} failed: {e}")
            continue

    # Fallback if AI fails completely
    return None