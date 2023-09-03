from base_models import Customer
from db import data
from typing import Optional


def get_customer_details(customer_id: int) -> Optional[Customer]:
    for customer in data.customers:
        if customer.customer_id == customer_id:
            return customer
    return None
