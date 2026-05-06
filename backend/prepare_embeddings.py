
# prepare_embeddings.py
import pandas as pd
import torch, os
from sentence_transformers import SentenceTransformer


# CONFIG
DATA_PATH = "job_title_des.csv"      # ensure this CSV exists
SAVE_PATH = "job_embeddings.pt"
MODEL_NAME = "all-MiniLM-L6-v2"

# Load model
print("🔹 Loading model...")
model = SentenceTransformer(MODEL_NAME)

# Check dataset exists
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ Dataset not found at {DATA_PATH}. Place your jobs CSV there.")

df = pd.read_csv(DATA_PATH)

# Find a text column for job descriptions
text_cols = [c for c in df.columns if any(k in c.lower() for k in ("job", "description", "details"))]
if not text_cols:
    raise KeyError("❌ Could not find a job description column (look for 'job' or 'description' in column names).")
job_col = text_cols[0]

# Clean function
def clean_text(s):
    if not isinstance(s, str): return ""
    return " ".join(s.split())

df[job_col] = df[job_col].astype(str).apply(clean_text)

# Encode
print(f"⚙️ Encoding {len(df)} job descriptions from column: {job_col}")
job_texts = df[job_col].tolist()
job_embeddings = model.encode(job_texts, convert_to_tensor=True, show_progress_bar=True)

# Save
torch.save({
    "embeddings": job_embeddings,
    "df": df,
    "job_col": job_col,
    "model_name": MODEL_NAME
}, SAVE_PATH)

print(f"✅ Saved embeddings to '{SAVE_PATH}'")
