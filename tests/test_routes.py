from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_pages_alive():
    routes = [
        "/",
        "/admin",
        "/getupdates",
    ]

    for route in routes:
        response = client.get(route)
        assert response.status_code == 200

def test_df1_page():
    response = client.get("/admin/df1/list")
    assert response.status_code == 200

def test_getupdates_page():
    response = client.get("/getupdates")
    assert response.status_code == 200
    assert "Завантаження " in response.text

def test_getupdates_page2():
    response = client.get("/getupdates")
    assert response.status_code == 200
    assert "555Завантаження " not in response.text

def test_unknown_page():
    response = client.get("/this-page-does-not-exist")
    assert response.status_code == 404