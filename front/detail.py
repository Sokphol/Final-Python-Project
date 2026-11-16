from urllib.parse import quote
from . import front_bp
from flask import render_template, request, abort, redirect, url_for
from models.product import Product

@front_bp.route('/product/<int:id>')
@front_bp.route('/detail')
def detail(id=None):
    if id is None:
        pro_id = request.args.get('pro_id', type=int)
        if not pro_id:
            return abort(404)
        id = pro_id

    product = Product.query.get_or_404(id)

    current_url = request.base_url
    share_text = f"Check out {product.name} on Watch Shop!"
    facebook_share_url = f"https://www.facebook.com/sharer/sharer.php?u={quote(current_url)}"
    telegram_share_url = f"https://t.me/share/url?url={quote(current_url)}&text={quote(share_text)}"

    related_products = Product.query.filter(
        Product.id != product.id,
        Product.category_id == product.category_id
    ).limit(4).all()

    return render_template(
        'front/detail.html',
        product=product,
        current_url=current_url,
        facebook_share_url=facebook_share_url,
        telegram_share_url=telegram_share_url,
        related_products=related_products
    )
