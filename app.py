from flask import Flask, redirect, jsonify, request
from config.database import  db, init_db
from controller.auth_controller import auth_bp
from controller.ticket_controller import ticket_bp
from controller.category_controller import category_bp
from flask_jwt_extended import JWTManager
from controller.comment_controller import comment_bp

def create_app():
  app = Flask(__name__)
  init_db(app)

  app.config["JWT_SECRET_KEY"] = "super-secrete-key"
  app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
  app.config["JWT_COOKIE_CSRF_PROJECT"]=False

  app.register_blueprint(auth_bp)
  app.register_blueprint(ticket_bp)
  app.register_blueprint(category_bp)
  app.register_blueprint(comment_bp)

  jwt = JWTManager(app)

  @jwt.unauthorized_loader
  def missing_token_callback(err_string):
    if request.is_json or request.path.startswith('/api'):
      return jsonify({
        "message" : "Authorization token is missing",
        "error" :  "unauthorized"
      }), 401
    #set web related here
    return redirect("/")

  @jwt.invalid_token_loader
  def invalid_token_callback(err_string):
      if request.is_json or request.path.startswith("/api"):
                  return jsonify({
                      "message": "Authorization token is invalid",
                      "error": "invalid_token"
                  }), 401
      return redirect("/")


  with app.app_context():
    # db.drop_all()
    db.create_all()
  return app


if __name__ == "__main__":
  app = create_app()
  app.run(host = '0.0.0.0', port = 5000, debug = True)