from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
CORS(app, origins=["*"])


from view import *


# with app.app_context():
#     db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
