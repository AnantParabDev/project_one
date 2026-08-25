from conftest import get_token

def test_register_user(client):
    resp = client.post('/api/register', json={'username': 'testuser', 'email': 'testuser@test.com', 'password': 'pass123', 'role_id': 1})
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'user' in data
    assert data['user']['email'] == 'testuser@test.com'

def test_register_returns_user_fields(client):
    resp = client.post('/api/register', json={'username': 'fieldcheckuser', 'email': 'fieldcheck@test.com', 'password': 'pass123', 'role_id': 1})
    user = resp.get_json()['user']
    assert 'user_id' in user
    assert 'username' in user
    assert 'email' in user
    assert 'role_id' in user

def test_login_success(client):
    client.post('/api/register', json={'username': 'loginuser', 'email': 'login@test.com', 'password': 'pass123', 'role_id': 1})
    resp = client.post('/api/login', json={'email': 'login@test.com', 'password': 'pass123'})
    assert resp.status_code == 200
    assert 'access_token' in resp.get_json()

def test_login_wrong_password(client):
    resp = client.post('/api/login', json={'email': 'login@test.com', 'password': 'WRONGPASSWORD'})
    assert resp.status_code == 401

def test_login_nonexistent_user(client):
    resp = client.post('/api/login', json={'email': 'ghost@test.com', 'password': 'anything'})
    assert resp.status_code == 401

def test_login_response_has_user(client):
    client.post('/api/register', json={'username': 'fullresp', 'email': 'fullresp@test.com', 'password': 'pass123', 'role_id': 1})
    resp = client.post('/api/login', json={'email': 'fullresp@test.com', 'password': 'pass123'})
    data = resp.get_json()
    assert 'user' in data
    assert data['user']['email'] == 'fullresp@test.com'