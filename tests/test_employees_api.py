def test_create_employee(client, employee_payload):
    response = client.post("/employees", json=employee_payload)
    assert response.status_code == 201
    body = response.json()
    assert body["employee_id"] == 1
    assert body["email"] == "dinithi@mail.com"


def test_get_employee(client, employee_payload):
    created = client.post("/employees", json=employee_payload).json()
    response = client.get(f"/employees/{created['employee_id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Dinithi"


def test_update_employee(client, employee_payload):
    created = client.post("/employees", json=employee_payload).json()
    employee_payload["salary"] = 75000
    response = client.put(f"/employees/{created['employee_id']}", json=employee_payload)
    assert response.status_code == 200
    assert response.json()["salary"] == 75000


def test_delete_employee(client, employee_payload):
    created = client.post("/employees", json=employee_payload).json()
    emp_id = created["employee_id"]

    assert client.delete(f"/employees/{emp_id}").status_code == 200
    assert client.get(f"/employees/{emp_id}").status_code == 404   # soft deleted


def test_invalid_employee_id(client):
    response = client.get("/employees/9999")
    assert response.status_code == 404


def test_invalid_salary(client, employee_payload):
    employee_payload["salary"] = -5
    response = client.post("/employees", json=employee_payload)
    assert response.status_code == 422


def test_duplicate_email(client, employee_payload):
    client.post("/employees", json=employee_payload)
    response = client.post("/employees", json=employee_payload)
    assert response.status_code == 409


def test_missing_required_fields(client):
    response = client.post("/employees", json={"name": "NoEmail"})
    assert response.status_code == 422


def test_unknown_department(client, employee_payload):
    employee_payload["department_id"] = 999
    response = client.post("/employees", json=employee_payload)
    assert response.status_code == 404


def test_leave_end_before_start(client, employee_payload):
    emp = client.post("/employees", json=employee_payload).json()
    response = client.post(
        f"/employees/{emp['employee_id']}/leave",
        json={"leave_type": "Annual", "start_date": "2026-11-10", "end_date": "2026-11-01"},
    )
    assert response.status_code == 422