from foxygallery import database, app
from foxygallery.models import Usuario, Post


with app.app_context():
    database.create_all()