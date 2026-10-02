def test_anonymous_access_is_rejected(client):
    response = client.get("/user/home")

    assert response.status_code == 401


def test_successful_and_failed_login(client, user):
    success = client.post(
        "/auth/login",
        data={"username": user["email"], "password": "password123"},
    )
    failure = client.post(
        "/auth/login",
        data={"username": user["email"], "password": "wrong-password"},
    )

    assert success.status_code == 200
    assert success.json()["token_type"] == "bearer"
    assert failure.status_code == 401


def test_regular_user_cannot_open_admin_panel(client, auth_headers):
    response = client.get("/admin/home", headers=auth_headers)

    assert response.status_code == 403


def test_admin_can_open_admin_panel(client, admin_headers):
    response = client.get("/admin/home", headers=admin_headers)

    assert response.status_code == 200


def test_admin_login_requires_admin_role(client, user, admin):
    regular_login = client.post(
        "/auth/admin-login",
        data={"username": user["email"], "password": "password123"},
    )
    admin_login = client.post(
        "/auth/admin-login",
        data={"username": admin["email"], "password": "admin123"},
    )

    assert regular_login.status_code == 401
    assert admin_login.status_code == 200


def test_user_cannot_read_another_users_pet(client, auth_headers):
    other = client.post(
        "/auth/register",
        json={"email": "other@example.com", "password": "password123"},
    )
    other_login = client.post(
        "/auth/login",
        data={"username": "other@example.com", "password": "password123"},
    )
    other_headers = {"Authorization": f"Bearer {other_login.json()['access_token']}"}
    pet = client.post(
        "/pets/",
        headers=other_headers,
        json={"name": " чужий улюбленець", "species": "кіт"},
    )

    assert other.status_code == 200
    assert pet.status_code == 200
    response = client.get(f"/pets/{pet.json()['id']}", headers=auth_headers)

    assert response.status_code == 403
