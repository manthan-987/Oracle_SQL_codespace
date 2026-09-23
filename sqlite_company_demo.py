import sqlite3

# Step 1: Connect to SQLite database (creates it if it doesn't exist)
print("Step 1: Connecting to SQLite database...")
connection = sqlite3.connect('company.db')
cursor = connection.cursor()
print("✓ Connected to company.db\n")

# Step 2: Drop existing tables if they exist (to avoid conflicts with previous data)
print("Step 2: Dropping existing tables...")
cursor.execute('DROP TABLE IF EXISTS employee')
cursor.execute('DROP TABLE IF EXISTS department')
print("✓ Existing tables dropped\n")

# Step 3: Create the department table
print("Step 3: Creating department table...")
cursor.execute('''
    CREATE TABLE department (
        id INTEGER PRIMARY KEY,
        name TEXT,
        location TEXT
    )
''')
print("✓ Department table created\n")

# Step 4: Create the employee table
print("Step 4: Creating employee table...")
cursor.execute('''
    CREATE TABLE employee (
        id INTEGER PRIMARY KEY,
        name TEXT,
        deptid INTEGER
    )
''')
print("✓ Employee table created\n")

# Step 5: Insert 5 dummy records into the department table
print("Step 5: Inserting department records...")
departments = [
    (1, 'Sales', 'Mumbai'),
    (2, 'HR', 'Bangalore'),
    (3, 'IT', 'Pune'),
    (4, 'Finance', 'Delhi'),
    (5, 'Marketing', 'Hyderabad')
]
cursor.executemany('INSERT INTO department VALUES (?, ?, ?)', departments)
print("✓ 5 department records inserted\n")

# Step 6: Insert 5 dummy records into the employee table
# Note: This data is designed to demonstrate different JOIN types:
#   - Employees with deptid 1, 2, 3, 4 have matching departments (INNER JOIN will show these)
#   - Employee with deptid 10 has NO matching department (LEFT JOIN will show this with NULLs)
#   - Department with id 5 (Marketing) has NO employees (RIGHT JOIN will show this with NULLs)
print("Step 6: Inserting employee records...")
employees = [
    (1, 'Raj Kumar', 1),           # Belongs to Sales (exists)
    (2, 'Priya Singh', 2),         # Belongs to HR (exists)
    (3, 'Anil Patel', 10),         # Belongs to department 10 (does NOT exist)
    (4, 'Maya Sharma', 3),         # Belongs to IT (exists)
    (5, 'Vikram Gupta', 4)         # Belongs to Finance (exists)
]
cursor.executemany('INSERT INTO employee VALUES (?, ?, ?)', employees)
print("✓ 5 employee records inserted\n")

# Step 7: Commit the changes to the database
print("Step 7: Committing changes to database...")
connection.commit()
print("✓ Changes committed\n")

# Step 8: Fetch and display all employees
print("=" * 50)
print("DISPLAYING ALL EMPLOYEES")
print("=" * 50)
print("ID | Name              | DeptID")
print("-" * 50)

cursor.execute('SELECT * FROM employee')
employees_data = cursor.fetchall()

for employee in employees_data:
    emp_id, emp_name, dept_id = employee
    print(f"{emp_id}  | {emp_name:17} | {dept_id}")

print()

# Step 9: Fetch and display all departments
print("=" * 50)
print("DISPLAYING ALL DEPARTMENTS")
print("=" * 50)
print("ID | Name              | Location")
print("-" * 50)

cursor.execute('SELECT * FROM department')
departments_data = cursor.fetchall()

for department in departments_data:
    dept_id, dept_name, location = department
    print(f"{dept_id}  | {dept_name:17} | {location}")

print()

# Step 10: Fetch and display employees in the HR department
# This demonstrates a JOIN between employee and department tables
print("=" * 50)
print("EMPLOYEES IN HR DEPARTMENT")
print("=" * 50)
print("Employee Name")
print("-" * 50)

cursor.execute('''
    SELECT e.name FROM employee e
    JOIN department d ON e.deptid = d.id
    WHERE d.name = 'HR'
''')
hr_employees = cursor.fetchall()

if hr_employees:
    for employee in hr_employees:
        print(f"{employee[0]}")
else:
    print("No employees found in HR department")

print()

# Step 11: Summary for JOIN demonstration
print("=" * 50)
print("NOTES FOR JOIN DEMONSTRATION")
print("=" * 50)
print("✓ INNER JOIN:   Will show 4 employees (those with matching departments)")
print("✓ LEFT JOIN:    Will show all 5 employees (including Anil with NULL dept)")
print("✓ RIGHT JOIN:   Will show all 5 departments (including Marketing with NULL employees)")
print()

# Step 12: Close the cursor and database connection
print("Step 12: Closing database connection...")
cursor.close()
connection.close()
print("✓ Connection closed\n")

print("Script completed successfully!")
