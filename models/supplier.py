from . import get_db

def all_suppliers():
    db=get_db(); cur=db.cursor(dictionary=True)
    cur.execute("SELECT * FROM suppliers ORDER BY supplier_name")
    rows=cur.fetchall(); cur.close(); db.close(); return rows

def add_supplier(data):
    db=get_db(); cur=db.cursor()
    cur.execute("INSERT INTO suppliers(supplier_name,phone,email) VALUES(%s,%s,%s)",
                (data["supplier_name"],data.get("phone"),data.get("email")))
    db.commit(); cur.close(); db.close()
