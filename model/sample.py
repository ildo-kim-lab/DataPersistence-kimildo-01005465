class Sample:
    def __init__(self, sample_id, name, avg_production_time, yield_rate, stock=0):
        self.sample_id = sample_id
        self.name = name
        self.avg_production_time = avg_production_time
        self.yield_rate = yield_rate
        self.stock = stock

    def to_dict(self):
        return {
            "sample_id": self.sample_id,
            "name": self.name,
            "avg_production_time": self.avg_production_time,
            "yield_rate": self.yield_rate,
            "stock": self.stock,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["sample_id"],
            data["name"],
            data["avg_production_time"],
            data["yield_rate"],
            data.get("stock", 0),
        )
