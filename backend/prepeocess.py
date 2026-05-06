
import pandas as pd
import torch, os
from sentence_transformers import SentenceTransformer


# =====================================================
# ⚙️ CONFIGURATION
# =====================================================
DATA_PATH = "job_title_des.csv"          # your job dataset path
SAVE_PATH = "job_embeddings.pt"      # where to save embeddings
MODEL_NAME = "all-MiniLM-L6-v2"      # small + accurate model

# =====================================================
# 🧠 LOAD MODEL
# =====================================================
print("🔹 Loading sentence embedding model...")
model = SentenceTransformer(MODEL_NAME)

# =====================================================
# 📄 LOAD JOB DATASET
# =====================================================
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ File not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

# Use any columns you have for job info
text_columns = [col for col in df.columns if col.lower() in ["job_description", "description", "job_details", "details"]]
if not text_columns:
    raise KeyError("❌ No job description column found in your dataset! Please ensure you have a 'job_description' column.")

job_col = text_columns[0]

# Clean text
def clean_text(text):
    if not isinstance(text, str):
        return ""
    return text.replace("\n", " ").replace("\r", " ").strip()

df[job_col] = df[job_col].astype(str).apply(clean_text)

# =====================================================
# 🧠 ENCODE ALL JOB DESCRIPTIONS
# =====================================================
print(f"⚙️ Encoding {len(df)} job descriptions...")
job_texts = df[job_col].tolist()
job_embeddings = model.encode(job_texts, convert_to_tensor=True, show_progress_bar=True)

# =====================================================
# 💾 SAVE EMBEDDINGS
# =====================================================
torch.save({
    "embeddings": job_embeddings,
    "df": df,
    "model_name": MODEL_NAME
}, SAVE_PATH)

print(f"✅ Job embeddings saved successfully to '{SAVE_PATH}'!")
