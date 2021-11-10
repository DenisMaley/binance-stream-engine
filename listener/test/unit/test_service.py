from nameko.testing.services import worker_factory

from listener.service import ListenerService


def test_on_close(capsys):
    service = worker_factory(ListenerService)
    service.on_close(None, 500, 'test')
    captured = capsys.readouterr()
    assert captured.out == "Connection closed: 500 - test\n"
