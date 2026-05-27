import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Restore in-memory activities after each test to keep tests isolated."""
    original_state = copy.deepcopy(activities)

    yield

    activities.clear()
    activities.update(original_state)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def valid_activity_name():
    return "Chess Club"


@pytest.fixture
def missing_activity_name():
    return "Nonexistent Activity"


@pytest.fixture
def existing_email(valid_activity_name):
    return activities[valid_activity_name]["participants"][0]


@pytest.fixture
def new_email():
    return "new.student@mergington.edu"


@pytest.fixture
def full_activity_name():
    activity_name = "Programming Class"
    max_participants = activities[activity_name]["max_participants"]
    activities[activity_name]["participants"] = [
        f"filled{i}@mergington.edu" for i in range(max_participants)
    ]
    return activity_name
