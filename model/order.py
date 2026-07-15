from model.enums import OrderStatus


class Order:
    _next_id = 1

    def __init__(self, sample_id, customer_name, quantity):
        self.order_id = Order._next_id
        Order._next_id += 1
        self.sample_id = sample_id
        self.customer_name = customer_name
        self.quantity = quantity
        self.status = OrderStatus.RESERVED
