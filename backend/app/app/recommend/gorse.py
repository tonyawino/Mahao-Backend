from typing import List, Any, Optional

import requests

from app.core.config import settings

from app.schemas.gorse_feedback import GorseFeedback
from fastapi.encoders import jsonable_encoder

from app.schemas.gorse_item import GorseItem
from app.schemas.gorse_user import GorseUser

from app.schemas.feedback_type import FeedbackType

url = f"{settings.GORSE_API_URL}/api/"
header = {"X-API-Key": ""}
session = requests.Session()


def get_results(endpoint: str, params: dict):
    try:
        r = session.get(f"{url}{endpoint}", params=params,
                        headers=header)
        if r.status_code == 200:
            return r.json()
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")


def insert_feedback(feedbacks: List[GorseFeedback]) -> Any:
    endpoint = "feedback"
    try:
        feedback_json = jsonable_encoder(feedbacks)
        for feedback in feedback_json:
            timestamp = feedback["Timestamp"]
            feedback["Timestamp"] = f"{timestamp[:len(timestamp) - 3]}Z"
        r = session.put(f"{url}{endpoint}", json=feedback_json,
                        headers=header)
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")


def remove_feedback(user_id: int, item_id: int, feedback_type: str) -> Any:
    endpoint = f"feedback/{str(feedback_type).lower()}/{user_id}/{item_id}"
    try:
        r = session.delete(f"{url}{endpoint}", headers=header)
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")


def get_users_collaborative(user_id: int, category: Optional[int] = None, skip: int = 0, limit: int = 0) -> Any:
    endpoint = f"intermediate/recommend/{user_id}"
    if category:
        endpoint = f"intermediate/recommend/{user_id}/{category}"
    params = {"n": limit, "offset": skip}
    return get_results(endpoint, params)


def insert_item(item: GorseItem) -> Any:
    endpoint = "item"
    try:
        item_json = jsonable_encoder(item)
        timestamp = item_json["Timestamp"]
        item_json["Timestamp"] = f"{timestamp[:len(timestamp)-3]}Z"
        r = session.post(f"{url}{endpoint}", json=item_json,
                         headers=header)
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")


def remove_item(item_id: int) -> Any:
    endpoint = f"item/{item_id}"
    try:
        r = session.delete(f"{url}{endpoint}", headers=header)
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")


def update_item(item_id: int, item: GorseItem) -> Any:
    endpoint = f"item/{item_id}"
    try:
        item_json = jsonable_encoder(item)
        timestamp = item_json["Timestamp"]
        item_json["Timestamp"] = f"{timestamp[:len(timestamp)-3]}Z"
        print(f"Item Sent {item_json}")
        r = session.patch(f"{url}{endpoint}", json=item_json,
                          headers=header)
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")


def add_category_to_item(item_id: int, category: int) -> Any:
    endpoint = f"item/{item_id}/category/{category}"
    try:
        r = session.put(f"{url}{endpoint}", headers=header)
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")


def remove_category_from_item(item_id: int, category: int) -> Any:
    endpoint = f"item/{item_id}/category/{category}"
    try:
        r = session.delete(f"{url}{endpoint}", headers=header)
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")


def get_item_neighbors(item_id: int, category: Optional[int] = None, skip: int = 0, limit: int = 0) -> Any:
    endpoint = f"item/{item_id}/neighbors"
    if category:
        endpoint = f"item/{item_id}/neighbors/{category}"
    params = {"n": limit, "offset": skip}
    return get_results(endpoint, params)


def get_latest_items(category: Optional[int] = None, skip: int = 0, limit: int = 0) -> Any:
    endpoint = f"latest"
    if category:
        endpoint = f"latest/{category}"
    params = {"n": limit, "offset": skip}
    return get_results(endpoint, params)


def get_popular_items(category: Optional[int] = None, skip: int = 0, limit: int = 0) -> Any:
    endpoint = f"popular"
    if category:
        endpoint = f"popular/{category}"
    params = {"n": limit, "offset": skip}
    return get_results(endpoint, params)


def get_recommended_items(user_id: int, category: Optional[int] = None, skip: int = 0, limit: int = 0) -> Any:
    endpoint = f"recommend/{user_id}"
    if category:
        endpoint = f"recommend/{user_id}/{category}"
    params = {"n": limit, "offset": skip}
    return get_results(endpoint, params)


def insert_user(user: GorseUser) -> Any:
    print(f"User {jsonable_encoder(user)}")
    endpoint = "user"
    try:
        r = session.post(f"{url}{endpoint}", json=jsonable_encoder(user),
                         headers=header)
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")


def remove_user(user_id: int) -> Any:
    endpoint = f"user/{user_id}"
    try:
        r = session.delete(f"{url}{endpoint}", headers=header)
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")


def update_user(user_id: int, user: GorseUser) -> Any:
    endpoint = f"user/{user_id}"
    try:
        r = session.patch(f"{url}{endpoint}", json=jsonable_encoder(user),
                          headers=header)
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")


def insert_users(users: List[GorseUser]) -> Any:
    endpoint = "users"
    try:
        r = session.post(f"{url}{endpoint}", json=jsonable_encoder(users),
                         headers=header)
    except ConnectionRefusedError:
        print("Unable to connect to Gorse Server")
