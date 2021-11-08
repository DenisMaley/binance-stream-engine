from collections import defaultdict

from nameko.rpc import rpc
from nameko.events import EventDispatcher


class ListenerService:

    name = 'listener'
    dispatch = EventDispatcher()

    def __init__(self):
        self.order_book = defaultdict(list)

    @rpc
    def start_stream(self):
        return True

    @rpc
    def log_trigger(self):
        self.dispatch('log_records', self.order_book)
        self.order_book = defaultdict(list)
