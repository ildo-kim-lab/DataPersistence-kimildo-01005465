# ConsoleMVC

S-semi 반도체 회사의 시료 생산/주문 관리 콘솔 애플리케이션입니다.

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

## 데이터 저장 (JSON 영속화)

시료와 주문 데이터는 저장소 루트의 `data/` 폴더에 JSON 파일로 저장되며, 앱을 재시작해도
데이터가 유지됩니다. (`data/`는 런타임 생성 폴더로 `.gitignore`에 의해 git 추적에서 제외됩니다.)

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
