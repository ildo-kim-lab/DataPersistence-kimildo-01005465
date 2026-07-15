from view.base_view import print_header, read_input, read_int


class OrderView:
    def __init__(self, order_controller):
        self.order_controller = order_controller

    def show_menu(self):
        while True:
            print_header("주문 (접수/승인/거절)")
            print("1. 주문 접수(예약)")
            print("2. 접수된 주문 목록")
            print("3. 주문 승인")
            print("4. 주문 거절")
            print("0. 이전 메뉴")
            choice = read_input("선택> ")
            if choice == "1":
                self._reserve_order()
            elif choice == "2":
                self._list_reserved_orders()
            elif choice == "3":
                self._approve_order()
            elif choice == "4":
                self._reject_order()
            elif choice == "0":
                break
            else:
                print("올바른 메뉴를 선택해주세요.")

    def _reserve_order(self):
        sample_id = read_input("시료 ID: ")
        customer_name = read_input("고객명: ")
        quantity = read_int("주문 수량: ")
        ok, result = self.order_controller.reserve_order(sample_id, customer_name, quantity)
        if ok:
            print(f"주문이 접수되었습니다. 주문번호: {result.order_id} (상태: {result.status.value})")
        else:
            print(result)

    def _list_reserved_orders(self):
        orders = self.order_controller.list_reserved_orders()
        if not orders:
            print("접수된 주문이 없습니다.")
            return
        for o in orders:
            print(f"{o.order_id} | 시료:{o.sample_id} | 고객:{o.customer_name} | 수량:{o.quantity}")

    def _approve_order(self):
        order_id = read_int("승인할 주문번호: ")
        ok, result = self.order_controller.approve_order(order_id)
        if ok:
            print(f"주문 {result.order_id}가 승인되었습니다. 상태: {result.status.value}")
        else:
            print(result)

    def _reject_order(self):
        order_id = read_int("거절할 주문번호: ")
        ok, result = self.order_controller.reject_order(order_id)
        print(f"주문 {result.order_id}가 거절되었습니다." if ok else result)
