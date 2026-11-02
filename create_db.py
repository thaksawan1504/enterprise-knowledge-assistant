import sqlite3

conn = sqlite3.connect("employees.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
)
""")

cursor.execute("DELETE FROM employees")

cursor.execute("""
INSERT INTO employees
(name, department, salary)
VALUES
('Rahul', 'IT', 50000)
""")

cursor.execute("""
INSERT INTO employees
(name, department, salary)
VALUES
('Amit', 'HR', 45000)
""")

cursor.execute("""
INSERT INTO employees
(name, department, salary)
VALUES
('Neha', 'Finance', 60000)
""")

conn.commit()
conn.close()

print("Database Created Successfully")