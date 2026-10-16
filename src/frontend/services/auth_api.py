
import requests

API_BASE_URL = "http://127.0.0.1:8000"


def register_user(email: str, password: str) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/auth/register",
        json={
            "email": email,
            "password": password,
        },
        timeout=10,
    )

    return {
        "status_code": response.status_code,
        "data": response.json(),
    }


def login_user(email: str, password: str) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password,
        },
        timeout=10,
    )

    return {
        "status_code": response.status_code,
        "data": response.json(),
    }
