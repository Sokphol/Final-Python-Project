from . import admin_bp
from flask import render_template, request, redirect, url_for, flash
from extensions import db
from models.order import Order

@admin_bp.get('/orders')
def order_list():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/order/index.html', orders=orders)


@admin_bp.get('/orders/<int:id>')
def order_detail(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/order/detail.html', order=order)


@admin_bp.post('/orders/<int:id>/status')
def order_update_status(id):
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ['Pending', 'Confirmed', 'Processing', 'Delivered', 'Cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order.order_number} status updated to {new_status}.', 'success')
    return redirect(url_for('admin_bp.order_detail', id=order.id))
