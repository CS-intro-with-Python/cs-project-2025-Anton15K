def test_auth_register_login(client):
    """Test full registration and login flow."""
    # 1. Register
    reg_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "securepassword",
        "confirm_password": "securepassword"
    }
    resp = client.post("/api/v1/auth/register", json=reg_data)
    assert resp.status_code == 201
    
    # 2. Login
    login_data = {
        "username": "newuser",
        "password": "securepassword"
    }
    resp = client.post("/api/v1/auth/login", json=login_data)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
    token = data["access_token"]
    
    # 3. Access Protected Route
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/api/v1/users/me", headers=headers)
    assert resp.status_code == 200
    user_data = resp.get_json()
    assert user_data["username"] == "newuser"

def test_login_invalid_credentials(client):
    """Test login with wrong password."""
    # Register first
    client.post("/api/v1/auth/register", json={
        "username": "user2",
        "email": "user2@example.com",
        "password": "password"
    })
    
    # Try login with wrong password
    resp = client.post("/api/v1/auth/login", json={
        "username": "user2",
        "password": "wrongpassword"
    })
    assert resp.status_code == 401
