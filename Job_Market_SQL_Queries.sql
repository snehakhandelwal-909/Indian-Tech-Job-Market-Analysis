-- Total number of job postings

SELECT COUNT(*) AS Total_Jobs
FROM tech_jobs;

-- Companies with the highest number of job postings

SELECT
    company_name,
    COUNT(*) AS Total_Jobs
FROM tech_jobs
GROUP BY company_name
ORDER BY Total_Jobs DESC
LIMIT 10;

-- Cities with the highest hiring demand

SELECT
    primary_city,
    COUNT(*) AS Total_Jobs
FROM tech_jobs
GROUP BY primary_city
ORDER BY Total_Jobs DESC;

-- Most frequently advertised roles

SELECT
    role_category,
    COUNT(*) AS Total_Postings
FROM tech_jobs
GROUP BY role_category
ORDER BY Total_Postings DESC;

-- Remote, Hybrid and Onsite jobs

SELECT
    work_mode,
    COUNT(*) AS Total_Jobs
FROM tech_jobs
GROUP BY work_mode
ORDER BY Total_Jobs DESC;

-- Average company rating for each role

SELECT
    role_category,
    ROUND(AVG(company_rating),2) AS Avg_Rating
FROM tech_jobs
GROUP BY role_category
ORDER BY Avg_Rating DESC;

-- Average salary offered by each role

SELECT
    role_category,
    ROUND(AVG(salary_midpoint_lpa),2) AS Avg_Salary
FROM tech_jobs
WHERE salary_midpoint_lpa>0
GROUP BY role_category
ORDER BY Avg_Salary DESC;

-- Average salary across experience levels

SELECT
    experience_tier,
    ROUND(AVG(salary_midpoint_lpa),2) AS Avg_Salary
FROM tech_jobs
WHERE salary_midpoint_lpa>0
GROUP BY experience_tier
ORDER BY Avg_Salary DESC;

-- Best rated companies

SELECT
    company_name,
    ROUND(AVG(company_rating),2) AS Rating
FROM tech_jobs
GROUP BY company_name
HAVING COUNT(*)>=5
ORDER BY Rating DESC
LIMIT 10;

-- Number of fresher friendly jobs

SELECT
    is_fresher_friendly,
    COUNT(*) AS Total
FROM tech_jobs
GROUP BY is_fresher_friendly;

-- Jobs in each salary tier

SELECT
    salary_tier,
    COUNT(*) AS Total_Jobs
FROM tech_jobs
GROUP BY salary_tier
ORDER BY Total_Jobs DESC;

-- Most demanded skill domains

SELECT
    skill_domain,
    COUNT(*) AS Jobs
FROM tech_jobs
GROUP BY skill_domain
ORDER BY Jobs DESC;

-- Average number of skills expected

SELECT
    ROUND(AVG(skills_count),2) AS Avg_Skills
FROM tech_jobs;

-- Average minimum and maximum experience

SELECT
    ROUND(AVG(experience_min_yrs),1) AS Avg_Min_Experience,
    ROUND(AVG(experience_max_yrs),1) AS Avg_Max_Experience
FROM tech_jobs;

-- Companies offering highest salaries

SELECT
    company_name,
    ROUND(AVG(salary_midpoint_lpa),2) AS Avg_Salary,
    COUNT(*) AS Jobs
FROM tech_jobs
WHERE salary_midpoint_lpa>0
GROUP BY company_name
HAVING COUNT(*)>=5
ORDER BY Avg_Salary DESC
LIMIT 10;

-- Rank companies by number of job postings

SELECT
    company_name,
    COUNT(*) AS Total_Jobs,
    DENSE_RANK() OVER(ORDER BY COUNT(*) DESC) AS Company_Rank
FROM tech_jobs
GROUP BY company_name;