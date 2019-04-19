from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required

from app import db
from app.models import Trip, User
from app.trips.forms import CreateTripForm
from app.users.utils import save_picture_trip

trips = Blueprint('trips', __name__)


@trips.route('/new_trip', methods=['POST', 'GET'])
@login_required
def new_trip():
    form = CreateTripForm()

    if form.validate_on_submit():
        picture_file = 'trip_default.jpg'
        if form.trip_picture.data:
            picture_file = save_picture_trip(form.trip_picture.data)
        trip = Trip(name=form.name.data, location=form.location.data, user_id=current_user.id, price=form.price.data,
                    people_number=form.people_number.data, starting_at=form.starting_at.data,
                    transport_type=form.transport_type.data, trip_duration=form.trip_duration.data,
                    details=form.details.data, image_file=picture_file)

        try:
            db.session.add(trip)
            db.session.commit()

            flash('Your post has been created!', 'success')
            return redirect(url_for('main.home'))
        except:
            flash("Greška prilikom stvaranja izleta. Provjerite Vaš unos. Za korisniču podršku nam se obratite "
                  "na email -- trippinapplication@gmail.com -- .", "danger")

    return render_template('new_trip2.html', form=form, title='New Trip')


@trips.route("/show_trip/<int:trip_id>")
def show_trip(trip_id):
    selected_trip = Trip.query.get_or_404(trip_id)

    counter = 0
    for user in selected_trip.users:
        counter+=1                      # broj korisnika prijavljenih na izlet

    users = User.query.filter(User.trips_joined.any(id=trip_id)).all()
    mylist = [x.username for x in users]
    print(mylist)
    return render_template('show_trip2.html', title=selected_trip.location, trip=selected_trip,
                           users=users, counter=counter, mylist=mylist)


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
        print(counter)

        if selected_trip.people_number <= form.people_number.data:
            selected_trip.people_number = form.people_number.data
        else:
            flash('Pogrešan unos! Broj prijavljenih korisnika: {}'.format(counter), 'danger')
            return redirect(url_for('trips.update_trip', trip=selected_trip.id))
        selected_trip.starting_at = form.starting_at.data
        selected_trip.transport_type = form.transport_type.data
        selected_trip.trip_duration = form.trip_duration.data
        selected_trip.details = form.details.data

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



