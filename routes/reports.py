from flask import Blueprint, render_template
from services.analysis_service import inventory_data, movement_data

reports_bp=Blueprint("reports",__name__)

@reports_bp.route("/")
def report():
    stock=inventory_data()
    movement=movement_data()
    products=stock.to_dict("records") if not stock.empty else []
    total_value=float(stock["stock_value"].sum()) if not stock.empty else 0
    fast=stock.sort_values("total_out",ascending=False).head(5).to_dict("records") if not stock.empty else []
    return render_template("reports/inventory_report.html",products=products,
                           movement=movement.to_dict("records"),total_value=total_value,
                           fast_products=fast)
