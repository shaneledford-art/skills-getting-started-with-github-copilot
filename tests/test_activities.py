"""Tests for GET /activities endpoint."""

from fastapi.testclient import TestClient


class TestGetActivities:
    """Test cases for retrieving all available activities."""

    def test_get_all_activities_returns_success(self, client: TestClient):
        """
        Test that GET /activities returns a 200 status code.
        
        AAA Pattern:
        - Arrange: Use fixture-provided client
        - Act: Make GET request to /activities
        - Assert: Status code is 200
        """
        # Arrange
        # Client is provided by the fixture

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_all_activities_returns_dict(self, client: TestClient):
        """
        Test that GET /activities returns a dictionary structure.
        
        AAA Pattern:
        - Arrange: Use fixture-provided client
        - Act: Make GET request to /activities
        - Assert: Response is a dictionary
        """
        # Arrange
        # Client is provided by the fixture

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)

    def test_get_activities_contains_expected_activities(self, client: TestClient):
        """
        Test that GET /activities returns the activities from test fixtures.
        
        AAA Pattern:
        - Arrange: Use fixture-provided client
        - Act: Make GET request to /activities
        - Assert: Response contains expected activity keys
        """
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity in expected_activities:
            assert activity in data

    def test_activity_structure_is_correct(self, client: TestClient):
        """
        Test that each activity has the required fields.
        
        AAA Pattern:
        - Arrange: Use fixture-provided client
        - Act: Make GET request to /activities
        - Assert: Each activity has description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_details in data.items():
            assert set(activity_details.keys()) == required_fields
            assert isinstance(activity_details["participants"], list)
            assert isinstance(activity_details["max_participants"], int)

    def test_activity_participants_are_emails(self, client: TestClient):
        """
        Test that participants in the response are email addresses.
        
        AAA Pattern:
        - Arrange: Use fixture-provided client
        - Act: Make GET request to /activities
        - Assert: All participants contain "@" (basic email validation)
        """
        # Arrange
        # Client is provided by the fixture

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_details in data.items():
            for participant in activity_details["participants"]:
                assert "@" in participant
