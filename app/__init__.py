from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import views, models

def create_pages():
    from app.models import Page
    if Page.query.count() == 0:
        pages = [
            Page(id=1, title='Page 1', template_name='page1.html'),
            Page(id=2, title='Page 2', template_name='page2.html'),
            Page(id=3, title='Page 3', template_name='page3.html'),
        ]
        db.session.bulk_save_objects(pages)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_pages()