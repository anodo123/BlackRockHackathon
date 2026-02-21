"""
Test type: integration
Validation to be executed: hit endpoints with known data
Command: pytest test/test_api.py
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_parse_and_returns():
    expenses = [
        {"date":"2023-10-12 20:15:30","amount":250},
        {"date":"2023-02-28 15:49:20","amount":375},
        {"date":"2023-07-01 21:59:00","amount":620},
        {"date":"2023-12-17 08:09:45","amount":480},
    ]
    r = client.post("/blackrock/challenge/v1/transactions:parse", json=expenses)
    assert r.status_code == 200
    data = r.json()
    assert data["total_remanent"] == 175.0
    # test returns index
    req = {
        "age":29,
        "wage":50000,
        "inflation":5.5,
        "q":[{"fixed":0,"start":"2023-07-01 00:00:00","end":"2023-07-31 23:59:59"}],
        "p":[{"extra":25,"start":"2023-10-01 08:00:00","end":"2023-12-31 19:59:59"}],
        "k":[
            {"start":"2023-01-01 00:00:00","end":"2023-12-31 23:59:59"},
            {"start":"2023-03-01 00:00:00","end":"2023-11-30 23:59:59"}
        ],
        "transactions": expenses
    }
    r2 = client.post("/blackrock/challenge/v1/returns:index", json=req)
    assert r2.status_code == 200
    out = r2.json()
    assert out["savingsByDates"][0]["amount"] == 145.0
    assert out["savingsByDates"][1]["amount"] == 75.0
