from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.product import all_products, add_product

products_bp=Blueprint("products",__name__)

@products_bp.route("/")
def listing():
    return render_template("products/list.html",products=all_products())

@products_bp.route("/add",methods=["GET","POST"])
def add():
    if request.method=="POST":
        try:
            add_product(request.form)
            flash("Product added successfully.","success")
            return redirect(url_for("products.listing"))
        except Exception as e:
            flash(f"Could not add product: {e}","danger")
    return render_template("products/add.html")
