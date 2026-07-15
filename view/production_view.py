from view.base_view import print_header, read_input


class ProductionView:
    def __init__(self, production_controller):
        self.production_controller = production_controller

    def show_menu(self):
        while True:
            print_header("생산 라인")
            print("1. 현재 생산 현황")
            print("2. 대기 중인 생산 큐")
            print("3. 현재 생산 완료 처리")
            print("0. 이전 메뉴")
            choice = read_input("선택> ")
            if choice == "1":
                self._show_current_job()
            elif choice == "2":
                self._show_queue()
            elif choice == "3":
                self._complete_current_job()
            elif choice == "0":
                break
            else:
                print("올바른 메뉴를 선택해주세요.")

    def _show_current_job(self):
        job = self.production_controller.current_job()
        if job is None:
            print("현재 생산 중인 시료가 없습니다.")
            return
        print(f"시료:{job.sample.name} | 주문번호:{job.order.order_id} | "
              f"실생산량:{job.actual_quantity} | 진행량:{job.produced_quantity} | "
              f"총생산시간:{job.total_time}")

    def _show_queue(self):
        jobs = self.production_controller.queued_jobs()
        if not jobs:
            print("대기 중인 생산 작업이 없습니다.")
            return
        for job in jobs:
            print(f"주문번호:{job.order.order_id} | 시료:{job.sample.name} | 실생산량:{job.actual_quantity}")

    def _complete_current_job(self):
        ok, result = self.production_controller.complete_current_job()
        if ok:
            print(f"생산 완료: 주문 {result.order.order_id}, 시료 {result.sample.name}")
        else:
            print(result)
