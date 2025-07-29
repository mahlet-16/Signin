from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from models.session import Base


class RegisterResponse(Base):
    __tablename__ = "register_response"

    id = Column(Integer, primary_key=True)

    irn = Column(String, nullable=True)
    status = Column(String)
    document_number = Column(String, nullable=True)
    signed_qr = Column(Text, nullable=True)
    signed_invoice = Column(Text, nullable=True)
    doc_no = Column(String, nullable=True)
    rule_errors = Column(JSON, nullable=True)
    bulk_response_id = Column(Integer, ForeignKey("bulk_response.id"), nullable=True)
    bulk_response = relationship("BulkResponse", back_populates="register_response")
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class BulkResponse(Base):
    __tablename__ = "bulk_response"

    id = Column(Integer, primary_key=True)
    conversion_id = Column(String, unique=True, index=True)
    conversation_id = Column(String, nullable=True)
    register_response = relationship("RegisterResponse", back_populates="bulk_response")
    received_callback_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
