from Backend.models import User
from werkzeug.security import check_password_hash

def test_user_password_hashing():
    """Test that password hashing works correctly."""
    u = User(username="test", email="test@test.com")
    u.set_password("cat")
    
    assert u.password_hash is not None
    assert check_password_hash(u.password_hash, "cat")
    assert not check_password_hash(u.password_hash, "dog")

def test_user_to_dict():
    """Test user serialization."""
    u = User(username="test", email="test@test.com", rating=1500)
    u.id = 1
    
    data = u.to_dict()
    assert data["username"] == "test"
    assert data["email"] == "test@test.com"
    assert data["rating"] == 1500
    assert "password_hash" not in data
