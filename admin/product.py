from . import admin_bp
from flask import current_app, render_template, request, redirect, url_for, flash
from flask_login import current_user
from extensions import db
from models.product import Product
from models.category import Category
from models.user import User
from services.upload_service import save_image

@admin_bp.get('/product')
def product():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template(
        'admin/product/index.html',
        products=products
    )

@admin_bp.route('/product/add', methods=['GET', 'POST'])
def product_add():
    categories = Category.query.order_by(Category.title).all()
    users = User.query.order_by(User.user_name).all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'Active')
        image_url = request.form.get('image_url', '').strip()

        if not name:
            flash('Product name is required.', 'error')
            return render_template('admin/product/add.html', categories=categories, users=users)

        try:
            price = float(request.form.get('price', 0) or 0)
            stock = int(request.form.get('stock', 0) or 0)
            rating = float(request.form.get('rating', 5.0) or 5.0)
            category_id = int(request.form.get('category_id') or 0)
            user_id = int(request.form.get('user_id') or 0) or current_user.id
        except (TypeError, ValueError):
            flash('Please enter valid numeric values for price and stock.', 'error')
            return render_template('admin/product/add.html', categories=categories, users=users)

        if category_id <= 0:
            category_id = categories[0].id if categories else None

        try:
            prod = Product(
                name=name,
                price=price,
                stock=stock,
                status=status,
                description=description,
                rating=rating,
                category_id=category_id,
                user_id=user_id,
            )

            # Check file upload or URL
            image_file = request.files.get('image')
            if image_file and image_file.filename != '':
                prod.image = save_image(
                    image_file, current_app.config['UPLOAD_FOLDER']
                )['original_url']
            elif image_url:
                prod.image = image_url

            db.session.add(prod)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('admin_bp.product'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding product: {e}', 'error')

    return render_template('admin/product/add.html', categories=categories, users=users)


@admin_bp.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def product_edit(id):
    prod = Product.query.get_or_404(id)
    categories = Category.query.order_by(Category.title).all()
    users = User.query.order_by(User.user_name).all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'Active')
        image_url = request.form.get('image_url', '').strip()

        if not name:
            flash('Product name is required.', 'error')
            return render_template('admin/product/edit.html', p=prod, categories=categories, users=users)

        try:
            price = float(request.form.get('price', 0) or 0)
            stock = int(request.form.get('stock', 0) or 0)
            rating = float(request.form.get('rating', 5.0) or 5.0)
            category_id = int(request.form.get('category_id') or 0)
            user_id = int(request.form.get('user_id') or 0) or current_user.id
        except (TypeError, ValueError):
            flash('Please enter valid numeric values for price and stock.', 'error')
            return render_template('admin/product/edit.html', p=prod, categories=categories, users=users)

        if category_id <= 0:
            category_id = prod.category_id

        try:
            prod.name = name
            prod.price = price
            prod.stock = stock
            prod.status = status
            prod.description = description
            prod.rating = rating
            prod.category_id = category_id
            prod.user_id = user_id

            image_file = request.files.get('image')
            if image_file and image_file.filename != '':
                prod.image = save_image(
                    image_file, current_app.config['UPLOAD_FOLDER']
                )['original_url']
            elif image_url:
                prod.image = image_url

            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('admin_bp.product'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product: {e}', 'error')

    return render_template('admin/product/edit.html', p=prod, categories=categories, users=users)


@admin_bp.post('/product/delete/<int:id>')
def product_delete(id):
    prod = Product.query.get_or_404(id)
    try:
        db.session.delete(prod)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {e}', 'error')
    return redirect(url_for('admin_bp.product'))
