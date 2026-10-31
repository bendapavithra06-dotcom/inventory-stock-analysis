from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.supplier import all_suppliers, add_supplier

suppliers_bp=Blueprint("suppliers",__name__)

@suppliers_bp.route("/")
def listing():
    return render_template("suppliers/list.html",suppliers=all_suppliers())

@suppliers_bp.route("/add",methods=["GET","POST"])
def add():
    if request.method=="POST":
        try:
            add_supplier(request.form)
            flash("Supplier added successfully.","success")
            return redirect(url_for("suppliers.listing"))
        except Exception as e:
            flash(f"Could not add supplier: {e}","danger")
    return render_template("suppliers/add.html")
