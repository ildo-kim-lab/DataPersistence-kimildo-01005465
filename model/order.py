from model.enums import OrderStatus


class Order:
    _next_id = 1

    def __init__(self, sample_id, customer_name, quantity, order_id=None, status=None):
        if order_id is None:
            self.order_id = Order._next_id
            Order._next_id += 1
        else:
            self.order_id = order_id
            if order_id >= Order._next_id:
                Order._next_id = order_id + 1
        self.sample_id = sample_id
        self.customer_name = customer_name
        self.quantity = quantity
        self.status = status if status is not None else OrderStatus.RESERVED

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "sample_id": self.sample_id,
            "customer_name": self.customer_name,
            "quantity": self.quantity,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["sample_id"],
            data["customer_name"],
            data["quantity"],
            order_id=data["order_id"],
            status=OrderStatus(data["status"]),
        )
