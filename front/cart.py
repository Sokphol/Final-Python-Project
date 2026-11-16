from . import front_bp
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from models.product import Product

def get_cart():
    if 'cart' not in session or not isinstance(session['cart'], dict):
        session['cart'] = {}
    return session['cart']

@front_bp.get('/cart')
def cart():
    cart_data = get_cart()
    cart_items = []
    total_amount = 0.0

    # Ensure fresh product info from database
    for pro_id_str, item in list(cart_data.items()):
        try:
            p_id = int(pro_id_str)
            product = Product.query.get(p_id)
            if not product or product.status != 'Active':
                # Product no longer available
                continue
            
            qty = max(1, int(item.get('quantity', 1)))
            if qty > product.stock:
                qty = product.stock
                item['quantity'] = qty

            subtotal = product.price * qty
            total_amount += subtotal

            cart_items.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': product.image,
                'category': product.category.title if product.category else 'Watch',
                'quantity': qty,
                'stock': product.stock,
                'subtotal': subtotal
            })
        except (ValueError, TypeError):
            continue

    return render_template(
        'front/cart.html',
        cart_items=cart_items,
        total_amount=total_amount,
        shipping_fee=0.0  # Free shipping on watches!
    )


@front_bp.post('/cart/add')
def cart_add():
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)

    if not product_id or quantity <= 0:
        flash('Invalid product or quantity.', 'error')
        return redirect(request.referrer or url_for('front_bp.home'))

    product = Product.query.get(product_id)
    if not product or product.status != 'Active':
        flash('Product not found or unavailable.', 'error')
        return redirect(request.referrer or url_for('front_bp.home'))

    if product.stock <= 0:
        flash(f'Sorry, {product.name} is currently out of stock.', 'error')
        return redirect(request.referrer or url_for('front_bp.detail', id=product.id))

    cart = get_cart()
    pro_id_str = str(product.id)

    current_qty = cart.get(pro_id_str, {}).get('quantity', 0)
    new_qty = min(current_qty + quantity, product.stock)

    cart[pro_id_str] = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'image': product.image,
        'quantity': new_qty,
        'stock': product.stock
    }
    session['cart'] = cart
    session.modified = True

    flash(f'Added "{product.name}" to your cart.', 'success')

    # Return JSON if requested via AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        total_count = sum(item.get('quantity', 1) for item in cart.values())
        return jsonify({
            'success': True,
            'message': f'Added "{product.name}" to cart.',
            'cart_count': total_count
        })

    return redirect(request.form.get('next') or request.referrer or url_for('front_bp.cart'))


@front_bp.post('/cart/update')
def cart_update():
    product_id = request.form.get('product_id', type=int)
    action = request.form.get('action')
    quantity = request.form.get('quantity', type=int)

    cart = get_cart()
    pro_id_str = str(product_id)

    if pro_id_str in cart:
        product = Product.query.get(product_id)
        max_stock = product.stock if product else 99

        if action == 'increase':
            cart[pro_id_str]['quantity'] = min(cart[pro_id_str]['quantity'] + 1, max_stock)
        elif action == 'decrease':
            new_qty = cart[pro_id_str]['quantity'] - 1
            if new_qty <= 0:
                del cart[pro_id_str]
            else:
                cart[pro_id_str]['quantity'] = new_qty
        elif quantity is not None:
            if quantity <= 0:
                del cart[pro_id_str]
            else:
                cart[pro_id_str]['quantity'] = min(quantity, max_stock)

        session['cart'] = cart
        session.modified = True

    return redirect(url_for('front_bp.cart'))


@front_bp.post('/cart/remove/<int:id>')
def cart_remove(id):
    cart = get_cart()
    pro_id_str = str(id)
    if pro_id_str in cart:
        item_name = cart[pro_id_str].get('name', 'Item')
        del cart[pro_id_str]
        session['cart'] = cart
        session.modified = True
        flash(f'Removed "{item_name}" from cart.', 'info')

    return redirect(url_for('front_bp.cart'))


@front_bp.post('/cart/clear')
def cart_clear():
    session['cart'] = {}
    session.modified = True
    flash('Cart has been cleared.', 'info')
    return redirect(url_for('front_bp.cart'))
