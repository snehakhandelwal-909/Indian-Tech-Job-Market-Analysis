from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA_PATH = Path(__file__).resolve().parent / "indian_tech_jobs_2026.csv"
PLOT_PATH = Path(__file__).resolve().parent / "salary_prediction_fit.png"

SKILLS = [
    "python", "sql", "excel", "power bi", "tableau", "aws", "azure",
    "machine learning", "deep learning", "nlp", "spark", "hadoop",
    "java", "javascript", "docker", "kubernetes", "tensorflow", "pytorch"
]
KEY_SKILLS = ["python", "sql", "aws", "azure", "machine learning", "power bi", "excel", "spark"]

CATEGORICAL_FEATURES = ["primary_city", "work_mode", "skill_domain", "company_size_bucket"]
NUMERIC_FEATURES = ["experience_min_yrs", "experience_max_yrs", "extracted_skill_count"]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES + [f"has_{skill.replace(' ', '_')}" for skill in KEY_SKILLS]
TARGET = "salary_midpoint_lpa"


def extract_skills(text):
    if pd.isna(text) or text == "Not Available":
        return []
    text = str(text).lower()
    return [skill for skill in SKILLS if skill in text]


def prepare_dataset(df):
    data = df[df["salary_disclosed"] == True].copy()
    print("Rows with disclosed salary:", len(data))

    data["extracted_skills"] = data["skills_required"].apply(extract_skills)
    data["extracted_skill_count"] = data["extracted_skills"].apply(len)

    for skill in KEY_SKILLS:
        col_name = f"has_{skill.replace(' ', '_')}"
        data[col_name] = data["skills_required"].astype(str).str.lower().str.contains(skill, na=False).astype(int)

    data = data.dropna(subset=FEATURES + [TARGET])
    return data


def build_pipeline(model):
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES)
        ],
        remainder="passthrough"
    )
    return Pipeline([("prep", preprocessor), ("model", model)])


def evaluate_model(model, X_train, X_test, y_train, y_test):
    pipe = build_pipeline(model)
    pipe.fit(X_train, y_train)

    preds_log = pipe.predict(X_test)
    preds_actual = np.expm1(preds_log)
    y_test_actual = np.expm1(y_test)

    rmse = np.sqrt(mean_squared_error(y_test_actual, preds_actual))
    r2 = r2_score(y_test_actual, preds_actual)
    return pipe, preds_actual, y_test_actual, rmse, r2


def plot_predictions(actual, predicted):
    plt.figure(figsize=(7, 5))
    plt.scatter(actual, predicted, alpha=0.3)
    plt.plot([actual.min(), actual.max()], [actual.min(), actual.max()], "r--")
    plt.xlabel("Actual Salary (LPA)")
    plt.ylabel("Predicted Salary (LPA)")
    plt.title("Predicted vs Actual Salary")
    plt.tight_layout()
    plt.savefig(PLOT_PATH)
    print(f"Saved plot to {PLOT_PATH}")


def main():
    df = pd.read_csv(DATA_PATH)
    data = prepare_dataset(df)

    X = data[FEATURES]
    y = np.log1p(data[TARGET])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = [
        ("Linear Regression", LinearRegression()),
        ("Random Forest", RandomForestRegressor(n_estimators=200, random_state=42))
    ]

    for name, model in models:
        pipe, preds_actual, y_test_actual, rmse, r2 = evaluate_model(model, X_train, X_test, y_train, y_test)
        print(f"{name} -> RMSE: {rmse:.2f} LPA, R²: {r2:.3f}")

        if name == "Random Forest":
            importances = pipe.named_steps["model"].feature_importances_
            feature_names = pipe.named_steps["prep"].get_feature_names_out()
            top_features = sorted(zip(feature_names, importances), key=lambda x: -x[1])[:8]
            print("Top features:", top_features)
            plot_predictions(y_test_actual, preds_actual)

    rf_pipeline = build_pipeline(RandomForestRegressor(n_estimators=200, random_state=42))
    cv_scores = cross_val_score(rf_pipeline, X, y, cv=5, scoring="r2")
    print("CV R² scores:", cv_scores)
    print("Mean CV R²:", round(cv_scores.mean(), 3))


if __name__ == "__main__":
    main()