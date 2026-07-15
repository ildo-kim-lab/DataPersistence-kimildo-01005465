from model.enums import OrderStatus


class ProductionController:
    def __init__(self, production_line, sample_repository, order_repository):
        self.production_line = production_line
        self.sample_repository = sample_repository
        self.order_repository = order_repository

    def current_job(self):
        return self.production_line.current_job()

    def queued_jobs(self):
        return self.production_line.queued_jobs()

    def complete_current_job(self):
        job = self.production_line.complete_current_job()
        if job is None:
            return False, "진행 중인 생산 작업이 없습니다."

        sample = self.sample_repository.get(job.sample.sample_id)
        sample.stock += job.actual_quantity

        order = job.order
        if sample.stock >= order.quantity:
            sample.stock -= order.quantity
            order.status = OrderStatus.CONFIRMED
        self.sample_repository.save()
        self.order_repository.save()
        return True, job
