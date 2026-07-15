from view.base_view import print_header, read_input, read_float


class SampleView:
    def __init__(self, sample_controller):
        self.sample_controller = sample_controller

    def show_menu(self):
        while True:
            print_header("시료 관리")
            print("1. 시료 등록")
            print("2. 시료 조회")
            print("3. 시료 검색")
            print("4. 시료 수정")
            print("5. 시료 삭제")
            print("0. 이전 메뉴")
            choice = read_input("선택> ")
            if choice == "1":
                self._register_sample()
            elif choice == "2":
                self._list_samples()
            elif choice == "3":
                self._search_samples()
            elif choice == "4":
                self._update_sample()
            elif choice == "5":
                self._delete_sample()
            elif choice == "0":
                break
            else:
                print("올바른 메뉴를 선택해주세요.")

    def _register_sample(self):
        sample_id = read_input("시료 ID: ")
        name = read_input("이름: ")
        avg_production_time = read_float("평균 생산시간: ")
        yield_rate = read_float("수율(0~1): ")
        ok, result = self.sample_controller.register_sample(
            sample_id, name, avg_production_time, yield_rate)
        print(f"시료가 등록되었습니다: {result.sample_id} ({result.name})" if ok else result)

    def _list_samples(self):
        samples = self.sample_controller.list_samples()
        if not samples:
            print("등록된 시료가 없습니다.")
            return
        print(f"{'ID':<10}{'이름':<15}{'평균생산시간':<15}{'수율':<10}{'재고':<10}")
        for s in samples:
            print(f"{s.sample_id:<10}{s.name:<15}{s.avg_production_time:<15}{s.yield_rate:<10}{s.stock:<10}")

    def _search_samples(self):
        keyword = read_input("검색어(이름): ")
        samples = self.sample_controller.search_samples(keyword)
        if not samples:
            print("검색 결과가 없습니다.")
            return
        for s in samples:
            print(f"{s.sample_id} | {s.name} | 재고 {s.stock}")

    def _update_sample(self):
        sample_id = read_input("수정할 시료 ID: ")
        print("변경하지 않을 항목은 비워두고 Enter를 누르세요.")
        name = read_input("새 이름: ") or None
        avg_production_time = self._read_optional_float("새 평균 생산시간: ")
        yield_rate = self._read_optional_float("새 수율(0~1): ")
        ok, result = self.sample_controller.update_sample(
            sample_id, name=name, avg_production_time=avg_production_time, yield_rate=yield_rate)
        print(f"시료가 수정되었습니다: {result.sample_id} ({result.name})" if ok else result)

    def _delete_sample(self):
        sample_id = read_input("삭제할 시료 ID: ")
        ok, result = self.sample_controller.delete_sample(sample_id)
        print(f"시료가 삭제되었습니다: {result.sample_id} ({result.name})" if ok else result)

    def _read_optional_float(self, prompt):
        while True:
            value = read_input(prompt)
            if not value:
                return None
            try:
                return float(value)
            except ValueError:
                print("숫자를 입력해주세요.")
