from soundcloud.songs.model import PlayCount, Songs, Comments
from sqlalchemy import func


def get_all_comments(song_id):
    comments = Comments.query.filter_by(song_id = song_id).order_by(
        Comments.date_posted.desc())
    return comments


def get_song(song_id):
    song = Songs.query.get_or_404(song_id)
    return song


def get_path(mediaPath):
    path = list(mediaPath.split("/", 1))
    return path[-1]


def get_count(song_id):
    count = PlayCount.query.with_entities(func.count(
        PlayCount.user_name)).filter_by(song_id=song_id).first()
    return count[0]


def get_song_list(page):
    songList = Songs.query.order_by(
        Songs.date_posted.desc()).paginate(page=page, per_page=5)
    return songList


def get_count_list():
    countList = PlayCount.query.with_entities(PlayCount.song_id, func.count(
        PlayCount.user_name)).group_by(PlayCount.song_id).all()
    return countList


def get_all_songs_by_user(user_id):
    # print(user_id)
    songs = Songs.query.filter_by(user_id=user_id).all()
    return songs
