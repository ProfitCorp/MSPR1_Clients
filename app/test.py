import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models import CustomerDB
from auth.auth import create_access_token

# Base SQLite pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override la dépendance get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Applique le override à l'app
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Création de 2 users pour les tests
    admin_user = CustomerDB(username="admin", password="adminpass", role="admin")
    normal_user = CustomerDB(username="user", password="userpass", role="user")
    db.add_all([admin_user, normal_user])
    db.commit()
    yield
    db.close()

def get_token(username, role, user_id):
    return create_access_token({"sub": username, "role": role, "user_id": user_id})

def auth_headers(username, role, user_id):
    token = get_token(username, role, user_id)
    return {"Authorization": f"Bearer {token}"}

# ----------------------------
# GET /customers
# ----------------------------
def test_get_customers_as_admin():
    headers = auth_headers("admin", "admin", 1)
    response = client.get("/customers/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2

def test_get_customers_as_user():
    headers = auth_headers("user", "user", 2)
    response = client.get("/customers/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "user"

# ----------------------------
# POST /customers
# ----------------------------
def test_create_customer_as_admin():
    headers = auth_headers("admin", "admin", 1)
    payload = {
        "username": "newuser",
        "password": "pass",
        "firstName": "Alice",
        "lastName": "Bob",
        "address": {
            "streetNumber": "42",
            "street": "Rue de Python",
            "postalCode": "75000",
            "city": "Paris"
        },
        "companyName": "ACME",
        "orders": []
    }
    response = client.post("/customers/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"

def test_create_customer_invalid_field():
    headers = auth_headers("admin", "admin", 1)
    payload = {
        "username": "broken",
        "password": "pass",
        "firstName": "Bad",
        "lastName": "Input",
        "address": {
            "streetNumber": 999,  # Mauvais type : int au lieu de str
            "street": "Broken",
            "postalCode": "00000",
            "city": "Null"
        },
        "companyName": "Broken Inc",
        "orders": []
    }
    response = client.post("/customers/", json=payload, headers=headers)
    assert response.status_code == 422

# ----------------------------
# PUT /customers/{id}
# ----------------------------
def test_update_customer_as_admin():
    headers = auth_headers("admin", "admin", 1)
    payload = {
        "username": "user",
        "password": "updatedpass",
        "firstName": "Updated",
        "lastName": "User",
        "address": {
            "streetNumber": "99",
            "street": "UpdateStreet",
            "postalCode": "12345",
            "city": "UpdateCity"
        },
        "companyName": "Updated Co",
        "orders": []
    }
    response = client.put("/customers/2", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["firstName"] == "Updated"

def test_update_customer_as_user_own_account():
    headers = auth_headers("user", "user", 2)
    payload = {
        "username": "user",
        "password": "newpass",
        "firstName": "User",
        "lastName": "Changed",
        "address": {
            "streetNumber": "1",
            "street": "Rue Modif",
            "postalCode": "75001",
            "city": "Paris"
        },
        "companyName": "MyCompany",
        "orders": []
    }
    response = client.put("/customers/2", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["lastName"] == "Changed"

def test_update_customer_as_user_other_account():
    headers = auth_headers("user", "user", 2)
    response = client.put("/customers/1", json={}, headers=headers)
    assert response.status_code == 403

# ----------------------------
# DELETE /customers/{id}
# ----------------------------
def test_delete_customer_as_admin():
    headers = auth_headers("admin", "admin", 1)
    response = client.delete("/customers/2", headers=headers)
    assert response.status_code == 200

def test_delete_customer_as_user_own_account():
    headers = auth_headers("user", "user", 2)
    response = client.delete("/customers/2", headers=headers)
    assert response.status_code == 200

def test_delete_customer_as_user_other_account():
    headers = auth_headers("user", "user", 2)
    response = client.delete("/customers/1", headers=headers)
    assert response.status_code == 403

# ----------------------------
# POST /token
# ----------------------------
def test_token_generation_and_usage():
    from auth.auth import authenticate_user
    db = TestingSessionLocal()
    
    # Préparer un utilisateur admin dans la base si besoin
    user = db.query(CustomerDB).filter_by(username="admin").first()
    if not user:
        from utils.hashing import get_password_hash
        user = CustomerDB(
            username="admin",
            password=get_password_hash("adminpass"),
            role="admin",
            first_name="Admin",
            last_name="Test"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    user = authenticate_user("admin", "adminpass", db)  # ← Corrigé
    assert user is not False

    token = create_access_token({
        "sub": user.username,
        "role": user.role,
        "user_id": user.id
    })
    assert token is not None

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/customers/", headers=headers)
    assert response.status_code == 200
