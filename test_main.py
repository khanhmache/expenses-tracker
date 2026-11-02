
from fastapi.testclient import TestClient
import main
import pytest

@pytest.fixture
def client():
    main.expenses.clear()
    main.next_id = 1

    with TestClient(main.app) as test_client:
        yield test_client

    main.expenses.clear()
    main.next_id = 1

def test_create_post(client):
    response = client.post(
        "/expenses",
        json={
            "title": "Mua sách",
            "amount": 100000
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Mua sách"
    assert data["amount"] == 100000
    assert data["category"] == "Khac"

def test_get_expenses(client):
    created = client.post(
        "/expenses",
        json={
            "title": "Mua bút",
            "amount": 20000
        }
    )

    response = client.get("/expenses")

    assert response.status_code == 200

    data = response.json()

    assert len(data["expenses"]) == 1
    assert created.json() in data["expenses"]

def test_update_expense(client):
    posted = client.post(
        "/expenses",
        json={
            "title": "Cocktail",
            "amount": 300000
        }
    )
    assert posted.status_code == 201
    expense_id = posted.json()["id"]

    updated = client.patch(
        f"/expenses/{expense_id}",
        json={
            "amount": 250000
        }
    )
    assert updated.status_code == 200

    assert updated.json()["amount"] == 250000

    response = client.get("/expenses")

    assert response.status_code == 200

    assert response.json()["expenses"][0]["amount"] == 250000

def test_delete_expense(client):
    created = client.post(
        "/expenses",
        json={
            "title": "Mua sách",
            "amount": 100000
        }
    )


    assert created.status_code == 201

    expense_id = created.json()["id"]

    deleted = client.delete(f"/expenses/{expense_id}")

    assert deleted.status_code == 200

    response = client.get("/expenses")

    assert response.status_code == 200

    assert len(response.json()["expenses"]) == 0 



# GET khi không có khoản chi
def test_get_empty(client):
    response = client.get("/expenses")

    assert response.status_code == 200
    assert response.json() == {"expenses": []}


# PATCH với ID không tồn tại
def test_patch_not_found(client):
    response = client.patch(
        "/expenses/999",
        json={"amount": 200000}
    )

    assert response.status_code == 404


# DELETE với ID không tồn tại
def test_delete_not_found(client):
    response = client.delete("/expenses/999")

    assert response.status_code == 404


# POST với số tiền không hợp lệ
def test_invalid_amount(client):
    response = client.post(
        "/expenses",
        json={
            "title": "Mua sách",
            "amount": -100000
        }
    )

    assert response.status_code == 422

    # Dữ liệu sai không được lưu
    result = client.get("/expenses")
    assert result.json()["expenses"] == []


    