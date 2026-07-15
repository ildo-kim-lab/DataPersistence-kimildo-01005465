from model.enums import OrderStatus


class SampleRepository:
    def __init__(self):
        self._samples = {}

    def add(self, sample):
        self._samples[sample.sample_id] = sample

    def get(self, sample_id):
        return self._samples.get(sample_id)

    def exists(self, sample_id):
        return sample_id in self._samples

    def list_all(self):
        return list(self._samples.values())

    def search_by_name(self, keyword):
        return [s for s in self._samples.values() if keyword.lower() in s.name.lower()]


class OrderRepository:
    def __init__(self):
        self._orders = {}

    def add(self, order):
        self._orders[order.order_id] = order

    def get(self, order_id):
        return self._orders.get(order_id)

    def list_all(self):
        return list(self._orders.values())

    def list_by_status(self, status: OrderStatus):
        return [o for o in self._orders.values() if o.status == status]
