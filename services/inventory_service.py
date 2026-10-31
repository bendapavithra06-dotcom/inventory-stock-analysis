from models import get_db

class InventoryError(Exception):
    pass

def record_transaction(product_id, kind, quantity, supplier_id=None, notes=None):
    quantity = int(quantity)
    if quantity <= 0:
        raise InventoryError("Quantity must be greater than zero.")
    if kind not in ("IN", "OUT"):
        raise InventoryError("Transaction type must be IN or OUT.")

    db = get_db()
    try:
        cur = db.cursor(dictionary=True)
        db.start_transaction()
        cur.execute("SELECT product_id, opening_stock FROM products WHERE product_id=%s FOR UPDATE",
                    (product_id,))
        product = cur.fetchone()
        if not product:
            raise InventoryError("Selected product does not exist.")

        cur.execute("""SELECT COALESCE(SUM(
            CASE WHEN transaction_type='IN' THEN quantity ELSE -quantity END
            ),0) AS movement
            FROM stock_transactions WHERE product_id=%s""", (product_id,))
        current_stock = int(product["opening_stock"]) + int(cur.fetchone()["movement"])
        if kind == "OUT" and quantity > current_stock:
            raise InventoryError(f"Insufficient stock. Current available stock: {current_stock}.")

        cur.execute("""INSERT INTO stock_transactions
            (product_id, transaction_type, quantity, supplier_id, notes)
            VALUES (%s,%s,%s,%s,%s)""",
            (product_id, kind, quantity, supplier_id or None, notes or None))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
