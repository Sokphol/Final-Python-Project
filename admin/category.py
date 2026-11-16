from . import admin_bp
from flask import current_app, render_template, request, redirect, url_for, flash
from extensions import db, execute_raw_sql
from models.category import Category
from services.upload_service import save_image
import re


def _slugify(value):
    value = (value or '').strip().lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-') or 'category'


@admin_bp.get('/category')
def category():
    categories = execute_raw_sql("select id,title,description,image_url,is_active,slug from category order by title ;")
    return render_template('admin/category/index.html', categories=categories)

@admin_bp.route('/category/add', methods=['GET', 'POST'])
def category_add():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Category title is required.', 'error')
            return render_template('admin/category/add.html')

        slug = request.form.get('slug', '').strip() or _slugify(title)
        if Category.query.filter(Category.slug == slug).first():
            flash('This slug is already used by another category.', 'error')
            return render_template('admin/category/add.html')

        try:
            cat = Category(
                title=title,
                description=request.form.get('description', '').strip(),
                slug=slug,
                is_active='is_active' in request.form,
            )

            image_file = request.files.get('image_url')
            if image_file and image_file.filename != '':
                cat.image_url = save_image(
                    image_file, current_app.config['UPLOAD_FOLDER']
                )['original_url']

            db.session.add(cat)
            db.session.commit()
            flash('Category added successfully!', 'success')
            return redirect(url_for('admin_bp.category'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding category: {e}', 'error')

    return render_template('admin/category/add.html')

@admin_bp.route('/category/edit/<int:id>', methods=['GET', 'POST'])
def category_edit(id):
    cat = Category.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Category title is required.', 'error')
            return render_template('admin/category/edit.html', c=cat)

        slug = request.form.get('slug', '').strip() or _slugify(title)
        duplicate_slug = Category.query.filter(Category.slug == slug, Category.id != id).first()
        if duplicate_slug:
            flash('This slug is already used by another category.', 'error')
            return render_template('admin/category/edit.html', c=cat)

        try:
            cat.title = title
            cat.description = request.form.get('description', '').strip()
            cat.slug = slug
            cat.is_active = 'is_active' in request.form

            image_file = request.files.get('image_url')
            if image_file and image_file.filename != '':
                cat.image_url = save_image(
                    image_file, current_app.config['UPLOAD_FOLDER']
                )['original_url']

            db.session.commit()
            flash('Category updated successfully!', 'success')
            return redirect(url_for('admin_bp.category'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating category: {e}', 'error')

    return render_template('admin/category/edit.html', c=cat)


@admin_bp.post('/category/delete/<int:id>')
def category_delete(id):
    cat = Category.query.get_or_404(id)
    try:
        db.session.delete(cat)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting category: {e}', 'error')
    return redirect(url_for('admin_bp.category'))
