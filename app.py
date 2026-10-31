from flask import Flask, render_template
from config import Config
from models import get_db
from routes.dashboard import dashboard_bp
from routes.products import products_bp
from routes.suppliers import suppliers_bp
from routes.transactions import transactions_bp
from routes.reports import reports_bp

app = Flask(__name__)
app.config.from_object(Config)

@app.context_processor
def inject_helpers():
    return {"app_name": "Inventory & Stock Analysis"}

@app.route("/")
def home():
    return dashboard_bp.view_functions["dashboard"]()

app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(suppliers_bp, url_prefix="/suppliers")
app.register_blueprint(transactions_bp, url_prefix="/transactions")
app.register_blueprint(reports_bp, url_prefix="/reports")

@app.errorhandler(404)
def not_found(error):
    return render_template("base.html", content_message="Page not found."), 404

if __name__ == "__main__":
    app.run(debug=True)
