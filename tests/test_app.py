import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestActivitiesAPI:
    """Test cases for the Mergington High School Activities API"""

    def test_get_activities(self):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == 200

        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0

        # Check that each activity has the required fields
        for name, details in activities.items():
            assert "description" in details
            assert "schedule" in details
            assert "max_participants" in details
            assert "participants" in details
            assert isinstance(details["participants"], list)

    def test_signup_successful(self):
        """Test successful signup for an activity"""
        # Use an activity that exists
        activity_name = "Basketball Team"
        email = "test@student.com"

        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert f"Signed up {email} for {activity_name}" in result["message"]

    def test_signup_activity_not_found(self):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/NonExistentActivity/signup",
            params={"email": "test@student.com"}
        )

        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Activity not found" in result["detail"]

    def test_signup_already_signed_up(self):
        """Test signup when already signed up"""
        activity_name = "Tennis Club"
        email = "sarah@mergington.edu"  # This email is already in the data

        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "Already signed up" in result["detail"]

    def test_unregister_successful(self):
        """Test successful unregister from an activity"""
        activity_name = "Art Club"
        email = "lucas@mergington.edu"  # This email is in the data

        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert f"Unregistered {email} from {activity_name}" in result["message"]

    def test_unregister_activity_not_found(self):
        """Test unregister from non-existent activity"""
        response = client.delete(
            "/activities/NonExistentActivity/unregister",
            params={"email": "test@student.com"}
        )

        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Activity not found" in result["detail"]

    def test_unregister_not_signed_up(self):
        """Test unregister when not signed up"""
        activity_name = "Science Club"
        email = "notsignedup@student.com"

        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "Not signed up" in result["detail"]

    def test_root_redirect(self):
        """Test root endpoint redirects to static index"""
        response = client.get("/", allow_redirects=False)
        assert response.status_code == 307  # Temporary redirect
        assert "/static/index.html" in response.headers["location"]

    def test_signup_updates_participants(self):
        """Test that signup actually adds participant to the activity"""
        activity_name = "Debate Team"
        email = "newsignup@student.com"

        # Get initial participants
        response = client.get("/activities")
        initial_activities = response.json()
        initial_count = len(initial_activities[activity_name]["participants"])

        # Sign up
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Check participants were updated
        response = client.get("/activities")
        updated_activities = response.json()
        updated_count = len(updated_activities[activity_name]["participants"])

        assert updated_count == initial_count + 1
        assert email in updated_activities[activity_name]["participants"]

    def test_unregister_updates_participants(self):
        """Test that unregister actually removes participant from the activity"""
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"  # This email is in the data

        # Get initial participants
        response = client.get("/activities")
        initial_activities = response.json()
        initial_count = len(initial_activities[activity_name]["participants"])

        # Unregister
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Check participants were updated
        response = client.get("/activities")
        updated_activities = response.json()
        updated_count = len(updated_activities[activity_name]["participants"])

        assert updated_count == initial_count - 1
        assert email not in updated_activities[activity_name]["participants"]