from flask import Blueprint
from flask import render_template, request

from app.models import Trip


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    trips = Trip.query.order_by(Trip.date_created.desc()).paginate(page=page, per_page=5)
    # users = User.query.filter(User.trips_joined.any(id=4)).all()
    return render_template('home.html', trips=trips)


@main.route('/about')
def about():
    return render_template('about.html', title='About')



