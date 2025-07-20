# test/test_routes.py

def test_home_status_ok(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Your Expenses" in resp.data  # string from index.html heading

def test_add_get_form(client):
    resp = client.get("/add")
    assert resp.status_code == 200
    assert b"Add New Expense" in resp.data

# Optional: post an expense (requires real DB)
def test_add_post_creates_expense(client):
    resp = client.post("/add", data={
        "expense_date": "2025-07-20",
        "amount": "123.45",
        "category": "Test",
        "notes": "pytest expense"
    }, follow_redirects=True)
    assert resp.status_code == 200
    # Verify new item appears in HTML
    assert b"123.45" in resp.data
    assert b"Test" in resp.data
