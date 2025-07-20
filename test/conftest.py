# tests/test_server.py

import pytest
from backend.server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    """Test if home route returns HTTP 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_add_expense_page(client):
    """Test add expense page is accessible"""
    response = client.get('/add')
    assert response.status_code == 200
    assert b"Add New Expense" in response.data
