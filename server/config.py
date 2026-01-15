import os
from flask import render_template
from dotenv import load_dotenv
load_dotenv()


from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/dist',  
    template_folder='../client/dist'
)
app.secret_key = b'\xfew6MO\xd3\xd0\xa5xft\x0f&\x18\\j'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)

api = Api(app)
CORS(app)
@app.route('/')
def index():
    return render_template("index.html")

# 2. This handles page refreshes (e.g., if someone refreshes on /login)
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")
# @app.route("/api/health")
# def health():
#     return {"status": "ok"}  cd server && flask db upgrade