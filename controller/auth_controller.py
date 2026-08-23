from dao.user_dao import UserDAO
from dao.role_dao import RoleDAO
from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from models.user import User
from models.role import Role
from service import user_service
from service import role_service
from service.user_service import UserService
from service.role_service import RoleService

auth_bp = Blueprint('auth', __name__)
user_dao = UserDAO()
role_dao = RoleDAO()

user_service = UserService(UserDAO())
role_service = RoleService(RoleDAO())

@auth_bp.route('/api/register', methods=['POST'])
def api_register():
  data = request.get_json()

  username = data.get("username")
  email = data.get("email")
  password = data.get("password")
  role_id = data.get("role_id")

  user = user_service.add_user(username,email,password,role_id)


  return jsonify(
    {
      "message": "User Registered Successfully",
      "user":user.to_dict()
    }
), 201


@auth_bp.route('/api/login', methods=['POST'])
def api_login():
  data = request.get_json()
  email = data.get("email")
  password = data.get("password")

  user = user_service.verify_login(email,password)


  if not user:
      return jsonify({
        "message" : "Invalid email or password"
      }), 401

  role = role_service.get_role_by_id(user.role_id)

  additional_claims = {
    "username" : user.username,
    "role" : role.roles
  }

  access_token = create_access_token(identity=str(user.user_id), additional_claims=additional_claims)

  return jsonify({
    "message" : "Login Successful",
    "access_token" : access_token,
    "user" : user.to_dict()
  }), 200

# @auth_bp.route('/api/logout', methods=['GET'])
# def api_logout():
  
    

  


