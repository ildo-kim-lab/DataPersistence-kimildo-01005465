from model.order import Order
from model.enums import OrderStatus
from model.production_line import ProductionJob


class OrderController:
    def __init__(self, order_repository, sample_repository, production_line):
        self.order_repository = order_repository
        self.sample_repository = sample_repository
        self.production_line = production_line

    def reserve_order(self, sample_id, customer_name, quantity):
        sample = self.sample_repository.get(sample_id)
        if sample is None:
            return False, f"등록되지 않은 시료입니다: {sample_id}"
        if quantity <= 0:
            return False, "주문 수량은 1 이상이어야 합니다."
        order = Order(sample_id, customer_name, quantity)
        self.order_repository.add(order)
        return True, order

    def list_reserved_orders(self):
        return self.order_repository.list_by_status(OrderStatus.RESERVED)

    def reject_order(self, order_id):
        order = self.order_repository.get(order_id)
        if order is None or order.status != OrderStatus.RESERVED:
            return False, "거절할 수 없는 주문입니다."
        order.status = OrderStatus.REJECTED
        self.order_repository.save()
        return True, order

    def approve_order(self, order_id):
        order = self.order_repository.get(order_id)
        if order is None or order.status != OrderStatus.RESERVED:
            return False, "승인할 수 없는 주문입니다."

        sample = self.sample_repository.get(order.sample_id)
        if sample.stock >= order.quantity:
            sample.stock -= order.quantity
            order.status = OrderStatus.CONFIRMED
            self.sample_repository.save()
            self.order_repository.save()
            return True, order

        shortage = order.quantity - sample.stock
        order.status = OrderStatus.PRODUCING
        job = ProductionJob(order, sample, shortage)
        self.production_line.enqueue(job)
        self.order_repository.save()
        return True, order
