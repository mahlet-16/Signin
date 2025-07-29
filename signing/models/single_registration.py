from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from models.session import Base


class SingleRegistrationResponse(Base):
    __tablename__ = "single_registrations_response"

    id = Column(Integer, primary_key=True, index=True)
    irn = Column(String)
    ack_date = Column(String)
    status = Column(String)
    signed_qr = Column(Text)
    document_number = Column(String)
    signed_invoice = Column(Text)
    invoice_counter = Column(Integer, index=True)
    conversation_id = Column(String)
    date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
