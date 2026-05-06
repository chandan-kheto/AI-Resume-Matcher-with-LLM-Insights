

# llm_assistant.py
from transformers import pipeline

# Load free Hugging Face LLM (Mistral 7B Instruct or Llama 3)
generator = pipeline(
    "text-generation",
    model="mistralai/Mistral-7B-Instruct-v0.2",
    device_map="auto"
)

def explain_match(resume_text, job_text):
    """
    Generate an explanation why a resume matches a given job description.
    """
    prompt = f"""
    You are an AI career assistant. Analyze the following resume and job description.
    Explain clearly why the resume is a good or bad fit for this job.

    Resume:
    {resume_text[:2000]}

    Job Description:
    {job_text[:1500]}

    Give a short 5-6 line explanation in simple language.
    """
    result = generator(prompt, max_new_tokens=250, temperature=0.6)
    generated = result[0].get("generated_text", "")
    return generated



def suggest_resume_improvements(resume_text, target_role):
    """
    Suggest resume improvement tips for a target job role.
    """
    prompt = f"""
    You are an expert resume advisor.
    Based on this resume, suggest improvements to make it stronger for the role: {target_role}

    Resume:
    {resume_text[:2500]}

    Provide:
    - 3-5 missing skills or keywords
    - 2-3 bullet points to add in summary
    - Tone/style improvements
    """
    result = generator(prompt, max_new_tokens=300, temperature=0.7)
    return result[0]['generated_text']
