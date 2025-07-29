from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from models.session import Base


class SellerDetails(Base):
    __tablename__ = "seller_details"

    id = Column(Integer, primary_key=True, index=True)

    legal_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    region = Column(String, nullable=True)
    tin = Column(String, nullable=False, unique=True)
    vat_number = Column(String, nullable=True)
    wereda = Column(String, nullable=True)
    city = Column(String, nullable=True, default=None)
    email = Column(String, nullable=True)
    house_number = Column(String, nullable=True, default=None)
    locality = Column(String, nullable=True, default=None)
    sub_city = Column(String, nullable=True, default=None)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
