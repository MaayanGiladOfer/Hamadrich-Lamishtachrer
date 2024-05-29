from flask import Flask
from app.config import Config
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
    pages = [
        Page(id=1, title='Page 1', template_name='page1.html'),
        Page(id=2, title='Page 2', template_name='page2.html'),
        Page(id=3, title='Page 3', template_name='page3.html'),
        Page(id=4, title='Page 4', template_name='page4.html'),
        Page(id=5, title='Page 5', template_name='page5.html'),
        Page(id=6, title='Page 6', template_name='page6.html'),
        Page(id=7, title='Page 7', template_name='page7.html'),
        Page(id=8, title='Page 8', template_name='page8.html'),
        Page(id=9, title='Page 9', template_name='page9.html'),
        Page(id=10, title='Page 10', template_name='page10.html'),
        Page(id=11, title='Page 11', template_name='page11.html'),
        Page(id=12, title='Page 12', template_name='page12.html'),
        Page(id=13, title='Page 13', template_name='page13.html'),
        Page(id=14, title='Page 14', template_name='page14.html'),
        Page(id=15, title='Page 15', template_name='page15.html'),
        Page(id=16, title='Page 16', template_name='page16.html'),
        Page(id=17, title='Page 17', template_name='page17.html'),
        Page(id=18, title='Page 18', template_name='page18.html'),
        Page(id=19, title='Page 19', template_name='page19.html'),
        Page(id=20, title='Page 20', template_name='page20.html'),
    ]
    for page in pages:
        existing_page = Page.query.get(page.id)
        if not existing_page:
            db.session.add(page)
    db.session.commit()

with app.app_context():
    db.create_all()
    create_pages()