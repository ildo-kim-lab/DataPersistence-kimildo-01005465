from view.base_view import print_header, read_input, read_int


class ReleaseView:
    def __init__(self, release_controller):
        self.release_controller = release_controller

    def show_menu(self):
        while True:
            print_header("출고 처리")
            print("1. 출고 대상 주문 목록(CONFIRMED)")
            print("2. 출고 처리")
            print("0. 이전 메뉴")
            choice = read_input("선택> ")
            if choice == "1":
                self._list_confirmed_orders()
            elif choice == "2":
                self._release_order()
            elif choice == "0":
                break
            else:
                print("올바른 메뉴를 선택해주세요.")

    def _list_confirmed_orders(self):
        orders = self.release_controller.list_confirmed_orders()
        if not orders:
            print("출고 대기 중인 주문이 없습니다.")
            return
        for o in orders:
            print(f"{o.order_id} | 시료:{o.sample_id} | 고객:{o.customer_name} | 수량:{o.quantity}")

    def _release_order(self):
        order_id = read_int("출고할 주문번호: ")
        ok, result = self.release_controller.release_order(order_id)
        print(f"주문 {result.order_id}가 출고 처리되었습니다." if ok else result)
