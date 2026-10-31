from . import get_db

def all_products():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT p.*,
        p.opening_stock + COALESCE(SUM(
          CASE WHEN t.transaction_type='IN' THEN t.quantity
               WHEN t.transaction_type='OUT' THEN -t.quantity ELSE 0 END
        ),0) AS current_stock
        FROM products p LEFT JOIN stock_transactions t ON p.product_id=t.product_id
        GROUP BY p.product_id ORDER BY p.product_name
    """)
    rows = cur.fetchall()
    cur.close(); db.close()
    return rows

def add_product(data):
    db = get_db(); cur = db.cursor()
    cur.execute("""INSERT INTO products
        (sku, product_name, category, opening_stock, reorder_level, unit_cost)
        VALUES (%s,%s,%s,%s,%s,%s)""",
        (data["sku"], data["product_name"], data.get("category") or None,
         int(data["opening_stock"]), int(data["reorder_level"]), float(data["unit_cost"])))
    db.commit(); cur.close(); db.close()
