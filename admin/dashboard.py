from . import admin_bp
from flask import render_template
from extensions import db
from models.product import Product
from models.order import Order
from models.category import Category
from models.user import User

@admin_bp.get('/')
@admin_bp.get('/dashboard')
def dashboard():
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0.0
    total_users = User.query.count()

    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    recent_products = Product.query.order_by(Product.id.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        total_products=total_products,
        total_orders=total_orders,
        total_revenue=total_revenue,
        total_users=total_users,
        recent_orders=recent_orders,
        recent_products=recent_products
    )
