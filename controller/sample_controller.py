from model.sample import Sample


class SampleController:
    def __init__(self, sample_repository):
        self.sample_repository = sample_repository

    def register_sample(self, sample_id, name, avg_production_time, yield_rate):
        if self.sample_repository.exists(sample_id):
            return False, f"이미 존재하는 시료 ID입니다: {sample_id}"
        if not (0 < yield_rate < 1):
            return False, "수율은 0 초과 1 미만이어야 합니다."
        sample = Sample(sample_id, name, avg_production_time, yield_rate)
        self.sample_repository.add(sample)
        return True, sample

    def list_samples(self):
        return self.sample_repository.list_all()

    def search_samples(self, keyword):
        return self.sample_repository.search_by_name(keyword)

    def update_sample(self, sample_id, name=None, avg_production_time=None, yield_rate=None):
        sample = self.sample_repository.get(sample_id)
        if sample is None:
            return False, f"등록되지 않은 시료입니다: {sample_id}"
        if yield_rate is not None and not (0 < yield_rate < 1):
            return False, "수율은 0 초과 1 미만이어야 합니다."

        fields = {}
        if name is not None:
            fields["name"] = name
        if avg_production_time is not None:
            fields["avg_production_time"] = avg_production_time
        if yield_rate is not None:
            fields["yield_rate"] = yield_rate
        self.sample_repository.update(sample_id, **fields)
        return True, sample

    def delete_sample(self, sample_id):
        sample = self.sample_repository.get(sample_id)
        if sample is None:
            return False, f"등록되지 않은 시료입니다: {sample_id}"
        self.sample_repository.delete(sample_id)
        return True, sample
