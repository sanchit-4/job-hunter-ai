import sys
import asyncio

# --- CRITICAL WINDOWS FIX (Must be at the very top) ---
# This ensures that when Uvicorn reloads, the new worker process 
# also gets the correct ProactorEventLoop policy.
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
# ------------------------------------------------------

from fastapi import FastAPI
from app.api.v1.router import router
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="JobHunterAI")

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {
        "status": "JobHunterAI is Active", 
        "platform": sys.platform,
        "event_loop": str(asyncio.get_event_loop_policy())
    }