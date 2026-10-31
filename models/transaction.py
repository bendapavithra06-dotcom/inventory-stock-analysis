from . import get_db

def all_transactions():
    db=get_db(); cur=db.cursor(dictionary=True)
    cur.execute("""SELECT t.*,p.product_name,s.supplier_name
        FROM stock_transactions t JOIN products p ON p.product_id=t.product_id
        LEFT JOIN suppliers s ON s.supplier_id=t.supplier_id
        ORDER BY t.transaction_date DESC,t.transaction_id DESC""")
    rows=cur.fetchall(); cur.close(); db.close(); return rows
