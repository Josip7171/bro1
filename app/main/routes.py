from flask import render_template, request, Blueprint
from sqlalchemy import func
from datetime import datetime

from app.models import Trip, User
from app.main.forms import SearchForm
from app.nortify_users import trip_start_check

main = Blueprint('main', __name__)


@main.route('/home2', methods=["GET", "POST"])
def home():
    sForm = SearchForm()

    now = datetime.now()
    if now.hour == 0 or now.hour == 12:
        trip_start_check()

    if sForm.validate_on_submit():
        if sForm.search.data:
            result1 = User.query.filter(func.lower(User.username) == func.lower(sForm.search.data))
            result2 = Trip.query.filter(func.lower(Trip.name) == func.lower(sForm.search.data))
            result3 = Trip.query.filter(func.lower(Trip.location) == func.lower(sForm.search.data))
            result4 = User.query.filter(func.lower(User.first_name) == func.lower(sForm.search.data))
            result5 = User.query.filter(func.lower(User.last_name) == func.lower(sForm.search.data))
            result6 = User.query.filter(func.lower(User.full_name) == func.lower(sForm.search.data))

            return render_template('results.html', users=result1, trips_name=result2,
                                   trips_location=result3, users_name=result4, users_last_name=result5,
                                   users_full_name=result6, sForm=sForm)
        else:
            result = User.query.all()
            result2 = Trip.query.all()

            return render_template('results.html', users=result, sForm=sForm, trips=result2)

    per_page_val = 5
    page = request.args.get('page', 1, type=int)
    trips = Trip.query.order_by(Trip.date_created.desc()).paginate(page=page, per_page=per_page_val)
    users = User.query.all()

    ids = [("id"+ str(trip.id)) for trip in trips.items]
    print(ids)

    return render_template('home2.html', trips=trips, users=users, sForm=sForm, ids=ids)

