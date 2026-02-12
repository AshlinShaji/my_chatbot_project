-- Create the database
CREATE DATABASE IF NOT EXISTS pizza_db;
USE pizza_db;

-- Table for menu items
CREATE TABLE menu_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    quantity INT DEFAULT 0,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for orders
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100),
    items TEXT,
    total_price DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO menu_items (name, description, price, quantity, category) VALUES
('Margherita', 'Fresh mozzarella, tomato, basil', 12.99, 45, 'Pizza'),
('Pepperoni', 'Classic pepperoni pizza', 13.99, 38, 'Pizza'),
('Vegetarian', 'Mixed fresh vegetables', 11.99, 52, 'Pizza'),
('Caesar Salad', 'Fresh romaine, parmesan', 8.99, 30, 'Salad'),
('Garlic Bread', 'Fresh baked with herbs', 4.99, 100, 'Sides');

INSERT INTO orders (customer_name, items, total_price, status) VALUES
('John Doe', 'Margherita, Garlic Bread', 17.98, 'Completed'),
('Jane Smith', 'Pepperoni x2', 27.98, 'Completed'),
('Bob Johnson', 'Vegetarian, Caesar Salad', 20.98, 'In Progress');