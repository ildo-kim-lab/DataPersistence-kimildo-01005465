from view.base_view import print_header, read_input


class MainView:
    def __init__(self, sample_controller, sample_view, order_view,
                 monitoring_view, release_view, production_view):
        self.sample_controller = sample_controller
        self.sample_view = sample_view
        self.order_view = order_view
        self.monitoring_view = monitoring_view
        self.release_view = release_view
        self.production_view = production_view

    def run(self):
        while True:
            self._show_summary()
            print_header("메인 메뉴")
            print("1. 시료관리")
            print("2. 주문(접수/승인/거절)")
            print("3. 모니터링")
            print("4. 출고 처리")
            print("5. 생산 라인")
            print("0. 종료")
            choice = read_input("선택> ")
            if choice == "1":
                self.sample_view.show_menu()
            elif choice == "2":
                self.order_view.show_menu()
            elif choice == "3":
                self.monitoring_view.show_menu()
            elif choice == "4":
                self.release_view.show_menu()
            elif choice == "5":
                self.production_view.show_menu()
            elif choice == "0":
                print("시스템을 종료합니다.")
                break
            else:
                print("올바른 메뉴를 선택해주세요.")

    def _show_summary(self):
        samples = self.sample_controller.list_samples()
        print_header("전체 시료 요약")
        if not samples:
            print("등록된 시료가 없습니다.")
            return
        for s in samples:
            print(f"{s.name} | 재고:{s.stock}")
