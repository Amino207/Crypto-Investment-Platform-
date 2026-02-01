-- Create the crypto platform database
CREATE DATABASE IF NOT EXISTS crypto;

USE crypto;

-- Table: accounts
CREATE TABLE accounts (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    initial_deposit FLOAT NOT NULL
);

-- Table: assets
CREATE TABLE assets (
    asset_name VARCHAR(50) PRIMARY KEY,
    price FLOAT NOT NULL
);

-- Table: transactions
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    datetime DATETIME NOT NULL,
    username VARCHAR(50),
    action ENUM('buy', 'sell') NOT NULL,
    asset_name VARCHAR(50),
    quantity FLOAT NOT NULL,
    FOREIGN KEY (username) REFERENCES accounts(username),
    FOREIGN KEY (asset_name) REFERENCES assets(asset_name)
);

-- Table: portfolio
CREATE TABLE portfolio (
    username VARCHAR(50),
    asset_name VARCHAR(50),
    quantity FLOAT NOT NULL,
    PRIMARY KEY (username, asset_name),
    FOREIGN KEY (username) REFERENCES accounts(username),
    FOREIGN KEY (asset_name) REFERENCES assets(asset_name)
);

-- Populate the assets table with some initial data
INSERT INTO assets (asset_name, price) VALUES
('Bitcoin', 74600),
('Ethereum', 2680),
('Avax', 27),
('Link', 13.35),
('Solana', 214.80),
('Matic', 1);
