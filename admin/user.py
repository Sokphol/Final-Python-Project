from . import admin_bp
from flask import current_app, render_template, request, redirect, url_for, flash
from extensions import db, execute_raw_sql
from services.upload_service import save_image
from werkzeug.security import generate_password_hash


@admin_bp.get('/user')
def user():
    users = execute_raw_sql("""
    SELECT id,user_name,first_name,last_name,email
    ,phone,address,password,role,profile_image,is_active FROM "user" ORDER BY user_name DESC
    """)
    return render_template('admin/user/index.html', users=users)
@admin_bp.route('/user/add', methods=['GET', 'POST'])
def user_add():
    if request.method == 'POST':
        user_name = request.form.get('user_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not user_name or not email or not password:
            flash('Username, email, and password are required.', 'error')
            return render_template('admin/user/add.html')

        duplicate_user = execute_raw_sql(
            'SELECT id FROM "user" WHERE user_name = :user_name OR email = :email LIMIT 1',
            {'user_name': user_name, 'email': email},
        )
        if duplicate_user:
            flash('This username or email is already in use.', 'error')
            return render_template('admin/user/add.html')

        try:
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            phone = request.form.get('phone', '').strip()
            address = request.form.get('address', '').strip()
            role = request.form.get('role', 'user')
            is_active = 'is_active' in request.form

            profile_image = None
            image_file = request.files.get('profile_image')
            if image_file and image_file.filename != '':
                profile_image = save_image(
                    image_file, current_app.config['UPLOAD_FOLDER']
                )['original_url']

            sql = """
                INSERT INTO "user" (user_name, first_name, last_name, email, phone,
                                    address, password, role, profile_image, is_active)
                VALUES (:user_name, :first_name, :last_name, :email, :phone,
                        :address, :password, :role, :profile_image, :is_active)
            """
            params = {
                "user_name": user_name,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "address": address,
                "password": generate_password_hash(password),
                "role": role,
                "profile_image": profile_image,
                "is_active": is_active,
            }
            execute_raw_sql(sql, params, fetch=False)

            flash('User added successfully!', 'success')
            return redirect(url_for('admin_bp.user'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding user: {e}', 'error')
    return render_template('admin/user/add.html')


@admin_bp.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def user_edit(id):
    user_rows = execute_raw_sql(
        """SELECT id, user_name, first_name, last_name, email, phone, address,
               password, role, profile_image, is_active FROM \"user\" WHERE id = :id""",
        {"id": id}
    )
    u = user_rows[0] if user_rows else None
    if not u:
        flash('User not found.', 'error')
        return redirect(url_for('admin_bp.user'))

    if request.method == 'POST':
        user_name = request.form.get('user_name', '').strip()
        email = request.form.get('email', '').strip()
        if not user_name or not email:
            flash('Username and email are required.', 'error')
            return render_template('admin/user/edit.html', u=u)

        duplicate_user = execute_raw_sql(
            'SELECT id FROM "user" WHERE (user_name = :user_name OR email = :email) AND id != :id LIMIT 1',
            {'user_name': user_name, 'email': email, 'id': id},
        )
        if duplicate_user:
            flash('This username or email is already used by another account.', 'error')
            return render_template('admin/user/edit.html', u=u)

        try:
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            phone = request.form.get('phone', '').strip()
            address = request.form.get('address', '').strip()
            role = request.form.get('role', 'user')
            is_active = 'is_active' in request.form
            password = request.form.get('password', '').strip()

            profile_image = None
            image_file = request.files.get('profile_image')
            if image_file and image_file.filename != '':
                profile_image = save_image(
                    image_file, current_app.config['UPLOAD_FOLDER']
                )['original_url']

            set_clauses = [
                "user_name = :user_name",
                "first_name = :first_name",
                "last_name = :last_name",
                "email = :email",
                "phone = :phone",
                "address = :address",
                "role = :role",
                "is_active = :is_active",
            ]
            params = {
                "id": id,
                "user_name": user_name,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "address": address,
                "role": role,
                "is_active": is_active,
            }
            if password:
                set_clauses.append("password = :password")
                params["password"] = generate_password_hash(password)
            if profile_image is not None:
                set_clauses.append("profile_image = :profile_image")
                params["profile_image"] = profile_image

            sql = f"""UPDATE "user" SET {', '.join(set_clauses)} WHERE id = :id"""
            execute_raw_sql(sql, params, fetch=False)

            flash('User updated successfully!', 'success')
            return redirect(url_for('admin_bp.user'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {e}', 'error')

    return render_template('admin/user/edit.html', u=u)


@admin_bp.post('/user/delete/<int:id>')
def user_delete(id):
    try:
        sql = 'DELETE FROM "user" WHERE id = :id'
        execute_raw_sql(sql, {"id": id}, fetch=False)
        flash('User deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting user: {e}', 'error')
    return redirect(url_for('admin_bp.user'))
