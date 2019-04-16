from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from app import bcrypt, db
from app.models import User, Trip
from app.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             ResetPasswordForm, RequestResetForm)
from app.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)


@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    full_name=form.full_name.data,username=form.username.data, email=form.email.data,
                    address=form.address.data, country=form.country.data, phone_number=form.phone_number.data,
                    gender=form.gender.data, birth_date=form.birth_date.data, about_me=form.about_me.data,
                    password=hashed_password, )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can now login.', 'success')
        return redirect(url_for('users.login'))
    else:
        flash('Account not created! Please check your input.', 'danger')
    return render_template('register2.html', title='Register', form=form)


@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login2.html', title='Login', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.country = form.country.data
        current_user.phone_number = form.phone_number.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.country.data = current_user.country
        form.phone_number.data = current_user.phone_number
        form.about_me.data = current_user.about_me
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account2.html', form=form, image_file=image_file)


@users.route("/user/<int:id>", methods=["POST", "GET"])
def user_trips(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=id).first_or_404()
    trips = Trip.query.filter_by(user_id=id).order_by(Trip.date_created.desc()).paginate(page=page, per_page=2)
    return render_template('user_trips2.html', user=user, trips=trips)


@users.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated. You can now login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/add/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def add_traveler(trip_id):
    selected_trip = Trip.query.get_or_404(trip_id)
    count = 0
    for user in selected_trip.users:
        count+=1
    if count == selected_trip.people_number:
        flash("Not enough space in trip! Try again later.")
        return redirect(url_for('main.home'))
    current_user.trips_joined.append(selected_trip)
    db.session.add(current_user)
    db.session.commit()
    flash(f'Prijavili ste se na putovanje! trip.id="{trip_id}"')
    return redirect(url_for('main.home'))


@users.route('/remove/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def remove_traveler(trip_id):
    selected_trip = Trip.query.get_or_404(trip_id)
    current_user.trips_joined.remove(selected_trip)
    db.session.add(current_user)
    db.session.commit()
    flash(f'>Odjavili ste se sa putovanja! trip.id="{trip_id}"')
    return redirect(url_for('main.home'))


@users.route('/travelers')
def travelers():
    users = User.query.all()
    return render_template('travelers.html', users=users, title='Travelers')


