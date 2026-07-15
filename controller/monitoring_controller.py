from model.enums import OrderStatus

_ACTIVE_STATUSES = (OrderStatus.RESERVED, OrderStatus.PRODUCING, OrderStatus.CONFIRMED)
_MONITORED_STATUSES = (OrderStatus.RESERVED, OrderStatus.PRODUCING,
                        OrderStatus.CONFIRMED, OrderStatus.RELEASE)


class MonitoringController:
    """REJECTED는 정상 흐름 밖의 상태이므로 모니터링에서 제외한다."""

    def __init__(self, order_repository, sample_repository):
        self.order_repository = order_repository
        self.sample_repository = sample_repository

    def order_counts(self):
        return {
            status: len(self.order_repository.list_by_status(status))
            for status in _MONITORED_STATUSES
        }

    def stock_status(self):
        result = []
        for sample in self.sample_repository.list_all():
            demand = sum(
                o.quantity for o in self.order_repository.list_all()
                if o.sample_id == sample.sample_id and o.status in _ACTIVE_STATUSES
            )
            if sample.stock <= 0:
                state = "고갈"
            elif sample.stock < demand:
                state = "부족"
            else:
                state = "여유"
            result.append((sample, demand, state))
        return result
