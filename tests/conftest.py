import pytest
from source import app

@pytest.fixture
def client():
    # app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

@pytest.fixture
def clubs_data():
    clubs = {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    }
    return clubs

@pytest.fixture
def competitions_data():
    competitions = {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    return competitions