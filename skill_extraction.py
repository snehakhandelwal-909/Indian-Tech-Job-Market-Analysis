import pandas as pd

df = pd.read_csv("indian_tech_jobs_2026.csv")

SKILLS = ["python", "sql", "excel", "power bi", "tableau", "aws", "azure",
          "machine learning", "deep learning", "nlp", "spark", "hadoop",
          "java", "javascript", "docker", "kubernetes", "tensorflow", "pytorch",
          "data analysis", "data visualization", "analytics"]

def extract_skills(text):
    if pd.isna(text) or text == "Not Available":
        return []
    text = str(text).lower()
    return [s for s in SKILLS if s in text]

df["extracted_skills"] = df["skills_required"].apply(extract_skills)
df["extracted_skill_count"] = df["extracted_skills"].apply(len)

print("Jobs with at least 1 skill matched:", (df["extracted_skill_count"] > 0).sum())
print("Total postings:", len(df))

# Skill demand by domain 
exploded = df.explode("extracted_skills").dropna(subset=["extracted_skills"])
print(exploded.groupby("skill_domain")["extracted_skills"].value_counts().groupby(level=0).head(5))
