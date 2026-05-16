
# backend/api.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil

from backend.matcher import (
    match_resume_with_jobs,
    extract_text_from_resume,
    generate_llm_insights
)

app = FastAPI(title="AI Resume Matcher API")

# 🔥 FIX CORS HERE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"msg": "API working"}


# ⭐ Match endpoint
@app.post("/match")
async def match_resume(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"

    # Save uploaded file
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = match_resume_with_jobs(temp_path, top_k=5)

    return {"matches": results}


# ⭐ Insights endpoint
@app.post("/insights")
async def generate_insights(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = match_resume_with_jobs(temp_path, top_k=1)
    resume_text = extract_text_from_resume(temp_path)

    insight = generate_llm_insights(resume_text, results[0]["Job Description"])

    return {"insight": insight}
