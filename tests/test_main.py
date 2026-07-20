import pytest
from fastapi.testclient import TestClient

from main import app, comments

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_comments():
    """Clear comments before each test"""
    comments.clear()
    yield
    comments.clear()


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_comments_empty():
    """Test getting comments when list is empty"""
    response = client.get("/comments")
    assert response.status_code == 200
    assert response.json() == []


def test_create_comment():
    """Test creating a new comment"""
    response = client.post(
        "/comments",
        json={"author": "Test Author", "text": "Test Comment"},
    )
    assert response.status_code == 200
    assert response.json() == {"author": "Test Author", "text": "Test Comment"}


def test_create_and_get_comments():
    """Test creating a comment and retrieving it"""
    # Create a comment
    client.post(
        "/comments",
        json={"author": "Jane Doe", "text": "Hello World!"},
    )

    # Get comments
    response = client.get("/comments")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == {"author": "Jane Doe", "text": "Hello World!"}


def test_create_multiple_comments():
    """Test creating multiple comments"""
    client.post("/comments", json={"author": "User 1", "text": "First comment"})
    client.post("/comments", json={"author": "User 2", "text": "Second comment"})

    response = client.get("/comments")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_invalid_comment_missing_author():
    """Test creating a comment without author fails"""
    response = client.post(
        "/comments",
        json={"text": "Comment without author"},
    )
    assert response.status_code == 422  # Validation error


def test_invalid_comment_missing_text():
    """Test creating a comment without text fails"""
    response = client.post(
        "/comments",
        json={"author": "Author"},
    )
    assert response.status_code == 422  # Validation error
