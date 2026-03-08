-- Create Database
CREATE DATABASE IF NOT EXISTS phonepe_pulse;
USE phonepe_pulse;

-- Aggregated Transaction Table
CREATE TABLE aggregated_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    transaction_type VARCHAR(100),
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

-- Aggregated User Table
CREATE TABLE aggregated_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    brand VARCHAR(100),
    user_count BIGINT,
    percentage DOUBLE
);

-- Map Transaction Table
CREATE TABLE map_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    district VARCHAR(100),
    year INT,
    quarter INT,
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

-- Map User Table
CREATE TABLE map_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    district VARCHAR(100),
    year INT,
    quarter INT,
    registered_users BIGINT,
    app_opens BIGINT
);

-- Top Transaction Table
CREATE TABLE top_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    district VARCHAR(100),
    year INT,
    quarter INT,
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

-- Top User Table
CREATE TABLE top_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    district VARCHAR(100),
    year INT,
    quarter INT,
    registered_users BIGINT
);