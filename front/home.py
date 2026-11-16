from . import front_bp
from flask import render_template, request
from models.product import Product
from models.category import Category

@front_bp.get('/')
def home():
    category_id = request.args.get('category', type=int)
    search_query = request.args.get('q', '').strip()

    query = Product.query
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))

    products = query.order_by(Product.id.desc()).all()
    categories = Category.query.filter_by(is_active=True).all()
    return render_template(
        'front/home.html',
        products=products,
        categories=categories,
        current_category=category_id,
        search_query=search_query
    )
