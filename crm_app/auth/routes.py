from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from crm_app import db
from crm_app.auth import auth_bp
from crm_app.models import User
from crm_app.forms import LoginForm, RegistrationForm

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Try to find user by email
            user = User.query.filter_by(email=form.email.data).first()

            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash('Login successful!', 'success')
                return redirect(next_page if next_page else url_for('main.dashboard'))
            else:
                flash('Login unsuccessful. Please check email and password.', 'danger')
        except Exception as e:
            flash(f'Database error: {str(e)}. Please make sure you have initialized the database with "flask init-db".', 'danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'danger')

    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))