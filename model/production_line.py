import math
from collections import deque


class ProductionJob:
    def __init__(self, order, sample, shortage_quantity):
        self.order = order
        self.sample = sample
        self.shortage_quantity = shortage_quantity
        self.actual_quantity = math.ceil(shortage_quantity / sample.yield_rate)
        self.total_time = sample.avg_production_time * self.actual_quantity
        self.produced_quantity = 0


class ProductionLine:
    """하나의 생산 라인은 시료를 하나씩(FIFO) 생산한다."""

    def __init__(self):
        self._queue = deque()
        self._current_job = None

    def enqueue(self, job: ProductionJob):
        self._queue.append(job)
        if self._current_job is None:
            self._start_next()

    def _start_next(self):
        self._current_job = self._queue.popleft() if self._queue else None

    def current_job(self):
        return self._current_job

    def queued_jobs(self):
        return list(self._queue)

    def complete_current_job(self):
        job = self._current_job
        if job is None:
            return None
        job.produced_quantity = job.actual_quantity
        self._start_next()
        return job
