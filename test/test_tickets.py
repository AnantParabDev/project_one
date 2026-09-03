from conftest import get_token

def _auth_headers(client, email, role_id=1):
    client.post('/api/register', json={'username': email.split('@')[0], 'email': email, 'password': 'pass123', 'role_id': role_id})
    token = get_token(client, email, 'pass123')
    return {'Authorization': f'Bearer {token}'}

def test_create_ticket_no_auth(client):
    resp = client.post('/api/tickets', json={'title': 'Test', 'description': 'desc', 'category_id': 1, 'priority': 'Low'})
    assert resp.status_code == 401

def test_get_tickets_no_auth(client):
    resp = client.get('/api/tickets')
    assert resp.status_code == 401

def test_create_ticket(client):
    headers = _auth_headers(client, 'ticket@test.com')
    resp = client.post('/api/tickets', json={'title': 'My First Ticket', 'description': 'Something broke in production', 'category_id': 1, 'priority': 'High'}, headers=headers)
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'ticket' in data
    assert data['ticket']['title'] == 'My First Ticket'

def test_create_ticket_response_fields(client):
    headers = _auth_headers(client, 'fieldticket@test.com')
    resp = client.post('/api/tickets', json={'title': 'Field Check Ticket', 'description': 'checking response fields', 'category_id': 1, 'priority': 'Medium'}, headers=headers)
    ticket = resp.get_json()['ticket']
    for field in ['ticket_id', 'title', 'description', 'status', 'priority', 'created_by', 'created_at']:
        assert field in ticket, f'Missing field: {field}'

def test_create_ticket_default_status_is_open(client):
    headers = _auth_headers(client, 'statuscheck@test.com')
    resp = client.post('/api/tickets', json={'title': 'Status Check Ticket', 'description': 'Checking default status', 'category_id': 1, 'priority': 'Low'}, headers=headers)
    ticket = resp.get_json()['ticket']
    assert ticket['status'] == 'open'

def test_create_ticket_high_priority_due_date_set(client):
    headers = _auth_headers(client, 'highpri@test.com')
    resp = client.post('/api/tickets', json={'title': 'Urgent Ticket', 'description': 'Very urgent', 'category_id': 1, 'priority': 'High'}, headers=headers)
    ticket = resp.get_json()['ticket']
    assert ticket['due_date'] is not None

def test_get_all_tickets(client):
    headers = _auth_headers(client, 'list@test.com')
    resp = client.get('/api/tickets', headers=headers)
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)

def test_get_ticket_by_valid_id(client):
    headers = _auth_headers(client, 'getbyid@test.com')
    create_resp = client.post('/api/tickets', json={'title': 'Lookup Ticket', 'description': 'Will be fetched by ID', 'category_id': 1, 'priority': 'Low'}, headers=headers)
    ticket_id = create_resp.get_json()['ticket']['ticket_id']
    resp = client.get(f'/api/tickets/{ticket_id}')
    assert resp.status_code == 200
    assert resp.get_json()['ticket_id'] == ticket_id

def test_get_ticket_invalid_id(client):
    resp = client.get('/api/tickets/99999')
    assert resp.status_code == 404

def test_filter_tickets_by_status(client):
    headers = _auth_headers(client, 'filteruser@test.com')
    resp = client.get('/api/tickets?status=open', headers=headers)
    assert resp.status_code == 200
    tickets = resp.get_json()
    for t in tickets:
        assert t['status'] == 'open'