import os

import requests
from dotenv import load_dotenv

from utils import get_the_last_token, sign_request_payload

load_dotenv()
API_KEY = os.getenv("API_KEY")
CERTIFICATE = os.getenv("CERTIFICATE")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
TIN = os.getenv("TIN")


def single_cancelation(request_body):
    if not request_body:
        print("Request body is empty. Please provide valid data.")
        return {"error": "Request body is empty. Please provide valid data."}
    if not request_body.get("irn") or not request_body.get("remark"):
        print("Missing required fields in request body.")
        return {"error": "Missing required fields in request body."}

    try:
        tokens = get_the_last_token()
        if not tokens:
            print("No tokens found. Please login first.")
            return {"error": "No tokens found. Please login first."}
        ACCESS_TOKEN = tokens.get("access_token")
        if not ACCESS_TOKEN:
            print("Access token not found in the last tokens.")
            return {"error": "Access token not found in the last tokens."}
    except Exception as e:
        print(f"Error retrieving tokens: {e}")
        return {"error": "Failed to retrieve tokens"}

    url = "https://core.mor.gov.et/v1/cancel"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    request_object = {
        "Irn": request_body.get("irn"),
        "ReasonCode": "1",
        "Remark": request_body.get("remark"),
    }

    signature_b64 = sign_request_payload(request_object)
    if not signature_b64:
        print("Failed to generate signature. Aborting.")
        return {"error": "Failed to sign request"}

    final_payload = {
        "request": request_object,
        "signature": signature_b64,
        "certificate": CERTIFICATE,
    }

    try:
        response = requests.post(url, headers=headers, json=final_payload)
        response.raise_for_status()
        json_data = response.json()
        return json_data

    except requests.exceptions.HTTPError as err:
        return {"error": err.response.text}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
