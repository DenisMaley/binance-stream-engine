import json
import requests

from collections import defaultdict

from websocket import WebSocketApp
from nameko.rpc import rpc
from nameko.events import EventDispatcher


class ListenerService:

    name = 'listener'
    dispatch = EventDispatcher()

    ORDER_BOOK_ENDPOINT = 'https://api.binance.com/api/v3/depth'
    STREAM_SOCKET = 'wss://stream.binance.com:9443/ws/'

    def __init__(self):
        self.order_book = defaultdict(list)

    def on_message(self, ws, message):
        json_message = json.loads(message)
        print(json_message)

    def on_close(self, ws):
        print("Connection closed")

    @rpc
    def get_order_book(self, cc, limit):
        response = requests.get(
            self.ORDER_BOOK_ENDPOINT,
            params=dict(symbol=cc.upper(), limit=limit)
        )
        order_book = response.json()
        print(order_book)

    @rpc
    def start_stream(self, cc, stream, speed):
        socket = f'{self.STREAM_SOCKET}{cc}@{stream}@{speed}'
        ws = WebSocketApp(socket, on_message=self.on_message, on_close=self.on_close)
        ws.run_forever()

    @rpc
    def log_trigger(self):
        self.dispatch('log_records', self.order_book)
        self.order_book = defaultdict(list)
