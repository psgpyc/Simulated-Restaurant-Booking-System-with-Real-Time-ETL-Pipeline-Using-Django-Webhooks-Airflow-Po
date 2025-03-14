import logging
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class Customer(BaseModel):
    customer_id: int
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    joined_date: datetime

    @field_validator('*', mode='before')
    @classmethod
    def strip_string(cls, val):
        if isinstance(val, str):
            return val.strip().lower()
        return val

    


class Reservation(BaseModel):
    reservation_id: int
    guest: Customer
    reservation_time: datetime
    experience: str
    size: int
    status: str
    payment_mode: str
    visit_notes: str
    created_at: datetime
    source: str


    @field_validator('*', mode='before')
    @classmethod
    def strip_string(cls, val):
        if isinstance(val, str):
            return val.strip().lower()
        return val