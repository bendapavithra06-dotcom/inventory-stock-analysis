from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.product import all_products
from models.supplier import all_suppliers
from models.transaction import all_transactions
from services.inventory_service import record_transaction, InventoryError

transactions_bp=Blueprint("transactions",__name__)

@transactions_bp.route("/")
def listing():
    return render_template("transactions/list.html",transactions=all_transactions())

@transactions_bp.route("/add",methods=["GET","POST"])
def add():
    if request.method=="POST":
        try:
            record_transaction(request.form["product_id"],request.form["transaction_type"],
                               request.form["quantity"],request.form.get("supplier_id"),
                               request.form.get("notes"))
            flash("Stock movement recorded.","success")
            return redirect(url_for("transactions.listing"))
        except (InventoryError,ValueError,KeyError) as e:
            flash(str(e),"danger")
        except Exception as e:
            flash(f"Could not record transaction: {e}","danger")
    return render_template("transactions/add.html",products=all_products(),
                           suppliers=all_suppliers())
