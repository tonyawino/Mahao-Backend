from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.category import create_random_property_category


def test_create_category(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/property_categories/", headers=superuser_token_headers, data=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content


def test_read_category(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    item = create_random_property_category(db)
    response = client.get(
        f"{settings.API_V1_STR}/property_categories/{item.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == item.id
