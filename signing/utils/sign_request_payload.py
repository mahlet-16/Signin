import base64
import json
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

SCRIPT_DIR = Path(__file__).parent
PRIVATE_KEY_PATH = SCRIPT_DIR / "private_key.key"


def sign_request_payload(payload_to_sign, private_key_path=PRIVATE_KEY_PATH):
    try:
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
        canonical_payload = json.dumps(payload_to_sign, separators=(",", ":")).encode(
            "utf-8"
        )

        signature = private_key.sign(
            canonical_payload, padding.PKCS1v15(), hashes.SHA512()
        )

        return base64.b64encode(signature).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: Private key file not found at {private_key_path}")
        return None
    except Exception as e:
        print(f"Error signing payload: {e}")
        return None
