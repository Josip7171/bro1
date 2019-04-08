from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required

from app import db
from app.models import Trip
from app.trips.forms import CreateTripForm

trips = Blueprint('trips', __name__)


@trips.route('/new_trip', methods=['POST', 'GET'])
@login_required
def new_trip():
    form = CreateTripForm()
    if form.validate_on_submit():
        trip = Trip(location=form.location.data, user_id=current_user.id, details=form.details.data)
        db.session.add(trip)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_trip.html', form=form, title='New Trip')


@trips.route("/show_trip/<int:trip_id>")
def show_trip(trip_id):
    selected_trip = Trip.query.get_or_404(trip_id)
    return render_template('show_trip.html', title=selected_trip.location, trip=selected_trip)


@trips.route("/update/<int:trip>", methods=["POST", "GET"])
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
        return redirect(url_for('main.home', trip=selected_trip.id))
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


@trips.route('/delete/<int:trip>', methods=['GET', 'POST'])
@login_required
def delete_trip(trip):
    selected_trip = Trip.query.get_or_404(trip)
    if selected_trip.author != current_user:
        abort(403)
    db.session.delete(selected_trip)
    db.session.commit()
    flash(f'>Izbrisali ste vas izlet!')
    return redirect(url_for('main.home'))



