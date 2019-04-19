from flask import Blueprint
from flask import render_template, request

from app.models import Trip, User


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    trips = Trip.query.order_by(Trip.date_created.desc()).paginate(page=page, per_page=5)

    trips2 = Trip.query.all()
    mydict = {}
    for i in range(len(trips2), 0, -1):
        users = User.query.filter(User.trips_joined.any(id=i)).all()
        mydict[i] = [x.username for x in users]
        # Tu bi mogo prosljedit sve podatke od usera a ne samo username
        # pa bi mogao i napravit link od svakog imena (?)

    # users = User.query.filter(User.trips_joined.any(id=4)).all()
    return render_template('home.html', trips=trips, mydict=mydict, dict_length=len(mydict))


@main.route('/about')
def about():
    return render_template('about.html', title='About')


