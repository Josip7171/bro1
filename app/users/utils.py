from flask import url_for, current_app
import secrets, os
from PIL import Image

from app import mail
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_picture_trip(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/trip_pics', picture_fn)

    output_size = (300, 225)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def registration_email(user, rand_password):
    token = user.get_reset_token()
    msg = Message('Registracija', sender='trippinapplication@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Da biste izmjenili svoju lozinku kliknite na sljedeći link
{url_for('users.reset_token', token=token, _external=True)}

Trenutna lozinka je "{rand_password}"


Ugodan ostatak dana želi Vam TrippinApp!
    '''
    mail.send(msg)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Resetiranje lozinke', sender='trippinapplication@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password visit the folowing link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request than simply ignore this email and no changes will be made.

    '''
    mail.send(msg)


def send_nortification_mail_24(user, trip):
    msg = Message('Pocetak izleta za manje od 24 sata!', sender='trippinapplication@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Pozdrav "{ user.username }",
Obavještavamo Vas da je vrijeme polaska izleta "{trip.name}" na koji ste se prijavili jako blizu!
    
Ugodan ostatak dana želi vam TrippinApp!
    '''
    mail.send(msg)


def trip_is_full(user, trip):
    msg = Message('Vaš izlet je popunjen!', sender='trippinapplication@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Pozdrav "{user.username}",
Obavještavamo Vas da je Vaš izlet "{trip.name}" popunjen!

Ugodan ostatak dana želi vam TrippinApp!
    '''
    mail.send(msg)


def trip_deleted(user, trip):
    msg = Message('Izlet Obrisan!', sender='trippinapplication@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Pozdrav "{user.username}",
Obavještavamo Vas da je izlet "{trip.name}" na koji ste bili prijavljeni izbrisan.

Ugodan ostatak dana želi vam TrippinApp!
    '''
    mail.send(msg)
