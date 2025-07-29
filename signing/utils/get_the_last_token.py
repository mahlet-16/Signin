from models import LoginResponse, SessionLocal


def get_the_last_token():
    db = SessionLocal()
    try:
        last_data = db.query(LoginResponse).order_by(LoginResponse.id.desc()).first()
        access_token = last_data.access_token if last_data else None
        refresh_token = last_data.refresh_token if last_data else None
        encryption_key = last_data.encryption_key if last_data else None
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "encryption_key": encryption_key,
        }
    finally:
        db.close()
