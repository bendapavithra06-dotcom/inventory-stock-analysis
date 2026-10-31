# Inventory and Stock Analysis System

A Flask + MySQL project for product/supplier management, stock-in and stock-out recording, low-stock alerts, movement analysis and inventory valuation.

## Features
- Add and view products and suppliers.
- Record stock IN and stock OUT transactions.
- Opening stock plus transaction history determines current stock.
- Stock-out is rejected when it exceeds available stock.
- Transaction history is retained for audit/reconciliation.
- Pandas summaries, NumPy valuation calculations and Matplotlib charts.
- Dashboard, low-stock list, fast-moving product list and inventory report.

## Requirements
- Python 3.10+
- MySQL Server 8.0+
- Git (for GitHub upload)

## Setup
1. Open MySQL Workbench or MySQL Command Line.
2. Run `database/inventory_db.sql` to create the database and tables.
3. Open a terminal in this project folder.
4. Create and activate a virtual environment:

   Windows:
   ```bat
   py -m venv venv
   venv\\Scripts\\activate
   ```

   macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Set your MySQL connection settings. The defaults are host `localhost`, user `root`, blank password, database `inventory_db`. If your MySQL root account has a password, set environment variables in the terminal before running:

   Windows CMD:
   ```bat
   set MYSQL_PASSWORD=your_mysql_password
   ```

   PowerShell:
   ```powershell
   $env:MYSQL_PASSWORD="your_mysql_password"
   ```

   macOS/Linux:
   ```bash
   export MYSQL_PASSWORD="your_mysql_password"
   ```

7. Start the application:
   ```bash
   python app.py
   ```
8. Open `http://127.0.0.1:5000` in your browser.

## Suggested demo
1. Add a supplier.
2. Add a product with opening stock 20, reorder level 5 and unit cost 100.
3. Record Stock IN of 10.
4. Record Stock OUT of 7.
5. Check that current stock is 23 and estimated value is ₹2300.
6. Try recording Stock OUT of 24. The application should reject it.
7. Open Reports and Dashboard to view low-stock status and charts.

## Run tests
```bash
python -m unittest discover -s tests
```

## Notes
- This is an educational starter application, not a production deployment.
- It does not perform automatic purchasing.
- For production, add authentication, CSRF protection, role-based access, migrations, stronger validation and secure secret management.
- Product opening stock is the initial baseline. Later corrections should be recorded as stock IN or stock OUT transactions with a reason in Notes; do not edit transaction history directly.
