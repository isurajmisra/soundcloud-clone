from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    song_image = FileField('Upload Song Picture', validators=[
                           FileAllowed(['jpg', 'png'])])
    song_file = FileField('Upload song', validators=[
        DataRequired(), FileAllowed(['mp3', 'ogg', 'wav'])])
    submit = SubmitField('Upload')


class UpdateSongForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    picture = FileField('Update Song Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
