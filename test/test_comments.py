from conftest import get_token

def _setup(client, email, role_id=1):
    client.post('/api/register', json={'username': email.split('@')[0], 'email': email, 'password': 'pass123', 'role_id': role_id})
    token = get_token(client, email, 'pass123')
    headers = {'Authorization': f'Bearer {token}'}
    resp = client.post('/api/tickets', json={'title': 'Comment Test Ticket', 'description': 'For comment tests', 'category_id': 1, 'priority': 'Low'}, headers=headers)
    ticket_id = resp.get_json()['ticket']['ticket_id']
    return (headers, ticket_id)

def test_get_comments_empty(client):
    headers, ticket_id = _setup(client, 'comment_empty@test.com')
    resp = client.get(f'/api/tickets/{ticket_id}/comments', headers=headers)
    assert resp.status_code == 200
    assert resp.get_json() == []

def test_add_comment(client):
    headers, ticket_id = _setup(client, 'comment_add@test.com')
    resp = client.post(f'/api/tickets/{ticket_id}/comments', json={'comment': 'This is a test comment.'}, headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'comment' in data
    assert data['comment']['comment'] == 'This is a test comment.'

def test_get_comments_after_add(client):
    headers, ticket_id = _setup(client, 'comment_get@test.com')
    client.post(f'/api/tickets/{ticket_id}/comments', json={'comment': 'First comment.'}, headers=headers)
    resp = client.get(f'/api/tickets/{ticket_id}/comments', headers=headers)
    assert resp.status_code == 200
    comments = resp.get_json()
    assert len(comments) >= 1
    assert comments[0]['comment'] == 'First comment.'

def test_comment_requires_auth(client):
    resp = client.post('/api/tickets/1/comments', json={'comment': 'Sneaky comment'})
    assert resp.status_code == 401

def test_comment_response_has_fields(client):
    headers, ticket_id = _setup(client, 'comment_fields@test.com')
    resp = client.post(f'/api/tickets/{ticket_id}/comments', json={'comment': 'Field check comment.'}, headers=headers)
    comment = resp.get_json()['comment']
    for field in ['comment_id', 'comment', 'ticket_id', 'user_id']:
        assert field in comment, f'Missing field in comment response: {field}'