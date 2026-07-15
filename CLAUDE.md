# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트

반도체 회사(S-semi)의 시료 생산/주문 관리 콘솔 애플리케이션입니다. `docs/S-semi.txt`(한글)에
정의된 요구사항을 기반으로 합니다. 외부 의존성 없는 순수 Python이며 별도 빌드 단계가 없습니다.
현재 이 저장소에는 자동화된 테스트, 린터, 포매터가 구성되어 있지 않습니다.

## 실행

```bash
python main.py
```

저장소 루트에서 실행해야 합니다 — 모듈들이 루트 기준 절대 임포트를 사용하므로
(예: `from model.enums import OrderStatus`), `main.py`는 반드시 `ConsoleMVC/`에서 실행해야 합니다.

아직 테스트 스위트는 없습니다. 변경 사항을 수동으로 검증하려면 콘솔 입력 루프를 거치지 않고
Controller를 직접 호출하는 시나리오를 스크립트로 작성하세요. 예:

```bash
python -c "
from model.repository import SampleRepository, OrderRepository
from model.production_line import ProductionLine
from controller.sample_controller import SampleController
from controller.order_controller import OrderController
# ... 필요한 객체를 조립하고 controller 메서드를 직접 호출
"
```

## 아키텍처

계층별로 패키지를 분리한 엄격한 3계층 MVC 구조입니다. 의존 방향은 단방향입니다:
`view -> controller -> model`. View는 Model 클래스를 직접 다루지 않고, Controller는
`print`/`input`을 호출하지 않습니다.

- **model/** — 도메인 엔티티와 인메모리 저장소. 불변조건 외의 비즈니스 규칙은 없습니다.
  - `enums.py` — `OrderStatus`: `RESERVED`, `REJECTED`, `PRODUCING`, `CONFIRMED`, `RELEASE`.
    `REJECTED`는 정상 흐름 밖의 종료 상태로, 모니터링에서 제외됩니다.
  - `sample.py` / `order.py` — 단순 데이터 홀더. `Order`는 클래스 레벨 카운터로 증가하는
    `order_id`를 스스로 채번하며, `Sample.sample_id`는 사용자 입력값을 그대로 사용합니다.
  - `repository.py` — `SampleRepository`/`OrderRepository`. ID를 키로 하는 dict 기반
    인메모리 저장소입니다. 디스크에 영속화하지 않으므로 프로세스를 재시작하면 상태가 초기화됩니다.
  - `production_line.py` — `ProductionLine`은 단일 FIFO 생산 라인을 모델링합니다(진행 중인
    작업 1건 + `deque`로 대기하는 나머지). `ProductionJob`은 다음을 계산합니다:
    `actual_quantity = ceil(shortage_quantity / sample.yield_rate)`,
    `total_time = sample.avg_production_time * actual_quantity`.

- **controller/** — 모든 비즈니스 로직과 엔티티 간 조율을 담당합니다. 예외를 던지는 대신
  `(ok: bool, result_or_error_message)` 튜플을 반환하여, View가 실패 시 메시지를 일관되게
  출력할 수 있도록 합니다.
  - `order_controller.approve_order`가 핵심 분기점입니다: `sample.stock >= order.quantity`이면
    즉시 재고를 차감하고 주문을 `CONFIRMED`로 전환하며, 그렇지 않으면 주문을 `PRODUCING`으로
    전환하고 공유된 `ProductionLine`에 `ProductionJob`을 큐잉합니다.
  - `production_controller.complete_current_job`이 실제로 대기 중인 작업을 완료 처리합니다:
    `job.actual_quantity`(수율을 고려해 계산된 실제 생산량, 부족분보다 많을 수 있음) 전량을
    재고에 더하고, 이것이 주문 수량을 충족하면 재고에서 차감한 뒤 주문을 `CONFIRMED`로
    전환합니다. 수율로 인한 초과 생산분은 폐기되지 않고 그대로 재고에 남아 이후 주문에 사용될
    수 있습니다. 실시간 타이머는 없으며, 이 메서드가 호출될 때만(콘솔 앱에서는 "생산 라인 →
    현재 생산 완료 처리" 메뉴를 통해) 생산이 진행됩니다. 이는 콘솔 앱에 맞춰 스펙의 실시간 생산
    흐름을 의도적으로 단순화한 것입니다.
  - `monitoring_controller.stock_status`는 시료별로 `RESERVED`/`PRODUCING`/`CONFIRMED`
    (활성 상태, 비종료 상태) 주문 수량의 합을 수요로 계산하고, 각 시료를 여유
    (stock >= demand), 부족 (0 < stock < demand), 고갈 (stock <= 0)로 분류합니다.

- **view/** — 콘솔 입출력(메뉴, `input()`/`print()`)만 담당합니다. 각 View는 정확히 하나의
  Controller를 감싸며 `show_menu()` 루프를 노출합니다. `main_view.py`는 최상위 메뉴이며 매
  렌더링 전에 전체 시료 요약을 출력합니다. `base_view.py`는 공통 입력/파싱 헬퍼를 보관합니다
  (`read_input`, `read_int`, `read_float`, `print_header`).

- **main.py** — 오직 조립(composition root) 역할만 합니다. 두 Repository와
  `ProductionLine`을 생성하고, 모든 Controller와 View를 연결한 뒤 `MainView.run()`을
  호출합니다. 새 기능을 추가할 때는 기존 코드에 손대기보다 여기서 새 controller+view 쌍을
  연결하는 방식을 따르세요.

## 상태 머신

`RESERVED -> (승인) -> CONFIRMED | PRODUCING -> (생산 완료) -> CONFIRMED -> (출고) -> RELEASE`
`RESERVED -> (거절) -> REJECTED` (종료 상태, 모니터링에서 제외)

주문 ID는 `Order._next_id`를 통해 프로세스 전역으로 채번됩니다. 상태가 메모리에만 존재하므로
프로세스를 재시작하면 주문 번호 체계와 재고/큐 상태가 모두 초기화됩니다.
