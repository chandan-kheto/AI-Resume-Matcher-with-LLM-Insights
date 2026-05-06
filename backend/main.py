
# backend/api.py
import sys, os
sys.path.append(os.path.abspath("."))

from fastapi import FastAPI, UploadFile, File
import shutil

from matcher import match_resume_with_jobs, extract_text_from_resume, generate_llm_insights
from fastapi.middleware.cors import CORSMiddleware

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

    os.remove(temp_path)

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

    os.remove(temp_path)

    return {"insight": insight}
