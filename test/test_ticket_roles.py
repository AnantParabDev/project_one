"""
test_ticket_roles.py
--------------------
Tests for role-based access control on ticket operations.
Verifies that:
  - Regular USERs cannot modify status or priority
  - ADMIN can modify status
  - SUPPORT_AGENT can modify priority
  - ADMIN can assign tickets to agents

Fixtures auto-discovered from conftest.py.

Author: Anant Parab
"""

from conftest import get_token


                                                                             
                  
                                                                             

def _register_and_login(client, email, role_id):
    """Register a user and return their JWT token string."""
    client.post("/api/register", json={
        "username": email.split("@")[0],
        "email":    email,
        "password": "pass123",
        "role_id":  role_id,
    })
    return get_token(client, email, "pass123")


def _create_ticket(client, token):
    """Create a ticket as a given user and return its integer ID."""
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post("/api/tickets", json={
        "title":       "Role Test Ticket",
        "description": "Testing RBAC rules",
        "category_id": 1,
        "priority":    "Medium",
    }, headers=headers)
    return resp.get_json()["ticket"]["ticket_id"]


                                                                             
                          
                                                                             

def test_modify_status_as_user_forbidden(client):
    """A regular USER must get 403 when trying to change ticket status."""
    user_token = _register_and_login(client, "normaluser@test.com", 1)
    ticket_id = _create_ticket(client, user_token)

    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.put(
        f"/api/tickets/{ticket_id}/status",
        json={"status": "resolved"},
        headers=headers
    )
    assert resp.status_code == 403


def test_modify_status_as_admin(client):
    """An ADMIN must be able to change ticket status and get 200."""
    admin_token = _register_and_login(client, "admin@test.com", 3)
    user_token  = _register_and_login(client, "user2@test.com", 1)
    ticket_id   = _create_ticket(client, user_token)

    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.put(
        f"/api/tickets/{ticket_id}/status",
        json={"status": "resolved"},
        headers=headers
    )
    assert resp.status_code == 200
    assert resp.get_json()["ticket"]["status"] == "resolved"


def test_modify_status_as_agent(client):
    """A SUPPORT_AGENT must be able to change ticket status and get 200."""
    agent_token = _register_and_login(client, "agent_status@test.com", 2)
    user_token  = _register_and_login(client, "user_for_agent@test.com", 1)
    ticket_id   = _create_ticket(client, user_token)

    headers = {"Authorization": f"Bearer {agent_token}"}
    resp = client.put(
        f"/api/tickets/{ticket_id}/status",
        json={"status": "In Progress"},
        headers=headers
    )
    assert resp.status_code == 200


                                                                             
                            
                                                                             

def test_modify_priority_as_user_forbidden(client):
    """A regular USER must get 403 when trying to escalate priority."""
    user_token = _register_and_login(client, "priuser@test.com", 1)
    ticket_id  = _create_ticket(client, user_token)

    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.put(
        f"/api/tickets/{ticket_id}/priority",
        json={"priority": "High"},
        headers=headers
    )
    assert resp.status_code == 403


def test_modify_priority_as_agent(client):
    """A SUPPORT_AGENT must be able to escalate priority and get 200."""
    agent_token = _register_and_login(client, "agent@test.com", 2)
    user_token  = _register_and_login(client, "user3@test.com", 1)
    ticket_id   = _create_ticket(client, user_token)

    headers = {"Authorization": f"Bearer {agent_token}"}
    resp = client.put(
        f"/api/tickets/{ticket_id}/priority",
        json={"priority": "High"},
        headers=headers
    )
    assert resp.status_code == 200
    assert resp.get_json()["ticket"]["priority"] == "High"


def test_modify_priority_as_admin(client):
    """An ADMIN must be able to change priority and get 200."""
    admin_token = _register_and_login(client, "admin2@test.com", 3)
    user_token  = _register_and_login(client, "user4@test.com", 1)
    ticket_id   = _create_ticket(client, user_token)

    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.put(
        f"/api/tickets/{ticket_id}/priority",
        json={"priority": "Medium"},
        headers=headers
    )
    assert resp.status_code == 200


                                                                             
                        
                                                                             

def test_assign_ticket_as_admin(client):
    """Only ADMIN should be able to assign a ticket; must return 200."""
    admin_token = _register_and_login(client, "assignadmin@test.com", 3)
    user_token  = _register_and_login(client, "user5@test.com", 1)
    agent_token = _register_and_login(client, "assignagent@test.com", 2)
    ticket_id   = _create_ticket(client, user_token)

                                                       
    agent_resp = client.post("/api/login", json={
        "email": "assignagent@test.com", "password": "pass123"
    })
    agent_user_id = agent_resp.get_json()["user"]["user_id"]

    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.put(
        f"/api/tickets/{ticket_id}/assign",
        json={"assigned_to": agent_user_id},
        headers=headers
    )
    assert resp.status_code == 200
    assert resp.get_json()["ticket"]["assigned_to"] == agent_user_id


def test_assign_ticket_as_user_forbidden(client):
    """A regular USER must get 403 when trying to assign a ticket."""
    user_token = _register_and_login(client, "assignuser@test.com", 1)
    ticket_id  = _create_ticket(client, user_token)

    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.put(
        f"/api/tickets/{ticket_id}/assign",
        json={"assigned_to": 1},
        headers=headers
    )
    assert resp.status_code == 403
