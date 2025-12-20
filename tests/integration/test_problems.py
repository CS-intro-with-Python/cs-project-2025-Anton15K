def test_get_problems(client):
    """Test listing problems."""
    resp = client.get("/api/v1/problems")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "items" in data

def test_create_problem_protected(client, token_factory):
    """Test that creating a problem works (assumes open or protected, checking current config)."""
    token = token_factory(user_id=1)
    headers = {"Authorization": f"Bearer {token}"}
    
    problem_data = {
        "cf_id": "1337A",
        "title": "Test Problem"
    }
    resp = client.post("/api/v1/problems", json=problem_data, headers=headers)
    if resp.status_code == 401:
        pass
        
    assert resp.status_code in [201, 200]
    data = resp.get_json()
    assert data["cf_id"] == "1337A"
