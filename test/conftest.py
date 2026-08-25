"""
conftest.py
-----------
pytest configuration file for the IT Service Desk test suite.

Placing fixtures here (at the package level) makes them automatically
available to every test module in this directory WITHOUT needing an
explicit import statement — pytest discovers conftest.py automatically.

This replaces the previous pattern of `from utils import app, client`
which only worked when pytest was run from inside the /test directory.

To run all tests from the project root:
    pytest test/ -v

Author: Anant Parab
"""

import os
import sys

                                                                             
                                                                        
                                                         
                                                                             
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

                                                                              
                                                 
os.environ["DB_URI"] = "sqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-do-not-use-in-production"

import pytest
from app import create_app
from config.database import db as _db


                                                                             
                                                               
                                                                             
@pytest.fixture(scope="session")
def app():
    """
    Create a fully configured Flask test application backed by an in-memory
    SQLite database.  The database is seeded with the minimum data required
    for every test (roles + one category) and torn down at the end.
    """
    flask_app = create_app()
    flask_app.config["TESTING"] = True
                                                                           
    flask_app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    flask_app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    with flask_app.app_context():
        _db.create_all()

                                                                    
        from models.role import Role
        roles = [
            Role(role_id=1, roles="USER"),
            Role(role_id=2, roles="SUPPORT_AGENT"),
            Role(role_id=3, roles="ADMIN"),
        ]
        _db.session.bulk_save_objects(roles)

                                                                           
        from models.category import Category
        _db.session.add(Category(category_id=1, category_name="Network"))

        _db.session.commit()
        yield flask_app

                                                           
        _db.drop_all()


                                                                             
                                                                    
                                                                             
@pytest.fixture()
def client(app):
    """Return a Flask test client for making HTTP requests in tests."""
    return app.test_client()


                                                                             
                                                                      
                                                                             
def get_token(client, email, password):
    """
    Log in via the JSON API and return the JWT access token string,
    or None if the login fails.

    Usage in tests:
        token = get_token(client, "user@test.com", "pass123")
        headers = {"Authorization": f"Bearer {token}"}
    """
    resp = client.post("/api/login", json={"email": email, "password": password})
    data = resp.get_json()
    return data.get("access_token") if data else None
