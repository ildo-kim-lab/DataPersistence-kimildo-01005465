from view.base_view import print_header, read_input


class MonitoringView:
    def __init__(self, monitoring_controller):
        self.monitoring_controller = monitoring_controller

    def show_menu(self):
        while True:
            print_header("모니터링")
            print("1. 상태별 주문량 확인")
            print("2. 시료별 재고량 확인")
            print("0. 이전 메뉴")
            choice = read_input("선택> ")
            if choice == "1":
                self._show_order_counts()
            elif choice == "2":
                self._show_stock_status()
            elif choice == "0":
                break
            else:
                print("올바른 메뉴를 선택해주세요.")

    def _show_order_counts(self):
        counts = self.monitoring_controller.order_counts()
        for status, count in counts.items():
            print(f"{status.value}: {count}건")

    def _show_stock_status(self):
        rows = self.monitoring_controller.stock_status()
        if not rows:
            print("등록된 시료가 없습니다.")
            return
        for sample, demand, state in rows:
            print(f"{sample.name} | 재고:{sample.stock} | 주문대비 수요:{demand} | 상태:{state}")
