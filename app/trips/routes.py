from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from datetime import datetime, timedelta

from app import db, bcrypt
from app.models import Trip, User, Comment, Event
from app.trips.forms import CreateTripForm
from app.users.utils import save_picture_trip, trip_is_full
from app.trips.forms import CommentTripForm

trips = Blueprint('trips', __name__)


@trips.route('/new_trip', methods=['POST', 'GET'])
@login_required
def new_trip():
    form = CreateTripForm()

    if form.validate_on_submit():
        if form.starting_at.data < (datetime.today() + timedelta(days=3)):
            flash('Izlet može početi najranije za 3 dana.', 'danger')
            return redirect(url_for('trips.new_trip'))

        if form.is_private.data:
            hashed_password = bcrypt.generate_password_hash(form.trip_password.data).decode('utf-8')
            picture_file = 'trip_default.jpg'
            if form.trip_picture.data:
                picture_file = save_picture_trip(form.trip_picture.data)
            trip = Trip(name=form.name.data, location=form.location.data, user_id=current_user.id, price=form.price.data,
                        people_number=form.people_number.data, starting_at=form.starting_at.data,
                        transport_type=form.transport_type.data, trip_duration=form.trip_duration.data,
                        is_private=form.is_private.data, trip_password=hashed_password,
                        details=form.details.data, image_file=picture_file)
        else:
            picture_file = 'trip_default.jpg'
            if form.trip_picture.data:
                picture_file = save_picture_trip(form.trip_picture.data)
            trip = Trip(name=form.name.data, location=form.location.data, user_id=current_user.id,
                        price=form.price.data, people_number=form.people_number.data, starting_at=form.starting_at.data,
                        transport_type=form.transport_type.data, trip_duration=form.trip_duration.data,
                        is_private=form.is_private.data, details=form.details.data, image_file=picture_file)

        try:
            db.session.add(trip)
            db.session.commit()

            trip = Trip.query.filter_by(name=form.name.data).first()
            event = Event(name=form.name.data, event="is_full", trip_id=trip.id)
            event2 = Event(name=form.name.data, event="starting_soon", trip_id=trip.id)
            db.session.add(event)
            db.session.add(event2)
            db.session.commit()

            flash('Vaš izlet je uspješno stvoren!', 'success')
            return redirect(url_for('main.home'))
        except:
            flash("Greška prilikom stvaranja izleta. Provjerite Vaš unos. Za korisniču podršku nam se obratite "
                  "na email -- trippinapplication@gmail.com -- .", "danger")

    return render_template('new_trip2.html', form=form, title='New Trip')


@trips.route("/show_trip/<int:trip_id>", methods=['POST', 'GET'])
@login_required
def show_trip(trip_id):
    selected_trip = Trip.query.get_or_404(trip_id)
    comments = Comment.query.order_by(Comment.date_created.desc()).filter_by(trip_id = selected_trip.id)
    users = User.query.filter(User.trips_joined.any(id=trip_id)).all()

    form = CommentTripForm()
    if form.validate_on_submit():
        comment = Comment(user_id=current_user.id, trip_id=trip_id, content=form.content.data)
        try:
            db.session.add(comment)
            db.session.commit()

            flash('Vaš komentar je uspješno objavljen!', 'success')
            return redirect(url_for('trips.show_trip', trip_id=selected_trip.id))
        except:
            flash("Greška prilikom stvaranja komentara. Provjerite Vaš unos. Za korisniču podršku nam se obratite "
                  "na email -- trippinapplication@gmail.com -- .", "danger")


    counter = 0
    for user in selected_trip.users:
        counter+=1                      # broj korisnika prijavljenih na izlet

    return render_template('show_trip2.html', title=selected_trip.location, trip=selected_trip,
                           users=users, counter=counter, form=form, comments=comments)


@trips.route("/update/<int:trip>", methods=["POST", "GET"])
@login_required
def update_trip(trip):
    selected_trip = Trip.query.get_or_404(trip)

    if selected_trip.author != current_user:
        abort(403)

    form = CreateTripForm()

    if form.validate_on_submit():
        if form.trip_picture.data:
            picture_file = save_picture_trip(form.trip_picture.data)
            selected_trip.image_file = picture_file

        selected_trip.location = form.location.data
        selected_trip.price = form.price.data

        counter=0
        for user in selected_trip.users:
            counter+=1

        if selected_trip.people_number <= form.people_number.data:      # nitko od prijavljenih ne smije izvisiti
            selected_trip.people_number = form.people_number.data
        else:
            flash('Pogrešan unos! Broj prijavljenih korisnika: {}'.format(counter), 'danger')
            return redirect(url_for('trips.update_trip', trip=selected_trip.id))
        selected_trip.starting_at = form.starting_at.data
        selected_trip.transport_type = form.transport_type.data
        selected_trip.trip_duration = form.trip_duration.data
        selected_trip.details = form.details.data

        if selected_trip.people_number == form.people_number.data:      #posalji autoru mail da mu je izlet pun
            # event = Event.query.filter(Event.name==selected_trip.name.data, Event.event=="is_full")
            event = Event.query.filter_by(name=selected_trip.name, event='is_full').first()
            if event:
                if event.executed == False:
                    trip_is_full(selected_trip.author, selected_trip)
                    event.executed = True                                   # posalji tu poruku samo jednom...
        db.session.commit()

        flash('Vas trip je ažuriran!')
        return redirect(url_for('main.home', trip=selected_trip.id))

    elif request.method == 'GET':
        form.name.data = selected_trip.name
        form.location.data = selected_trip.location
        form.price.data = selected_trip.price
        form.people_number.data = selected_trip.people_number
        form.starting_at.data = selected_trip.starting_at
        form.transport_type.data = selected_trip.transport_type
        form.trip_duration.data = selected_trip.trip_duration
        form.details.data = selected_trip.details

    return render_template('new_trip2.html', title='Update Trip', form=form,
                           trip=selected_trip, legend='Update Trip')


@trips.route('/delete/<int:trip>', methods=['GET', 'POST'])
@login_required
def delete_trip(trip):
    selected_trip = Trip.query.get_or_404(trip)
    if selected_trip.author != current_user:
        abort(403)
    db.session.delete(selected_trip)
    db.session.commit()
    flash(f'>Izbrisali ste vaš izlet!')
    return redirect(url_for('main.home'))



