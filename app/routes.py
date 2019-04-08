from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from PIL import Image

from app import app, bcrypt, db, mail
from app.models import User, Trip
from app.forms import (RegistrationForm, LoginForm, UpdateAccountForm, CreateTripForm,
                        ResetPasswordForm, RequestResetForm)
from flask_mail import Message


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    trips = Trip.query.order_by(Trip.date_created.desc()).paginate(page=page, per_page=5)
    # users = User.query.filter(User.trips_joined.any(id=4)).all()
    return render_template('home.html', trips=trips)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can now login.', 'success')
        return redirect(url_for('login'))
    else:
        flash('Account not created! Please check your input.', 'danger')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/travelers')
def travelers():
    users = User.query.all()
    return render_template('travelers.html', users=users, title='Travelers')


@app.route('/new_trip', methods=['POST', 'GET'])
@login_required
def new_trip():
    form = CreateTripForm()
    if form.validate_on_submit():
        trip = Trip(location=form.location.data, user_id=current_user.id, details=form.details.data)
        db.session.add(trip)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_trip.html', form=form, title='New Trip')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size= (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', form=form, image_file=image_file)


@app.route("/show_trip/<int:trip_id>")
def show_trip(trip_id):
    selected_trip = Trip.query.get_or_404(trip_id)
    return render_template('show_trip.html', title=selected_trip.location, trip=selected_trip)


@app.route("/user/<int:id>", methods=["POST", "GET"])
def user_trips(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=id).first_or_404()
    trips = Trip.query.filter_by(user_id=id).order_by(Trip.date_created.desc()).paginate(page=page, per_page=2)
    return render_template('user_trips.html', user=user, trips=trips)


@app.route('/add/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def add_traveler(trip_id):
    selected_trip = Trip.query.get_or_404(trip_id)
    current_user.trips_joined.append(selected_trip)
    db.session.add(current_user)
    db.session.commit()
    flash(f'Prijavili ste se na putovanje! trip.id="{trip_id}"')
    return redirect(url_for('home'))


@app.route('/remove/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def remove_traveler(trip_id):
    selected_trip = Trip.query.get_or_404(trip_id)
    current_user.trips_joined.remove(selected_trip)
    db.session.add(current_user)
    db.session.commit()
    flash(f'>Odjavili ste se sa putovanja! trip.id="{trip_id}"')
    return redirect(url_for('home'))


@app.route("/update/<int:trip>", methods=["POST", "GET"])
@login_required
def update_trip(trip):
    selected_trip = Trip.query.get_or_404(trip)
    if selected_trip.author != current_user:
        abort(403)
    form = CreateTripForm()
    if form.validate_on_submit():
        selected_trip.location = form.location.data
        # selected_trip.transport = form.transport.data
        # selected_trip.spaces_available = form.spaces.data
        # selected_trip.start_date = form.start_date.data
        # selected_trip.price = form.price.data
        # selected_trip.trip_duration = form.trip_duration.data
        selected_trip.details = form.details.data
        db.session.commit()
        flash('Vas trip je update-an!')
        return redirect(url_for('home', trip=selected_trip.id))
    elif request.method == 'GET':
        form.location.data = selected_trip.location
        # form.transport.data = selected_trip.transport
        # form.spaces.data = selected_trip.spaces_available
        # form.start_date.data = selected_trip.start_date
        # form.price.data = selected_trip.price
        # form.trip_duration.data = selected_trip.trip_duration
        form.details.data = selected_trip.details

    return render_template('new_trip.html', title='Update Trip', form=form,
                           trip=selected_trip, legend='Update Trip')


@app.route('/delete/<int:trip>', methods=['GET','POST'])
@login_required
def delete_trip(trip):
    selected_trip = Trip.query.get_or_404(trip)
    if selected_trip.author != current_user:
        abort(403)
    db.session.delete(selected_trip)
    db.session.commit()
    flash(f'>Izbrisali ste vas izlet!')
    return redirect(url_for('home'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Passsowrd Reset Request', sender='trippinapplication@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password visit the folowing link:
    { url_for('reset_token', token=token, _external=True) }
    
If you did not make this request than simply ignore this email and no changes will be made.

    '''
    mail.send(msg)


@app.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated. You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)





