# 🧠 AI Resume Matcher with LLM Insights

An AI-powered web application that intelligently matches resumes with relevant job roles and provides personalized career insights using LLMs.

---

## 🚀 Features

- 🔍 **Semantic Job Matching**  
  Uses Sentence Transformers (`all-MiniLM-L6-v2`) to compute similarity between resume and job descriptions.

- 🧠 **Profile-Aware Ranking System**  
  Hybrid scoring combining:
  - Semantic similarity
  - Skill matching
  - Domain-specific boosting (AI/ML vs Backend)

- 🤖 **LLM Career Insights**  
  Generates personalized feedback using **Mistral-7B (Hugging Face)**:
  - Strengths
  - Missing skills
  - Improvement suggestions

- 📄 **Multi-format Resume Support**  
  Accepts `.pdf`, `.docx`, `.txt`

- ⚡ **Fast API Backend + React UI**  
 Modern full-stack web interface for real-time matching

- 📊 **Skill Gap Analysis**  
  Shows matched vs missing skills for each job

---

## 🏗️ Project Structure

```
AI-Resume-Matcher/
│
├── backend/
│ ├── api.py # FastAPI endpoints
│ ├── matcher.py # Matching + ranking logic
│ ├── prepare_embeddings.py # Precompute embeddings
│ ├── job_embeddings.pt # Stored embeddings
│ ├── job_title_des.csv # Job dataset
│
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ ├── pages/
│ │ └── api.js # API integration
│
├── requirements.txt
└── README.md
```

---

## 🧩 Tech Stack

| Component | Technology |
|----------|-----------|
| Frontend | React + Tailwind CSS |
| Backend | FastAPI |
| NLP Model | SentenceTransformers (MiniLM) |
| LLM | Mistral-7B (Hugging Face Offline Inference) |
| Similarity | Cosine Similarity |
| Storage | Torch (.pt embeddings) |

---

- 🧠 **Offline LLM Inference**  
  Runs Mistral-7B locally without external API calls, ensuring privacy and low latency.

## ⚙️ Setup Instructions

### 1️⃣ Clone Repo

```bash
git clone https://github.com/<your-username>/AI-Resume-Matcher.git
cd AI-Resume-Matcher
2️⃣ Backend Setup:  pip install -r requirements.txt
3️⃣ Generate Embeddings (one-time):  python prepare_embeddings.py
4️⃣ Run Backend:  uvicorn api:app --reload
5️⃣ Run Frontend:  npm run dev 
