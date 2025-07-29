from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from models.session import Base


class LoginResponse(Base):
    __tablename__ = "login_responses"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
    encryption_key = Column(String)
    expires_in = Column(String)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
