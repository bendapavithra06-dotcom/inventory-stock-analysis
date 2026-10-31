CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(120) NOT NULL,
    phone VARCHAR(25),
    email VARCHAR(120),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    opening_stock INT NOT NULL DEFAULT 0,
    reorder_level INT NOT NULL DEFAULT 5,
    unit_cost DECIMAL(12,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (opening_stock >= 0),
    CHECK (reorder_level >= 0),
    CHECK (unit_cost >= 0)
);

CREATE TABLE IF NOT EXISTS stock_transactions (
    transaction_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    transaction_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_type ENUM('IN','OUT') NOT NULL,
    quantity INT NOT NULL,
    supplier_id INT NULL,
    notes VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transaction_product FOREIGN KEY (product_id)
        REFERENCES products(product_id),
    CONSTRAINT fk_transaction_supplier FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id),
    CHECK (quantity > 0)
);

CREATE INDEX idx_transactions_product_date
ON stock_transactions(product_id, transaction_date);
