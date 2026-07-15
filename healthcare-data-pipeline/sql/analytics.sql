-- ============================================
-- Healthcare Data Pipeline - SQL Analytics
-- ============================================
-- What: Analytical queries on the patients table.
-- Why:  Demonstrates SQL skills for data analysis.
-- How:  Run these queries after ETL loads data into MySQL.
--
-- Usage:
--   mysql -u root -p healthcare_db < sql/analytics.sql
-- ============================================

USE healthcare_db;

-- -------------------------------------------------
-- 1. Average Billing Amount
-- -------------------------------------------------
-- What is the overall average billing amount?

SELECT
    ROUND(AVG(billing_amount), 2) AS average_billing
FROM patients;


-- -------------------------------------------------
-- 2. Most Common Disease (Medical Condition)
-- -------------------------------------------------
-- Which medical condition appears most frequently?

SELECT
    medical_condition,
    COUNT(*) AS patient_count
FROM patients
GROUP BY medical_condition
ORDER BY patient_count DESC
LIMIT 1;


-- -------------------------------------------------
-- 3. Admissions by Type
-- -------------------------------------------------
-- How many patients were admitted under each type?

SELECT
    admission_type,
    COUNT(*) AS total_admissions
FROM patients
GROUP BY admission_type
ORDER BY total_admissions DESC;


-- -------------------------------------------------
-- 4. Insurance Provider Distribution
-- -------------------------------------------------
-- How are patients distributed across insurance providers?

SELECT
    insurance_provider,
    COUNT(*) AS patient_count
FROM patients
GROUP BY insurance_provider
ORDER BY patient_count DESC;


-- -------------------------------------------------
-- 5. Average Billing by Disease
-- -------------------------------------------------
-- What is the average billing amount for each condition?

SELECT
    medical_condition,
    ROUND(AVG(billing_amount), 2) AS avg_billing,
    COUNT(*) AS patient_count
FROM patients
GROUP BY medical_condition
ORDER BY avg_billing DESC;
