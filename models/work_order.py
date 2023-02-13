from sqlalchemy import Column, ForeignKey, Integer, String, Enum

from models.customer import Customer
from db import db
from models.enums.work_order_type import WorkOrderType


class WorkOrder(db.Model):
    __tablename__ = "work_orders"
    id = Column(Integer, primary_key=True)
    work_order_type = Column(Enum(WorkOrderType))
    schedule = Column(String)
    customer = Column(ForeignKey('customers.id'))


    def to_dict(self):
        return {
            "id": self.id,
            "work_order_type": self.work_order_type.value,
            "schedule": self.schedule,
            "customer": Customer.query.get(self.customer).to_dict(),
        }
