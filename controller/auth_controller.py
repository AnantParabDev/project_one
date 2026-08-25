from flask import Blueprint, jsonify, make_response, redirect, render_template, request
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from dao.role_dao import RoleDAO
from dao.user_dao import UserDAO
from service.role_service import RoleService
from service.user_service import UserService
auth_bp = Blueprint('auth', __name__)
user_service = UserService(UserDAO())
role_service = RoleService(RoleDAO())

@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')
    user = user_service.add_user(username, email, password, role_id)
    return (jsonify({'message': 'User Registered Successfully', 'user': user.to_dict()}), 201)

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = user_service.verify_login(email, password)
    if not user:
        return (jsonify({'message': 'Invalid email or password'}), 401)
    role = role_service.get_role_by_id(user.role_id)
    additional_claims = {'username': user.username, 'role': role.roles}
    access_token = create_access_token(identity=str(user.user_id), additional_claims=additional_claims)
    return (jsonify({'message': 'Login Successful', 'access_token': access_token, 'user': user.to_dict()}), 200)

@auth_bp.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def handle_register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role_id = request.form.get('role_id')
    try:
        user_service.add_user(username, email, password, role_id)
    except Exception:
        return render_template('register.html', error='Registration failed. The email address may already be in use.')
    return redirect('/')

@auth_bp.route('/login', methods=['POST'])
def handle_login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = user_service.verify_login(email, password)
    if not user:
        return render_template('login.html', error='Incorrect email or password. Please try again.')
    role = role_service.get_role_by_id(user.role_id)
    additional_claims = {'username': user.username, 'role': role.roles}
    access_token = create_access_token(identity=str(user.user_id), additional_claims=additional_claims)
    response = make_response(redirect('/dashboard'))
    set_access_cookies(response, access_token)
    return response

@auth_bp.route('/logout', methods=['GET'])
def handle_logout():
    response = make_response(redirect('/'))
    unset_jwt_cookies(response)
    return response