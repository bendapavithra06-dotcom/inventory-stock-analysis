import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from models import get_db

def inventory_data():
    db=get_db()
    query="""SELECT p.product_id,p.sku,p.product_name,p.category,p.opening_stock,
        p.reorder_level,p.unit_cost,
        COALESCE(SUM(CASE WHEN t.transaction_type='IN' THEN t.quantity
                          WHEN t.transaction_type='OUT' THEN -t.quantity ELSE 0 END),0) AS net_movement,
        COALESCE(SUM(CASE WHEN t.transaction_type='IN' THEN t.quantity ELSE 0 END),0) AS total_in,
        COALESCE(SUM(CASE WHEN t.transaction_type='OUT' THEN t.quantity ELSE 0 END),0) AS total_out
        FROM products p LEFT JOIN stock_transactions t ON p.product_id=t.product_id
        GROUP BY p.product_id ORDER BY p.product_name"""
    df=pd.read_sql(query,db); db.close()
    if df.empty:
        return df
    df["current_stock"] = df["opening_stock"].to_numpy(dtype=int) + df["net_movement"].to_numpy(dtype=int)
    df["stock_value"] = np.round(df["current_stock"].to_numpy(dtype=float) *
                                 df["unit_cost"].to_numpy(dtype=float), 2)
    df["low_stock"] = df["current_stock"] <= df["reorder_level"]
    return df

def movement_data():
    db=get_db()
    df=pd.read_sql("""SELECT p.product_name,t.transaction_type,
        SUM(t.quantity) AS quantity
        FROM stock_transactions t JOIN products p ON p.product_id=t.product_id
        GROUP BY p.product_id,p.product_name,t.transaction_type
        ORDER BY p.product_name""",db)
    db.close()
    return df

def create_charts():
    os.makedirs("static/charts",exist_ok=True)
    stock=inventory_data()
    movement=movement_data()
    if not stock.empty:
        plt.figure(figsize=(9,4))
        plt.bar(stock["product_name"],stock["current_stock"])
        plt.xticks(rotation=35,ha="right")
        plt.ylabel("Units"); plt.title("Current Stock by Product")
        plt.tight_layout(); plt.savefig("static/charts/stock_levels.png"); plt.close()
    if not movement.empty:
        pivot=movement.pivot_table(index="product_name",columns="transaction_type",
                                   values="quantity",aggfunc="sum",fill_value=0)
        pivot.plot(kind="bar",figsize=(9,4))
        plt.ylabel("Units"); plt.title("Stock In vs Stock Out")
        plt.xticks(rotation=35,ha="right"); plt.tight_layout()
        plt.savefig("static/charts/product_movement.png"); plt.close()
    return stock, movement
