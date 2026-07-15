-- ============================================
-- Healthcare Data Pipeline - Database Schema
-- ============================================
-- This script creates the MySQL database and
-- the patients table used by the ETL pipeline.
--
-- Run this ONCE before loading data:
--   mysql -u root -p < schema.sql
-- ============================================

-- Create the database
CREATE DATABASE IF NOT EXISTS healthcare_db;
USE healthcare_db;

-- Create the patients table
-- Stores cleaned and transformed patient records
CREATE TABLE IF NOT EXISTS patients (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    age             INT NOT NULL,
    gender          VARCHAR(10),
    medical_condition VARCHAR(100),
    admission_type  VARCHAR(20),
    insurance_provider VARCHAR(50),
    billing_amount  DECIMAL(10, 2),
    test_result     VARCHAR(20),
    length_of_stay  INT COMMENT 'Engineered feature: days between admission and discharge'
);
