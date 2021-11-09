import json

from collections import defaultdict

from websocket import WebSocketApp
from nameko.rpc import rpc
from nameko.events import EventDispatcher


class ListenerService:

    name = 'listener'
    dispatch = EventDispatcher()

    def __init__(self):
        self.order_book = defaultdict(list)

    def on_message(self, ws, message):
        json_message = json.loads(message)
        print(json_message)

    def on_close(self, ws):
        print("Connection closed")

    @rpc
    def start_stream(self, socket):
        ws = WebSocketApp(socket, on_message=self.on_message, on_close=self.on_close)
        ws.run_forever()

    @rpc
    def log_trigger(self):
        self.dispatch('log_records', self.order_book)
        self.order_book = defaultdict(list)
