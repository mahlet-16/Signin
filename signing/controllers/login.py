import os

from dotenv import load_dotenv

from models import LoginResponse, SessionLocal

load_dotenv()
import requests

from utils import sign_request_payload

API_KEY = os.getenv("API_KEY")
CERTIFICATE = os.getenv("CERTIFICATE")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
TIN = os.getenv("TIN")


def login():
    url = "https://core.mor.gov.et/auth/login"
    headers = {
        "Content-Type": "application/json",
    }

    request_object = {
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET,
        "apikey": API_KEY,
        "tin": TIN,
    }

    signature_b64 = sign_request_payload(request_object)

    if not signature_b64:
        print("Failed to generate signature. Aborting.")
        return {"error": "Failed to sign request"}

    final_payload = {
        "request": request_object,
        "certificate": CERTIFICATE,
        "signature": signature_b64,
    }

    try:

        response = requests.post(url, headers=headers, json=final_payload)
        response.raise_for_status()

        json_data = response.json()

        db = SessionLocal()
        login_record = LoginResponse(
            access_token=json_data["data"].get("accessToken"),
            refresh_token=json_data["data"].get("refreshToken"),
            encryption_key=json_data["data"].get("encryptionKey"),
            expires_in=json_data["data"].get("expiresIn"),
        )
        db.add(login_record)
        db.commit()
        db.refresh(login_record)
        db.close()

        return json_data

    except requests.exceptions.HTTPError as err:
        print("Response Body:", err.response.text)
        return {"error": err.response.text}
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}
