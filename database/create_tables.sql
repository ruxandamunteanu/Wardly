CREATE DATABASE IF NOT EXISTS clothes_db;
USE clothes_db;

DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    shop VARCHAR(255),
    category_norm VARCHAR(255),
    name_clean TEXT,
    article VARCHAR(255),
    color_norm VARCHAR(255),
    price_norm DECIMAL(15,2),
    image TEXT,
    url TEXT
);

