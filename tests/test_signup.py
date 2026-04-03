"""Tests for POST /activities/{activity_name}/signup endpoint."""

from fastapi.testclient import TestClient
from typing import Dict, Any


class TestSignupForActivity:
    """Test cases for signing up a student for an activity."""

    def test_successful_signup_returns_200(self, client: TestClient):
        """
        Test that signing up a new student returns a 200 status code.
        
        AAA Pattern:
        - Arrange: Prepare activity name and new email
        - Act: POST to signup endpoint
        - Assert: Status code is 200
        """
        # Arrange
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200

    def test_successful_signup_returns_confirmation_message(self, client: TestClient):
        """
        Test that a successful signup returns a confirmation message.
        
        AAA Pattern:
        - Arrange: Prepare activity name and new email
        - Act: POST to signup endpoint and get response JSON
        - Assert: Response contains success message
        """
        # Arrange
        activity_name = "Gym Class"
        email = "athlete@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client: TestClient, test_activities: Dict[str, Any]):
        """
        Test that signing up actually adds the participant to the activity.
        
        AAA Pattern:
        - Arrange: Prepare activity name and new email
        - Act: POST to signup endpoint, then GET activities
        - Assert: New participant appears in activity participants list
        """
        # Arrange
        activity_name = "Gym Class"
        email = "newathlete@mergington.edu"

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert email in data[activity_name]["participants"]

    def test_duplicate_signup_returns_400(self, client: TestClient):
        """
        Test that signing up with an email already registered returns 400 Bad Request.
        
        AAA Pattern:
        - Arrange: Use an email already in the activity's participants
        - Act: POST to signup endpoint with duplicate email
        - Assert: Status code is 400
        """
        # Arrange
        activity_name = "Chess Club"
        duplicate_email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": duplicate_email}
        )

        # Assert
        assert response.status_code == 400

    def test_duplicate_signup_returns_error_message(self, client: TestClient):
        """
        Test that a duplicate signup attempt returns an appropriate error message.
        
        AAA Pattern:
        - Arrange: Use an email already in the activity's participants
        - Act: POST to signup endpoint with duplicate email
        - Assert: Response contains "already signed up" error detail
        """
        # Arrange
        activity_name = "Chess Club"
        duplicate_email = "daniel@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": duplicate_email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_nonexistent_activity_returns_404(self, client: TestClient):
        """
        Test that signing up for a nonexistent activity returns 404 Not Found.
        
        AAA Pattern:
        - Arrange: Use a nonexistent activity name
        - Act: POST to signup endpoint with invalid activity
        - Assert: Status code is 404
        """
        # Arrange
        nonexistent_activity = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404

    def test_signup_nonexistent_activity_returns_error_detail(self, client: TestClient):
        """
        Test that signing up for a nonexistent activity returns an error detail message.
        
        AAA Pattern:
        - Arrange: Use a nonexistent activity name
        - Act: POST to signup endpoint with invalid activity
        - Assert: Response contains "Activity not found" error detail
        """
        # Arrange
        nonexistent_activity = "Unknown Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_with_special_characters_in_email(self, client: TestClient):
        """
        Test that signup handles email addresses with special characters (URL encoded).
        
        AAA Pattern:
        - Arrange: Prepare an email with special characters
        - Act: POST to signup endpoint with encoded email
        - Assert: Signup succeeds
        """
        # Arrange
        activity_name = "Programming Class"
        email = "student+tag@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
