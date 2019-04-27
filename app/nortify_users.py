from app.models import Event, Trip
from datetime import datetime, timedelta

from app import db
from app.users.utils import send_nortification_mail_24, trip_deleted


def trip_start_check():
    trips = Trip.query.all()

    for trip in trips:
        if trip.starting_at >= (datetime.today() - timedelta(days=30)):          # ako izlet pocinje za manje od 1 dana
            event = Event.query.filter_by(name=trip.name, event="starting_soon").first()
            if event:
                if event.executed == False:
                    for user in trip.users:
                        send_nortification_mail_24(user, trip)
                    event.executed = True
                    db.session.commit()


def trip_deleted_nortify(trip_id):
    trip = Trip.query.filter_by(id=trip_id).first()
    print("TRIP NAME", trip.name)

    event = Event.query.filter_by(name=trip.name, event="trip_deleted").first()
    if event:
        if event.executed == False:
            for user in trip.users:
                trip_deleted(user, trip)
            event.executed = True
            db.session.commit()

