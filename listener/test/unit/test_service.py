from nameko.testing.services import worker_factory

from listener.service import ListenerService


def test_log_trigger():
    service = worker_factory(ListenerService)
    service.log_trigger()
    assert len(service.order_book) == 0
