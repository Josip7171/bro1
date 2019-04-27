from flask import Blueprint
from flask import url_for, flash, redirect
from flask_login import current_user, login_required

from app import db
from app.models import Comment

comments = Blueprint('comments', __name__)


@comments.route('/delete_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    selected_comment = Comment.query.get_or_404(comment_id)
    trip_id = selected_comment.trip_id
    if selected_comment.comment_author != current_user:
        flash("Nemate ovasti izbrisati navedeni komentar.", "danger")
        return redirect(url_for('trips.show_trip'))
    db.session.delete(selected_comment)
    db.session.commit()
    flash(f'>Uspješno ste izbrisali komentar!', 'success')
    return redirect(url_for('trips.show_trip', trip_id=trip_id))



