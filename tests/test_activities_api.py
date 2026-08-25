def test_get_activities_returns_activity_catalog(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant_case_insensitive(client):
    # Arrange
    activity_name = "Chess Club"
    first_email = "duplicate@mergington.edu"
    second_email = "DUPLICATE@mergington.edu"

    # Act
    first_signup = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": first_email},
    )
    second_signup = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": second_email},
    )

    # Assert
    assert first_signup.status_code == 200
    assert second_signup.status_code == 400
    assert second_signup.json()["detail"] == "Student is already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "remove.me@mergington.edu"

    # Act
    signup = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    unregister = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email.upper()},
    )
    activities = client.get("/activities").json()

    # Assert
    assert signup.status_code == 200
    assert unregister.status_code == 200
    assert unregister.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-signed-up@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
