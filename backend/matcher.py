
import torch
import pandas as pd
import torch.serialization as serialization
from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader
import docx, os
from huggingface_hub import InferenceClient

# =====================================================
# 🔹 CONFIGURATION
# =====================================================
MODEL_NAME = "all-MiniLM-L6-v2"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "job_embeddings.pt")

# Initialize Hugging Face LLM client
HF_TOKEN = os.getenv("HF_TOKEN")  # read token from environment
client = InferenceClient(model = "mistralai/Mistral-7B-Instruct-v0.3", token=HF_TOKEN)

# =====================================================
# 🔹 LOAD MODEL + PRECOMPUTED EMBEDDINGS
# =====================================================
print("🚀 Loading model and precomputed embeddings...")
model = SentenceTransformer(MODEL_NAME)

if not os.path.exists(EMBEDDINGS_PATH):
    raise FileNotFoundError("❌ job_embeddings.pt not found! Run prepare_embeddings.py first.")


data = torch.load(EMBEDDINGS_PATH, weights_only=False)
job_embeddings = data["embeddings"]
job_data = data["df"]

print(f"✅ Loaded {len(job_data)} job entries from dataset.")

SKILLS = [
    "python", "llm", "fastapi", "flask", "mysql", "sql", "excel",
    "power bi", "seaborn", "machine learning", "deep learning",
    "tensorflow", "pytorch", "nlp", "data analysis", "statistics",
    "pandas", "numpy", "java", "springboot", "react", "api", "aws", "docker"
]

ROLE_CATEGORIES = {
    "ml": ["machine learning", "ai", "deep learning"],
    "data": ["data analyst", "data scientist"],
    "backend": ["backend", "developer", "api"],
    "software": ["software engineer", "developer"]
}

def extract_skills(text):
    text = text.lower()
    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    return found
# =====================================================
# 🔹 FUNCTION: EXTRACT TEXT FROM RESUME
# =====================================================
def extract_text_from_resume(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file format. Please upload a PDF, DOCX, or TXT file.")
    return text.strip()

# =====================================================
# 🔹 ROLE EXTRACTION FUNCTION (FIXED POSITION)
# =====================================================
def extract_role_from_text(text):
    text = text.lower()

    if any(x in text for x in [
        "data scientist", "machine learning engineer",
        "deep learning", "modeling", "predictive model"
       ]):
        return "data scientist"

    elif any(x in text for x in [
       "machine learning", "ml", "neural network", "nlp"
       ]):
        return "machine learning"

    elif any(x in text for x in [
          "data analyst", "power bi", "dashboard"
        ]):
        return "data analyst"

    elif any(x in text for x in ["backend", "spring", "api", "fastapi"]):
        return "backend"
    else:
        return "software engineer"

# =====================================================
# 🔹 FUNCTION: MATCH RESUME WITH JOBS
# =====================================================
def match_resume_with_jobs(resume_path, top_k=5):

    # 1. Extract resume text
    resume_text = extract_text_from_resume(resume_path)

    # 2. Extract role + skills
    role = extract_role_from_text(resume_text)
    resume_skills = extract_skills(resume_text)

    print("Role:", role)
    print("Skills:", resume_skills)

    # 3. Smart filtering
    filtered_indices = []

    for i, row in job_data.iterrows():
        title = str(row.get("Job Title", "")).lower()

        if (
            role in title
            or any(word in title for word in role.split())
            or any(skill in title for skill in resume_skills)
            or any(word in title for word in ["data science", "software developer", "data analyst", "machine learning"])
        ):
            filtered_indices.append(i)
        elif i % 2 == 0:
            filtered_indices.append(i)

    if len(filtered_indices) < 20:
        filtered_indices = list(range(len(job_data)))

    filtered_indices = list(set(filtered_indices))

    # 4. Filter embeddings
    filtered_embeddings = job_embeddings[filtered_indices]

    # 5. Encode resume
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    # 6. Similarity
    similarities = util.cos_sim(resume_embedding, filtered_embeddings)[0]

    # Get more candidates
    top_results = torch.topk(similarities, k=min(top_k * 20, len(filtered_indices)))

    # Detect profile ONCE (before loop)
    is_ai_profile = any(x in resume_text.lower() for x in [
      "llm", "rag", "transformer", "langchain"
    ])

    results = []

    for score, idx in zip(top_results.values, top_results.indices):

        real_idx = filtered_indices[int(idx)]
        row = job_data.iloc[real_idx]

        title = str(row.get("Job Title", "")).lower()
        job_desc = str(row.get("Job Description", "") or "").lower()


        # 🔥 SMART DISPLAY TITLE (FINAL)
        if "data scientist" in title:
           display_title = "Data Scientist"

        elif "data analyst" in title:
           display_title = "Data Analyst"

        elif "machine learning" in title or "ml" in title:
             display_title = "Machine Learning Engineer"

        elif "backend" in title:
             display_title = "Backend Developer"

        elif "software" in title:
             display_title = "Software Developer"

        elif "ai" in title:
           display_title = "AI Engineer"

        else:
          display_title = role.title() + " Engineer"

         # 🔥 SKILLS
        matched_skills = [s for s in resume_skills if s in job_desc]
        skill_score = len(matched_skills)

        job_skills = [s for s in SKILLS if s in job_desc]
        missing_skills = [s for s in job_skills if s not in resume_skills]

        base_score = float(score) * 60
        skill_part = skill_score * 5

        ai_score = sum(1 for x in ["llm", "rag", "transformer", "nlp", "ai", "deep learning"] if x in job_desc) * 8

        backend_score = sum(1 for x in [
        "api", "sql", "database"] if x in job_desc) * 2


        # 🔥 Final score
        score_percent =  base_score + skill_part + ai_score + backend_score

          # 🔥 AI PROFILE BOOST
        if is_ai_profile and ai_score > 0:
          score_percent += 10

        # 🔥 Confidence
        if score_percent >= 70:
            confidence = "High"
        elif score_percent >= 50:
            confidence = "Medium"
        else:
            confidence = "Low"

        explanation = (
            f"Matched skills: {', '.join(matched_skills[:3])}"
            if matched_skills else "General profile match"
        )

        results.append({
            "Job Title": display_title,
            "Job Description": row.get("Job Description", "")[:200] + "...",
            "Match Score": round(score_percent, 2),
            "Confidence": confidence,
            "Matched Skills": matched_skills[:5],
            "Missing Skills": missing_skills[:5],
            "Why Matched": explanation
        })

    # 🔥 Remove duplicate titles (CORRECT PLACE)
    unique_results = []
    seen = set()

    for r in results:
        key = r["Job Title"] + r["Job Description"][:50].lower()

        if key not in seen:
           unique_results.append(r)
           seen.add(key)

    if len(unique_results) < top_k:
       for r in results:
           if r not in unique_results:
              unique_results.append(r)
           if len(unique_results) >= top_k:
              break

    results = unique_results

    # Sort results
    results = sorted(results, key=lambda x: x["Match Score"], reverse=True)

    # 🔥 FORCE DIVERSITY
    final_results = []
    seen_roles = {}

    for job in results:
       role = job["Job Title"]

       if role not in seen_roles:
          seen_roles[role] = 0

       if seen_roles[role] < 2:   # max 2 per role
           final_results.append(job)
           seen_roles[role] += 1

       if len(final_results) >= top_k:
           break

    results = final_results

    # 🔥 FINAL OUTPUT (correct placement)
    if len(results) == 0:
        return {"top_match": None, "others": []}

    return {
        "top_match": results[0],
        "others": results[1:]
    }

# =====================================================
# 🔹 FUNCTION: LLM-Powered Resume Insights
# =====================================================
def generate_llm_insights(resume_text, top_jobs):
    try:
        prompt = f"""
You are an AI career coach.
Below is a candidate's resume and top matched job descriptions.
Explain:
1️⃣ Why these jobs match or don't match.
2️⃣ What important skills or keywords are missing in the resume.
3️⃣ Give 2-3 improvement tips for better matching in the future.

Resume: {resume_text[:1500]}

Top Jobs Description: {top_jobs}
"""

        messages = [
            {"role": "system", "content": "You are a helpful AI career advisor."},
            {"role": "user", "content": prompt},
        ]

        # ✅ Use chat_completion() instead of conversational()
        response = client.chat_completion(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=messages,
            max_tokens=500,
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"⚠️ Error generating insights: {str(e)}"




