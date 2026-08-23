from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
  app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:X3raV5VrcMzt4x4U3nj5@localhost/IT_MANAGEMENT"
  app.config["SQL_TRACK_MODIFICATIONS"] = False
  db.init_app(app)





