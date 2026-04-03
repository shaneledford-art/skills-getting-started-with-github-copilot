"""Pytest configuration and shared fixtures for API tests."""

import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any, Generator

from src.app import app, get_activities_db


@pytest.fixture
def test_activities() -> Dict[str, Any]:
    """
    Provide a fresh copy of the activities database for each test.
    This ensures test isolation and prevents state leakage between tests.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
    }


@pytest.fixture
def client(test_activities: Dict[str, Any]) -> Generator[TestClient, None, None]:
    """
    Provide a TestClient with a clean, isolated activities database.
    Each test gets its own copy of the database via dependency override.
    """
    # Override the get_activities_db dependency to use test data
    app.dependency_overrides[get_activities_db] = lambda: test_activities
    
    yield TestClient(app)
    
    # Clean up: remove the override after the test
    app.dependency_overrides.clear()
