from model.enums import OrderStatus
from model.sample import Sample
from model.order import Order
from model.json_storage import load_json, save_json


class SampleRepository:
    def __init__(self, storage_path=None):
        self._samples = {}
        self.storage_path = storage_path
        if storage_path:
            self.load()

    def add(self, sample):
        self._samples[sample.sample_id] = sample
        self._save()

    def get(self, sample_id):
        return self._samples.get(sample_id)

    def exists(self, sample_id):
        return sample_id in self._samples

    def list_all(self):
        return list(self._samples.values())

    def search_by_name(self, keyword):
        return [s for s in self._samples.values() if keyword.lower() in s.name.lower()]

    def update(self, sample_id, **fields):
        sample = self._samples.get(sample_id)
        if sample is None:
            return None
        for key, value in fields.items():
            setattr(sample, key, value)
        self._save()
        return sample

    def delete(self, sample_id):
        sample = self._samples.pop(sample_id, None)
        if sample is not None:
            self._save()
        return sample

    def save(self):
        self._save()

    def load(self):
        data = load_json(self.storage_path, [])
        self._samples = {d["sample_id"]: Sample.from_dict(d) for d in data}

    def _save(self):
        if self.storage_path:
            save_json(self.storage_path, [s.to_dict() for s in self._samples.values()])


class OrderRepository:
    def __init__(self, storage_path=None):
        self._orders = {}
        self.storage_path = storage_path
        if storage_path:
            self.load()

    def add(self, order):
        self._orders[order.order_id] = order
        self._save()

    def get(self, order_id):
        return self._orders.get(order_id)

    def list_all(self):
        return list(self._orders.values())

    def list_by_status(self, status: OrderStatus):
        return [o for o in self._orders.values() if o.status == status]

    def update(self, order_id, **fields):
        order = self._orders.get(order_id)
        if order is None:
            return None
        for key, value in fields.items():
            setattr(order, key, value)
        self._save()
        return order

    def delete(self, order_id):
        order = self._orders.pop(order_id, None)
        if order is not None:
            self._save()
        return order

    def save(self):
        self._save()

    def load(self):
        data = load_json(self.storage_path, [])
        self._orders = {}
        for d in data:
            order = Order.from_dict(d)
            self._orders[order.order_id] = order

    def _save(self):
        if self.storage_path:
            save_json(self.storage_path, [o.to_dict() for o in self._orders.values()])
