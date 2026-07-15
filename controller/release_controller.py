from model.enums import OrderStatus


class ReleaseController:
    def __init__(self, order_repository):
        self.order_repository = order_repository

    def list_confirmed_orders(self):
        return self.order_repository.list_by_status(OrderStatus.CONFIRMED)

    def release_order(self, order_id):
        order = self.order_repository.get(order_id)
        if order is None or order.status != OrderStatus.CONFIRMED:
            return False, "출고할 수 없는 주문입니다."
        order.status = OrderStatus.RELEASE
        self.order_repository.save()
        return True, order
