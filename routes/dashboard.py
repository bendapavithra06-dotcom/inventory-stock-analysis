from flask import Blueprint, render_template
from services.analysis_service import create_charts

dashboard_bp=Blueprint("dashboard",__name__)

@dashboard_bp.route("/")
def dashboard():
    stock,movement=create_charts()
    if stock.empty:
        stats={"products":0,"units":0,"low":0,"value":0}
        low=[]
    else:
        stats={"products":int(len(stock)),"units":int(stock.current_stock.sum()),
               "low":int(stock.low_stock.sum()),"value":float(stock.stock_value.sum())}
        low=stock[stock.low_stock].to_dict("records")
    return render_template("dashboard.html",stats=stats,low_products=low,
                           stock_chart="stock_levels.png",movement_chart="product_movement.png")
