from urllib.parse import quote

from src.app import activities


def test_signup_successfully_adds_student(client, valid_activity_name, new_email):
    # Arrange
    encoded_activity = quote(valid_activity_name, safe="")
    assert new_email not in activities[valid_activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": new_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {new_email} for {valid_activity_name}"
    assert new_email in activities[valid_activity_name]["participants"]


def test_signup_returns_404_for_missing_activity(client, missing_activity_name, new_email):
    # Arrange
    encoded_activity = quote(missing_activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": new_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_when_already_registered(client, valid_activity_name, existing_email):
    # Arrange
    encoded_activity = quote(valid_activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": existing_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_returns_400_when_activity_is_full(client, full_activity_name, new_email):
    # Arrange
    encoded_activity = quote(full_activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": new_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Activity is full"
