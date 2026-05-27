from urllib.parse import quote

from src.app import activities


def test_unregister_removes_existing_participant(client, valid_activity_name, existing_email):
    # Arrange
    encoded_activity = quote(valid_activity_name, safe="")
    assert existing_email in activities[valid_activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/participants",
        params={"email": existing_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {existing_email} from {valid_activity_name}"
    assert existing_email not in activities[valid_activity_name]["participants"]


def test_unregister_returns_404_for_missing_activity(client, missing_activity_name, new_email):
    # Arrange
    encoded_activity = quote(missing_activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/participants",
        params={"email": new_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_404_when_student_not_signed_up(client, valid_activity_name, new_email):
    # Arrange
    encoded_activity = quote(valid_activity_name, safe="")
    assert new_email not in activities[valid_activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/participants",
        params={"email": new_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Student is not signed up for this activity"
