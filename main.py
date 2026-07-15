import os

from model.repository import SampleRepository, OrderRepository
from model.production_line import ProductionLine

from controller.sample_controller import SampleController
from controller.order_controller import OrderController
from controller.monitoring_controller import MonitoringController
from controller.release_controller import ReleaseController
from controller.production_controller import ProductionController

from view.sample_view import SampleView
from view.order_view import OrderView
from view.monitoring_view import MonitoringView
from view.release_view import ReleaseView
from view.production_view import ProductionView
from view.main_view import MainView


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
SAMPLES_FILE = os.path.join(DATA_DIR, "samples.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")


def main():
    sample_repository = SampleRepository(SAMPLES_FILE)
    order_repository = OrderRepository(ORDERS_FILE)
    production_line = ProductionLine()

    sample_controller = SampleController(sample_repository)
    order_controller = OrderController(order_repository, sample_repository, production_line)
    monitoring_controller = MonitoringController(order_repository, sample_repository)
    release_controller = ReleaseController(order_repository)
    production_controller = ProductionController(production_line, sample_repository, order_repository)

    sample_view = SampleView(sample_controller)
    order_view = OrderView(order_controller)
    monitoring_view = MonitoringView(monitoring_controller)
    release_view = ReleaseView(release_controller)
    production_view = ProductionView(production_controller)

    main_view = MainView(sample_controller, sample_view, order_view,
                          monitoring_view, release_view, production_view)
    main_view.run()


if __name__ == "__main__":
    main()
