from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from celery import Celery

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(user="postgres",pw="password",host="postgres",port='5432',db='soundcloud')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
app.config['UPLOAD_FOLDER'] = 'static/'
db = SQLAlchemy(app)
app.app_context().push()
db.create_all()
db.session.commit()
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

from soundcloud.errors.routes import errors
app.register_blueprint(errors)

from soundcloud.main.routes import main
app.register_blueprint(main)

from soundcloud.users.routes import users
app.register_blueprint(users)

from soundcloud.songs.routes import songs
app.register_blueprint(songs)

from soundcloud.background.routes import background
app.register_blueprint(background)
