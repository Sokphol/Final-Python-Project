import uuid
from datetime import datetime
from . import front_bp
from flask import render_template, request, redirect, url_for, session, flash, abort
from extensions import db
from models.product import Product
from models.order import Order, OrderItem
from services.khqr_service import generate_khqr_qr_code

@front_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_data = session.get('cart', {})
    if not cart_data:
        flash('Your cart is empty. Please add items before checking out.', 'info')
        return redirect(url_for('front_bp.home'))

    # Load items and calculate total
    cart_items = []
    total_amount = 0.0

    for pro_id_str, item in list(cart_data.items()):
        try:
            product = Product.query.get(int(pro_id_str))
            if not product or product.status != 'Active':
                continue
            qty = max(1, int(item.get('quantity', 1)))
            subtotal = product.price * qty
            total_amount += subtotal
            cart_items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal
            })
        except (ValueError, TypeError):
            continue

    if not cart_items:
        flash('No valid products in your cart.', 'error')
        return redirect(url_for('front_bp.home'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()

        if not full_name or not email or not phone or not shipping_address:
            flash('Please fill in all required customer details.', 'error')
            qr_image = generate_khqr_qr_code(total_amount, merchant_name="WATCH SHOP")
            return render_template(
                'front/checkout.html',
                cart_items=cart_items,
                total_amount=total_amount,
                qr_image=qr_image,
                form=request.form
            )

        try:
            # Generate unique order number
            order_number = f"WS-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

            new_order = Order(
                order_number=order_number,
                customer_name=full_name,
                customer_email=email,
                customer_phone=phone,
                shipping_address=shipping_address,
                total_amount=total_amount,
                payment_method='KHQR',
                payment_status='Paid',
                status='Confirmed'
            )
            db.session.add(new_order)
            db.session.flush()

            # Create order items and update stock
            for item_info in cart_items:
                product = item_info['product']
                qty = item_info['quantity']

                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=product.id,
                    product_name=product.name,
                    product_image=product.image,
                    price=product.price,
                    quantity=qty,
                    subtotal=item_info['subtotal']
                )
                db.session.add(order_item)

                # Reduce stock
                product.stock = max(0, product.stock - qty)

            db.session.commit()

            # Clear cart
            session['cart'] = {}
            session.modified = True

            flash('Order placed successfully via KHQR payment!', 'success')
            return redirect(url_for('front_bp.order_confirmation', id=new_order.id))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while placing your order: {e}', 'error')

    # Generate KHQR QR Code for display
    qr_image = generate_khqr_qr_code(total_amount, merchant_name="WATCH SHOP")

    return render_template(
        'front/checkout.html',
        cart_items=cart_items,
        total_amount=total_amount,
        qr_image=qr_image,
        form={}
    )


@front_bp.get('/order/confirmation/<int:id>')
def order_confirmation(id):
    order = Order.query.get_or_404(id)
    return render_template('front/confirmation.html', order=order)
