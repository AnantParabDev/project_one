"""
test_auth.py
------------
Tests for user registration and login (REST API endpoints).

Fixtures `app` and `client` are automatically injected from conftest.py.
`get_token` is a helper imported from conftest.py.

Author: Anant Parab
"""

from conftest import get_token


                                                                             
                    
                                                                             

def test_register_user(client):
    """A valid registration payload should return 201 with a user object."""
    resp = client.post("/api/register", json={
        "username": "testuser",
        "email":    "testuser@test.com",
        "password": "pass123",
        "role_id":  1
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert "user" in data
    assert data["user"]["email"] == "testuser@test.com"


def test_register_returns_user_fields(client):
    """The returned user dict must contain user_id, username, email, role_id."""
    resp = client.post("/api/register", json={
        "username": "fieldcheckuser",
        "email":    "fieldcheck@test.com",
        "password": "pass123",
        "role_id":  1
    })
    user = resp.get_json()["user"]
    assert "user_id"  in user
    assert "username" in user
    assert "email"    in user
    assert "role_id"  in user


                                                                             
             
                                                                             

def test_login_success(client):
    """Valid credentials should return 200 with an access_token."""
                             
    client.post("/api/register", json={
        "username": "loginuser",
        "email":    "login@test.com",
        "password": "pass123",
        "role_id":  1
    })
    resp = client.post("/api/login", json={
        "email":    "login@test.com",
        "password": "pass123"
    })
    assert resp.status_code == 200
    assert "access_token" in resp.get_json()


def test_login_wrong_password(client):
    """A correct email but wrong password must return 401."""
                                                                          
    resp = client.post("/api/login", json={
        "email":    "login@test.com",
        "password": "WRONGPASSWORD"
    })
    assert resp.status_code == 401


def test_login_nonexistent_user(client):
    """Trying to log in with an email that was never registered must return 401."""
    resp = client.post("/api/login", json={
        "email":    "ghost@test.com",
        "password": "anything"
    })
    assert resp.status_code == 401


def test_login_response_has_user(client):
    """Successful login response must include the user object."""
    client.post("/api/register", json={
        "username": "fullresp",
        "email":    "fullresp@test.com",
        "password": "pass123",
        "role_id":  1
    })
    resp = client.post("/api/login", json={
        "email":    "fullresp@test.com",
        "password": "pass123"
    })
    data = resp.get_json()
    assert "user" in data
    assert data["user"]["email"] == "fullresp@test.com"
