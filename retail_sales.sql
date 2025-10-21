-- Retail Sales Database Schema and Data

-- Create Products table
CREATE TABLE Products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);

-- Create Customers table
CREATE TABLE Customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Create Sales table
CREATE TABLE Sales (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(id),
    FOREIGN KEY (customer_id) REFERENCES Customers(id)
);

-- Insert data into Products (10 records)
INSERT INTO Products (name, category, price) VALUES
('Laptop', 'Electronics', 1200.00),
('Mouse', 'Electronics', 25.00),
('Keyboard', 'Electronics', 50.00),
('Book', 'Books', 15.00),
('Shirt', 'Clothing', 30.00),
('Pants', 'Clothing', 60.00),
('Shoes', 'Clothing', 80.00),
('Phone', 'Electronics', 800.00),
('Tablet', 'Electronics', 400.00),
('Headphones', 'Electronics', 100.00);

-- Insert data into Customers (10 records)
INSERT INTO Customers (name, age, email) VALUES
('Alice Johnson', 28, 'alice@example.com'),
('Bob Smith', 35, 'bob@example.com'),
('Charlie Brown', 22, 'charlie@example.com'),
('Diana Prince', 30, 'diana@example.com'),
('Eve Wilson', 45, 'eve@example.com'),
('Frank Miller', 50, 'frank@example.com'),
('Grace Lee', 27, 'grace@example.com'),
('Henry Davis', 33, 'henry@example.com'),
('Ivy Chen', 29, 'ivy@example.com'),
('Jack Taylor', 40, 'jack@example.com');

-- Insert data into Sales (10 records, ensuring valid product and customer IDs)
INSERT INTO Sales (product_id, customer_id, quantity, sale_date, total_amount) VALUES
(1, 1, 1, '2023-10-01', 1200.00),
(2, 2, 2, '2023-10-02', 50.00),
(3, 3, 1, '2023-10-03', 50.00),
(4, 4, 3, '2023-10-04', 45.00),
(5, 5, 2, '2023-10-05', 60.00),
(6, 6, 1, '2023-10-06', 60.00),
(7, 7, 1, '2023-10-07', 80.00),
(8, 8, 1, '2023-10-08', 800.00),
(9, 9, 1, '2023-10-09', 400.00),
(10, 10, 2, '2023-10-10', 200.00);

-- Additional sales to make trends visible
INSERT INTO Sales (product_id, customer_id, quantity, sale_date, total_amount) VALUES
(1, 2, 1, '2023-10-11', 1200.00),
(2, 3, 1, '2023-10-12', 25.00),
(3, 4, 1, '2023-10-13', 50.00),
(4, 5, 2, '2023-10-14', 30.00),
(5, 6, 1, '2023-10-15', 30.00),
(6, 7, 1, '2023-10-16', 60.00),
(7, 8, 1, '2023-10-17', 80.00),
(8, 9, 1, '2023-10-18', 800.00),
(9, 10, 1, '2023-10-19', 400.00),
(10, 1, 1, '2023-10-20', 100.00);

-- Query 1: Best-selling product (product with max total quantity sold)
SELECT p.name, SUM(s.quantity) AS total_quantity
FROM Sales s
JOIN Products p ON s.product_id = p.id
GROUP BY p.id, p.name
ORDER BY total_quantity DESC
LIMIT 1;

-- Query 2: Total sales per product category
SELECT p.category, SUM(s.total_amount) AS total_sales
FROM Sales s
JOIN Products p ON s.product_id = p.id
GROUP BY p.category
ORDER BY total_sales DESC;

-- Query 3: Average purchase per customer
SELECT c.name, AVG(s.total_amount) AS avg_purchase
FROM Sales s
JOIN Customers c ON s.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY avg_purchase DESC;

-- Query 4: Daily sales trends (sum total_amount by date)
SELECT sale_date, SUM(total_amount) AS daily_sales
FROM Sales
GROUP BY sale_date
ORDER BY sale_date;

-- Query 5: Monthly sales trends (sum total_amount by month)
SELECT strftime('%Y-%m', sale_date) AS month, SUM(total_amount) AS monthly_sales
FROM Sales
GROUP BY month
ORDER BY month;
