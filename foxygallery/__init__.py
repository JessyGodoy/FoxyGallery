from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

#criando aplication do flask(app) - forma padrão
app = Flask(__name__)
#criando o banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
app.config["SECRET_KEY"] = "233e7b855f892e25ce35ddc8a344a3e6"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

#puxando o arquivo routes para que as rotas sejam vinculadas
from foxygallery import routes