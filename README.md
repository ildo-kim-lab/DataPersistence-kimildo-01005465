# Data Persistence

S-semi 반도체 회사의 시료 생산/주문 관리 콘솔 애플리케이션에 적용된 JSON 파일 기반
데이터 영속성(Data Persistence) 기능을 설명합니다.

## 실행 방법

```bash
python main.py
```

## 주요 기능

- 시료관리: 등록 / 목록 조회 / 이름 검색 / 수정 / 삭제
- 주문(접수/승인/거절): 주문 예약, 재고 상황에 따른 자동 승인 처리(즉시 출고 대기 또는 생산 요청), 거절
- 생산 라인: 현재 생산 현황 및 대기 큐 확인, 생산 완료 처리
- 출고 처리: 출고 대기(CONFIRMED) 주문에 대한 출고 실행
- 모니터링: 상태별 주문 건수, 시료별 재고 현황(여유/부족/고갈)

## 데이터 영속성 (JSON 파일 저장)

시료와 주문 데이터는 저장소 루트의 `data/` 폴더에 JSON 파일로 저장되며, 앱을 재시작해도
재고, 주문 목록/상태, 주문 번호 채번이 유지됩니다. (`data/`는 런타임 생성 폴더로
`.gitignore`에 의해 git 추적에서 제외됩니다.)

### 동작 방식

- `model/json_storage.py`의 `load_json`/`save_json`이 공통 유틸 역할을 합니다. 파일이
  없으면 `load_json`이 기본값을 반환하고, `save_json`은 상위 디렉터리를 자동 생성한 뒤
  `ensure_ascii=False, indent=2`로 기록합니다.
- `SampleRepository`/`OrderRepository`는 생성 시 `storage_path`를 받아 즉시 파일에서
  데이터를 로드하고, `add`/`update`/`delete` 등 변경이 있을 때마다 전체 컬렉션을 파일에
  다시 저장합니다.
- `Sample`/`Order`는 `to_dict`/`from_dict`로 직렬화/역직렬화됩니다. `Order.from_dict`는
  저장된 `order_id`를 복원하면서 필요 시 클래스 카운터(`Order._next_id`)를 이어받아,
  재시작 후에도 주문 번호가 겹치지 않도록 합니다.
- 컨트롤러가 리포지토리 메서드를 거치지 않고 엔티티를 직접 변경하는 지점
  (`order_controller.approve_order`/`reject_order`, `production_controller.
  complete_current_job`, `release_controller.release_order`)에는 각각 명시적으로
  `save()`를 호출해 상태 전이가 즉시 디스크에 반영됩니다.

### 알려진 제한

`ProductionLine`(현재 생산 중인 작업 + 대기 큐)은 메모리에만 존재하며 영속화하지 않습니다.
`PRODUCING` 상태의 주문 자체는 재시작 후에도 유지되지만, 생산 큐의 진행 순서는 재시작 시
초기화됩니다.

### `data/samples.json` — 시료 목록

| 필드 | 타입 | 설명 |
|---|---|---|
| `sample_id` | string | 사용자가 입력한 시료 ID (키) |
| `name` | string | 시료 이름 |
| `avg_production_time` | float | 평균 생산 시간 |
| `yield_rate` | float | 수율 (0 초과 1 미만) |
| `stock` | int | 현재 재고 수량 |

### `data/orders.json` — 주문 목록

| 필드 | 타입 | 설명 |
|---|---|---|
| `order_id` | int | 자동 채번된 주문 번호 (재시작 시에도 최댓값+1부터 이어짐) |
| `sample_id` | string | 주문 대상 시료 ID |
| `customer_name` | string | 고객명 |
| `quantity` | int | 주문 수량 |
| `status` | string | `OrderStatus` enum 값(`RESERVED`/`REJECTED`/`PRODUCING`/`CONFIRMED`/`RELEASE`) |

## 구조

Model / View / Controller 3계층으로 분리되어 있습니다. 자세한 아키텍처 설명은
[CLAUDE.md](CLAUDE.md)를 참고하세요.
