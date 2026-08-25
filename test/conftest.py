import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['DB_URI'] = 'sqlite:///:memory:'
os.environ['JWT_SECRET_KEY'] = 'test-secret-key-do-not-use-in-production'
import pytest
from app import create_app
from config.database import db as _db

@pytest.fixture(scope='session')
def app():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    flask_app.config['JWT_TOKEN_LOCATION'] = ['headers']
    flask_app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    with flask_app.app_context():
        _db.create_all()
        from models.role import Role
        roles = [Role(role_id=1, roles='USER'), Role(role_id=2, roles='SUPPORT_AGENT'), Role(role_id=3, roles='ADMIN')]
        _db.session.bulk_save_objects(roles)
        from models.category import Category
        _db.session.add(Category(category_id=1, category_name='Network'))
        _db.session.commit()
        yield flask_app
        _db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

def get_token(client, email, password):
    resp = client.post('/api/login', json={'email': email, 'password': password})
    data = resp.get_json()
    return data.get('access_token') if data else None