from ariadne import convert_kwargs_to_snake_case

from validation.validators import Validator
from models.work_order import WorkOrder
from models.customer import Customer
from db import db


def resolve_customers(obj, info) -> object | None:
    return [customer.to_dict() for customer in Customer.query.all()]


def resolve_work_orders(obj, info) -> object | None:
    return [work_order.to_dict() for work_order in WorkOrder.query.all()]


@convert_kwargs_to_snake_case
def resolve_customer(obj, info, customer_id) -> object | None:
    customer = Customer.query.get(customer_id)
    if customer:
        return customer.to_dict()
    return None


@convert_kwargs_to_snake_case
def resolve_work_order(obj, info, work_order_id) -> object | None:
    work_order = WorkOrder.query.get(work_order_id)
    if work_order:
        return work_order.to_dict()
    return None


@convert_kwargs_to_snake_case
def resolve_create_customer(obj, info, first_name, last_name, address, phone_number, email_address) -> object:
    validator = Validator(db)
    customer_fields = {
        'first_name': first_name,
        'last_name': last_name,
        'address': address,
        'phone_number': phone_number,
        'email_address': email_address
    }
    errors = validator.validate_customer(**customer_fields)
    if errors:
        return {"errors": errors}
    customer = Customer(**customer_fields)
    db.session.add(customer)
    db.session.commit()

    return {"customer": customer.to_dict()}


@convert_kwargs_to_snake_case
def resolve_create_work_order(obj, info, work_order_type, schedule, customer_id) -> object:
    validator = Validator(db)
    work_order_fields = {
        "customer_id": customer_id,
        "schedule": schedule,
        "work_order_type": work_order_type
    }
    errors = validator.validate_work_order(**work_order_fields)
    if errors:
        return {"errors": errors}
    customer = Customer.query.get(customer_id)
    work_order = WorkOrder(customer=customer.id,
                           work_order_type=work_order_type, schedule=schedule)
    db.session.add(work_order)
    db.session.commit()
    return {"work_order": work_order.to_dict()}
