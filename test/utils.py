import os
os.environ['DB_URI'] = 'sqlite:///:memory:'
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import create_app
from config.database import db as _db

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    with app.app_context():
        _db.create_all()
        from models.role import Role
        roles = [Role(role_id=1, roles='USER'), Role(role_id=2, roles='SUPPORT_AGENT'), Role(role_id=3, roles='ADMIN')]
        _db.session.bulk_save_objects(roles)
        from models.category import Category
        _db.session.add(Category(category_id=1, category_name='Network'))
        _db.session.commit()
        yield app
        _db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

def get_token(client, email, password):
    resp = client.post('/api/login', json={'email': email, 'password': password})
    data = resp.get_json()
    return data.get('access_token')