# Indian Tech Job Market Analysis

## Overview

This project analyzes **23,201+ Indian technology job postings** to uncover hiring trends, salary patterns, in-demand skills, and to build a predictive model for salary estimation. The analysis was performed using **Python, SQL, and Excel**, and includes two connected components: (1) skill extraction and standardization, and (2) salary prediction using machine learning.

---

## Objectives

- Analyze hiring trends across the Indian technology sector.
- Identify the most in-demand job roles, skills, and hiring locations.
- Standardize inconsistent skill listings into a usable taxonomy.
- Build and validate a model to predict salary from job posting features.
- Generate business insights using data visualization and SQL analysis.

---

## Dataset

- **Source:** Kaggle
- **Records:** 23,201 job listings (2,768 with disclosed salary)
- **Columns:** 32 features

### Key Attributes

- Company Name, Job Title, Role Category
- Primary City, Work Mode, Experience Tier
- Company Rating, Salary Range
- Skills Required, Skill Domain
- Fresher Friendly, Days Since Posted

---

## Tools & Technologies

Python (Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn), SQL, Microsoft Excel

---

## Part 1: Skill Extraction & Standardization

**Goal:** Map messy, free-text skill listings to a standard taxonomy for analysis.

**Approach:**

- Initial attempt extracted skills from the `job_description` field — this failed, returning zero matches on 19,669 of 23,201 postings, since the field was mostly truncated boilerplate text rather than real content.
- Pivoted to standardizing the `skills_required` column instead, using pattern matching against a defined skill taxonomy.
- Achieved a **66% match rate (15,346 / 23,201 postings)**, with clear domain-specific patterns emerging — e.g., Python/ML skills clustering in AI roles, Power BI/Excel clustering in BI roles.

This pivot — diagnosing why the first approach failed and adjusting the data source rather than the method — is documented as part of the project's process, not hidden.

---

## Part 2: Salary Prediction Model

**Goal:** Predict salary from job posting features (skills present, experience, work mode, etc.).

**Approach:**

- Built and compared **Linear Regression** and **Random Forest** models on 2,768 postings with disclosed salaries.
- Iterated by adding individual skill flags as features, log-transforming salary to address skew, and using **5-fold cross-validation** to get an honest performance estimate.
- Initial single train/test split gave an optimistic R² of 0.335; the cross-validated mean R² was **~0.29–0.38** depending on model configuration.

**Diagnostics:**

- The predicted-vs-actual plot shows the model systematically underpredicts high salaries — a long-tail distribution problem common in salary data, where a small number of very high earners are hard to predict from skill flags alone.
- Feature importance (Random Forest) shows experience (min/max years) and extracted skill count as the strongest predictors, ahead of any individual skill flag.

### Limitations

- Salary is influenced by many factors not present in this dataset (location cost-of-living, company size, negotiation, seniority nuance beyond stated experience tier), so an R² in the 0.3–0.4 range is expected, not a flaw to hide.
- The model underperforms on high-salary outliers and should be read as a directional estimator, not a precise predictor.
- This is an analytics/portfolio prototype, not a production-ready deployment.

---

## Project Workflow

1. **Data Cleaning** — removed duplicates, checked missing values, verified data types, filtered salary data for meaningful analysis.
2. **Skill Extraction** — standardized `skills_required` into a taxonomy (see Part 1).
3. **Exploratory Data Analysis** — hiring trends, top companies/cities, work mode and experience distributions, salary tiers, skill domain analysis.
4. **SQL Analysis** — hiring by company, city, role, work mode, salary, ratings, skill demand, fresher-friendly roles.
5. **Excel Dashboard** — pivot tables and charts for hiring cities, companies, roles, experience levels, work modes, salary distribution.
6. **Salary Prediction Modeling** — Linear Regression and Random Forest with cross-validation (see Part 2).

---

## Business Insights

- Data Scientist and Data Analyst roles account for a significant share of postings.
- Hiring is concentrated in major Indian tech hubs.
- Hybrid and onsite roles are more common than fully remote positions.
- Salary transparency is limited — most employers don't publish salary details.
- Experience level and extracted skill count are stronger salary predictors than any single skill.
- A relatively small number of companies contribute a large share of total postings.

---

## Repository Structure

Indian-Tech-Job-Market-Analysis/
│
├── data/
│ ├── indian_tech_jobs_2026.csv
│ └── jobs_with_extracted_skills.csv
│
├── python/
│ ├── skill_extraction.py
│ ├── salary_prediction.py
│ ├── skill_extraction_summary.png
│ └── salary_prediction_fit.png
│
├── sql/
│ └── Job_Market_SQL_Queries.sql
│
├── excel/
│ └── Job_Market_Dashboard.xlsx
│
└── README.md

---

## Key Skills Demonstrated

- Data cleaning, EDA, SQL querying, dashboard development
- Text-based feature extraction and taxonomy design
- Predictive modeling (Linear Regression, Random Forest)
- Model validation (cross-validation, honest performance reporting)
- Diagnosing and communicating model limitations

---

## Future Improvements

- Build an interactive Power BI or Streamlit dashboard for live exploration.
- Perform NLP analysis on full job descriptions (once cleaner text data is available).
- Expand the skill taxonomy and test additional model types (e.g. Gradient Boosting).

---

## Author

**Sneha Khandelwal**
B.Tech Chemical Engineering — Birla Institute of Technology, Mesra

---

## License

This project is intended for educational and portfolio purposes only. The dataset belongs to its original creator on Kaggle.
