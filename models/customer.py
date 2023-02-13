from sqlalchemy import Column, Integer, String
from ..db import db

class Customer(db.Model):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    email_address = Column(String)
    phone_number = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "email_address": self.email_address,
            "phone_number": self.phone_number
        }
