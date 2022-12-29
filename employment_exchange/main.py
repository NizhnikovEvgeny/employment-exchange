from fastapi import FastAPI
import uvicorn
from db.base import database
from endpoints import users, auth, jobs, responds, jobs_page
from core.config import DATABASE_URL

app = FastAPI(title="Employment exchange")
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(responds.router, tags=["responds"])
app.include_router(jobs_page.router, prefix="/job_page", tags=["job page"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
