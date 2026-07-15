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
