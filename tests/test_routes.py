from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_pages_alive():
    routes = [
        "/",
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

def test_admin_redirects_to_login():
    response = client.get(
        "/admin/",
        follow_redirects=False
    )
    assert response.status_code == 302
    assert "/admin/login" in response.headers["location"]