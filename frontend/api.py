
import requests

API_BASE_URL = "http://127.0.0.1:8000"


def register_user(username, email, password):
    url = f"{API_BASE_URL}/auth/register"

    payload = {
        "username": username,
        "email": email,
        "password": password
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        return response
    except requests.RequestException:
        return None


def login_user(email, password):
    url = f"{API_BASE_URL}/auth/login"

    payload = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        return response
    except requests.RequestException:
        return None


def get_user_profile(token):
    url = f"{API_BASE_URL}/auth/me"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )
        return response
    except requests.RequestException:
        return None



def get_applications(token, company=None, status=None, location=None):
    url = f"{API_BASE_URL}/applications"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "limit": 100
    }

    if company:
        params["company"] = company

    if status and status != "All":
        params["status"] = status

    if location:
        params["location"] = location

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        return response

    except requests.RequestException:
        return None


def create_application(token, application_data):
    url = f"{API_BASE_URL}/applications"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(
            url,
            json=application_data,
            headers=headers,
            timeout=10
        )

        return response

    except requests.RequestException:
        return None

    

def update_application(token, application_id, application_data):
    url = f"{API_BASE_URL}/applications/{application_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.put(
            url,
            json=application_data,
            headers=headers,
            timeout=10
        )
        return response

    except requests.RequestException:
        return None


def delete_application(token, application_id):
    url = f"{API_BASE_URL}/applications/{application_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(
            url,
            headers=headers,
            timeout=10
        )
        return response

    except requests.RequestException:
        return None
