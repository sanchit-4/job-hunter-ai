from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Define the structure we want the LLM to output
class TailoredResume(BaseModel):
    summary: str = Field(description="A professional summary tailored to the job")
    skills_highlighted: list[str] = Field(description="List of top 10 relevant skills found in the JD")
    experience_bullets: dict[str, list[str]] = Field(description="Key: Company Name, Value: List of rewritten bullet points")
    cover_letter: str = Field(description="A complete cover letter")

class ResumeAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.1)
        self.parser = JsonOutputParser(pydantic_object=TailoredResume)

    async def tailor_resume(self, original_resume_text: str, job_description: str) -> dict:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert career coach and resume writer. Your goal is to maximize ATS (Applicant Tracking System) compatibility."),
            ("user", """
            JOB DESCRIPTION:
            {job_description}
            
            MY RESUME:
            {resume_text}
            
            INSTRUCTIONS:
            1. Analyze the Job Description for keywords.
            2. Rewrite my resume summary to match the persona they are looking for.
            3. Select my experience bullet points and rephrase them to emphasize the specific skills requested in the JD.
            4. Write a professional cover letter.
            
            {format_instructions}
            """)
        ])

        chain = prompt | self.llm | self.parser
        
        result = await chain.ainvoke({
            "job_description": job_description,
            "resume_text": original_resume_text,
            "format_instructions": self.parser.get_format_instructions()
        })
        
        return result
    