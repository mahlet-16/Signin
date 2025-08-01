from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class SingleRegistrationResponseBase(BaseModel):
    irn: Optional[str]
    ack_date: Optional[str]
    status: Optional[str]
    signed_qr: Optional[str]
    document_number: Optional[str]
    signed_invoice: Optional[str]
    invoice_counter: Optional[int]
    conversation_id: Optional[str]
    date: Optional[datetime]


class SingleRegistrationResponseOut(SingleRegistrationResponseBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class SellerDetailsBase(BaseModel):
    legal_name: str
    phone: Optional[str]
    region: Optional[str]
    tin: str
    vat_number: Optional[str]
    wereda: Optional[str]
    city: Optional[str] = None
    email: Optional[str]
    house_number: Optional[str] = None
    locality: Optional[str] = None
    sub_city: Optional[str] = None


class SellerDetailsOut(SellerDetailsBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RegisterResponseBase(BaseModel):
    irn: Optional[str]
    status: str
    document_number: Optional[str]
    signed_qr: Optional[str]
    signed_invoice: Optional[str]
    doc_no: Optional[str]
    rule_errors: Optional[Any]
    bulk_response_id: Optional[int]


class RegisterResponseOut(RegisterResponseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BulkResponseBase(BaseModel):
    conversion_id: str
    conversation_id: Optional[str]


class BulkResponseOut(BulkResponseBase):
    id: int
    received_callback_at: datetime
    register_response: Optional[List[RegisterResponseOut]]  # if nested response needed

    class Config:
        orm_mode = True


class LoginResponseOut(BaseModel):
    id: int
    access_token: str
    refresh_token: str
    encryption_key: str
    expires_in: str
    created_at: datetime

    class Config:
        orm_mode = True
