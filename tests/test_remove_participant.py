"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""

from fastapi.testclient import TestClient


class TestRemoveParticipant:
    """Test cases for removing a participant from an activity."""

    def test_successful_removal_returns_200(self, client: TestClient):
        """
        Test that removing an existing participant returns a 200 status code.
        
        AAA Pattern:
        - Arrange: Prepare an activity with participants
        - Act: DELETE with existing participant email
        - Assert: Status code is 200
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200

    def test_successful_removal_returns_confirmation_message(self, client: TestClient):
        """
        Test that removing a participant returns a confirmation message.
        
        AAA Pattern:
        - Arrange: Prepare an activity and participant to remove
        - Act: DELETE participant and get response JSON
        - Assert: Response contains confirmation message with participant and activity
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Existing participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_removal_deletes_participant_from_activity(self, client: TestClient):
        """
        Test that removing a participant actually deletes them from the activity.
        
        AAA Pattern:
        - Arrange: Prepare activity and participant
        - Act: DELETE participant, then GET activities
        - Assert: Participant no longer appears in activity's participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"  # Existing participant

        # Act
        client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert email not in data[activity_name]["participants"]

    def test_removal_updates_availability_spots(self, client: TestClient):
        """
        Test that removing a participant increases the available spots for the activity.
        
        AAA Pattern:
        - Arrange: Get initial participant count
        - Act: DELETE a participant, then GET activities again
        - Assert: Participant count decreases by 1
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Get initial count
        response_before = client.get("/activities")
        initial_count = len(response_before.json()[activity_name]["participants"])

        # Act
        client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        response_after = client.get("/activities")
        final_count = len(response_after.json()[activity_name]["participants"])

        # Assert
        assert final_count == initial_count - 1

    def test_remove_nonexistent_participant_returns_404(self, client: TestClient):
        """
        Test that removing a participant not in the activity returns 404 Not Found.
        
        AAA Pattern:
        - Arrange: Prepare a participant not in the activity
        - Act: DELETE with nonexistent participant email
        - Assert: Status code is 404
        """
        # Arrange
        activity_name = "Chess Club"
        nonexistent_email = "notamember@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{nonexistent_email}"
        )

        # Assert
        assert response.status_code == 404

    def test_remove_nonexistent_participant_returns_error_detail(self, client: TestClient):
        """
        Test that removing a nonexistent participant returns an error detail message.
        
        AAA Pattern:
        - Arrange: Prepare a participant not in the activity
        - Act: DELETE with nonexistent participant email
        - Assert: Response contains "Participant not found" error detail
        """
        # Arrange
        activity_name = "Gym Class"
        nonexistent_email = "stranger@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{nonexistent_email}"
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "Participant not found" in data["detail"]

    def test_remove_from_nonexistent_activity_returns_404(self, client: TestClient):
        """
        Test that removing from a nonexistent activity returns 404 Not Found.
        
        AAA Pattern:
        - Arrange: Prepare a nonexistent activity name
        - Act: DELETE from nonexistent activity
        - Assert: Status code is 404
        """
        # Arrange
        nonexistent_activity = "Fake Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404

    def test_remove_from_nonexistent_activity_returns_error_detail(self, client: TestClient):
        """
        Test that removing from a nonexistent activity returns an error detail message.
        
        AAA Pattern:
        - Arrange: Prepare a nonexistent activity name
        - Act: DELETE from nonexistent activity
        - Assert: Response contains "Activity not found" error detail
        """
        # Arrange
        nonexistent_activity = "Mystery Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/participants/{email}"
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_removal_with_special_characters_in_email(self, client: TestClient):
        """
        Test that removal handles email addresses with special characters (URL encoded).
        
        AAA Pattern:
        - Arrange: Add a participant with special characters, then prepare for removal
        - Act: DELETE with encoded email
        - Assert: Removal succeeds
        """
        # Arrange
        activity_name = "Programming Class"
        email = "special+tag@mergington.edu"
        
        # First, sign up the participant
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
