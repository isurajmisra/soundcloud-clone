from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from soundcloud import db, login_manager
from flask_login import UserMixin
from soundcloud.songs.model import SongLike


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    songs = db.relationship('Songs', backref='author', lazy=True)
    liked = db.relationship(
        'SongLike',
        foreign_keys='SongLike.user_id',
        backref='user', lazy='dynamic')
    comments = db.relationship(
        'Comments', foreign_keys='Comments.user_name',
        backref='user', lazy='dynamic')

    def like(self, songs):
        if not self.is_liking(songs):
            like = SongLike(user_id=self.id, song_id=songs.id)
            db.session.add(like)

    def unlike(self, songs):
        if self.is_liking(songs):
            SongLike.query.filter_by(
                user_id=self.id,
                song_id=songs.id).delete()

    def is_liking(self, songs):
        return SongLike.query.filter(
            SongLike.user_id == self.id,
            SongLike.song_id == songs.id).count() > 0

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
