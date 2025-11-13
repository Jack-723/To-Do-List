from fastapi.testclient import TestClient


def test_create_todo(client: TestClient):
    """Test creating a new todo."""
    response = client.post(
        "/todos",
        json={"title": "Test Todo", "description": "Test Description", "done": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["done"] is False
    assert "id" in data


def test_list_todos(client: TestClient):
    """Test listing all todos."""
    # Create a todo first
    client.post(
        "/todos",
        json={"title": "Todo 1", "description": "Desc 1", "done": False}
    )
    
    # List todos
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Todo 1"


def test_get_todo_by_id(client: TestClient):
    """Test getting a specific todo by ID."""
    # Create a todo
    create_response = client.post(
        "/todos",
        json={"title": "Get Me", "description": "Find me", "done": False}
    )
    todo_id = create_response.json()["id"]
    
    # Get the todo
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Get Me"


def test_get_todo_not_found(client: TestClient):
    """Test getting a non-existent todo returns 404."""
    response = client.get("/todos/99999")
    assert response.status_code == 404


def test_update_todo(client: TestClient):
    """Test updating a todo."""
    # Create a todo
    create_response = client.post(
        "/todos",
        json={"title": "Update Me", "description": "Old desc", "done": False}
    )
    todo_id = create_response.json()["id"]
    
    # Update the todo
    response = client.patch(
        f"/todos/{todo_id}",
        json={"title": "Updated Title", "done": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["done"] is True
    assert data["description"] == "Old desc"  # Should remain unchanged


def test_delete_todo(client: TestClient):
    """Test deleting a todo."""
    # Create a todo
    create_response = client.post(
        "/todos",
        json={"title": "Delete Me", "description": "Bye", "done": False}
    )
    todo_id = create_response.json()["id"]
    
    # Delete the todo
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404