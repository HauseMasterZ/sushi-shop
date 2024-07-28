CREATE TABLE Orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total_price DECIMAL(8, 2) NOT NULL,
    discount_applied VARCHAR(255),
    discount_amount DECIMAL(8, 2),
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
