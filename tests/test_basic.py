import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_valid_url(client):
    response = client.post('/api/shorten', json={"url": "https://www.example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data
    assert data["short_url"].endswith(data["short_code"])

def test_shorten_invalid_url(client):
    response = client.post('/api/shorten', json={"url": "not_a_url"})
    assert response.status_code == 400
    data = response.get_json()
    assert "Invalid URL" in data["message"]

def test_redirect_and_click_count(client):
    # Shorten a URL
    response = client.post('/api/shorten', json={"url": "https://www.example.com/page"})
    code = response.get_json()["short_code"]
    # Redirect
    response = client.get(f'/{code}', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "https://www.example.com/page"
    # Stats should show 1 click
    stats = client.get(f'/api/stats/{code}').get_json()
    assert stats["clicks"] == 1

def test_stats_endpoint(client):
    response = client.post('/api/shorten', json={"url": "https://www.example.com"})
    code = response.get_json()["short_code"]
    stats = client.get(f'/api/stats/{code}')
    assert stats.status_code == 200
    data = stats.get_json()
    assert data["url"] == "https://www.example.com"
    assert data["clicks"] == 0
    assert "created_at" in data

def test_404_for_unknown_code(client):
    response = client.get('/api/stats/unknown123')
    assert response.status_code == 404
    data = response.get_json()
    assert "URL not found" in data["message"]
    response = client.get('/unknown123')
    assert response.status_code == 404
    data = response.get_json()
    assert "URL not found" in data["message"]