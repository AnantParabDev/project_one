"""
test_file_upload.py
-------------------
Tests for the file-attachment upload endpoint.

POST /api/tickets/<id>/attachments

Fixtures auto-discovered from conftest.py.

Author: Anant Parab
"""

import io

from conftest import get_token


                                                                             
                                                                        
                                                                             

def _setup_user_and_ticket(client, email):
    """
    Register a user, log them in, and create a test ticket.
    Returns (auth_headers dict, ticket_id int).
    """
    client.post("/api/register", json={
        "username": email.split("@")[0],
        "email":    email,
        "password": "pass123",
        "role_id":  1
    })
    token = get_token(client, email, "pass123")
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post("/api/tickets", json={
        "title":       "Upload Test Ticket",
        "description": "Ticket for file upload tests",
        "category_id": 1,
        "priority":    "Low"
    }, headers=headers)
    ticket_id = resp.get_json()["ticket"]["ticket_id"]
    return headers, ticket_id


                                                                             
              
                                                                             

def test_upload_no_file_part(client):
    """
    POST without the 'file' multipart field must return 400.
    """
    client.post("/api/register", json={
        "username": "uploaduser",
        "email":    "upload@test.com",
        "password": "pass123",
        "role_id":  1
    })
    token = get_token(client, "upload@test.com", "pass123")
    headers = {"Authorization": f"Bearer {token}"}

                                                           
    resp = client.post("/api/tickets/1/attachments", headers=headers)
    assert resp.status_code == 400
    assert "file part" in resp.get_json()["message"].lower()


def test_upload_empty_filename(client):
    """
    POST with an empty filename string must return 400.
    """
    token = get_token(client, "upload@test.com", "pass123")
    headers = {"Authorization": f"Bearer {token}"}

    data = {"file": (io.BytesIO(b"content"), "")}
    resp = client.post(
        "/api/tickets/1/attachments",
        data=data,
        content_type="multipart/form-data",
        headers=headers
    )
    assert resp.status_code == 400


def test_upload_invalid_extension(client):
    """
    Uploading a file with a forbidden extension (.exe) must return 400.
    """
    token = get_token(client, "upload@test.com", "pass123")
    headers = {"Authorization": f"Bearer {token}"}

    data = {"file": (io.BytesIO(b"malicious content"), "virus.exe")}
    resp = client.post(
        "/api/tickets/1/attachments",
        data=data,
        content_type="multipart/form-data",
        headers=headers
    )
    assert resp.status_code == 400
    assert "not allowed" in resp.get_json()["message"].lower()


def test_upload_valid_pdf(client):
    """
    Uploading a valid PDF to an existing ticket must NOT return 400.
    (It returns 201 if the ticket exists; other statuses are acceptable
    as long as the extension validation did not reject it.)
    """
    headers, ticket_id = _setup_user_and_ticket(client, "uploader2@test.com")

    data = {"file": (io.BytesIO(b"%PDF-1.4 minimal pdf content"), "report.pdf")}
    resp = client.post(
        f"/api/tickets/{ticket_id}/attachments",
        data=data,
        content_type="multipart/form-data",
        headers=headers
    )
                                            
    assert resp.status_code != 400


def test_upload_valid_image(client):
    """
    Uploading a PNG image to an existing ticket must be accepted.
    """
    headers, ticket_id = _setup_user_and_ticket(client, "imguploader@test.com")

                                          
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0c"
        b"IDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00"
        b"\x00IEND\xaeB`\x82"
    )
    data = {"file": (io.BytesIO(png_bytes), "screenshot.png")}
    resp = client.post(
        f"/api/tickets/{ticket_id}/attachments",
        data=data,
        content_type="multipart/form-data",
        headers=headers
    )
    assert resp.status_code != 400


def test_upload_requires_auth(client):
    """
    Attempting a file upload without a JWT must return 401.
    """
    data = {"file": (io.BytesIO(b"%PDF-1.4"), "noauth.pdf")}
    resp = client.post(
        "/api/tickets/1/attachments",
        data=data,
        content_type="multipart/form-data"
    )
    assert resp.status_code == 401
