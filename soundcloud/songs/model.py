from datetime import datetime
from soundcloud import db


class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    image_file = db.Column(db.String(100), nullable=False,
                           default='default.jpg')
    filepath = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('SongLike', backref='songs', lazy='dynamic')
    comments = db.relationship('Comments', backref='songs', lazy='dynamic')

    def __repr__(self):
        return f"Songs('{self.title}', '{self.date_posted}')"


class SongLike(db.Model):
    __tablename__ = 'song_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), db.ForeignKey('user.username'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))
    comment = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.Float)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)


class PlayCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))
