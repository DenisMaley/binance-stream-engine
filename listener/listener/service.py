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
        order_details = json.loads(message)
        self.dispatch('insert_orders', order_details)
        print(order_details)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"Connection closed: {close_status_code} - {close_msg}")

    @rpc
    def get_order_book(self, cc, limit):
        response = requests.get(
            self.ORDER_BOOK_ENDPOINT,
            params=dict(symbol=cc.upper(), limit=limit)
        )
        order_book = response.json()
        self.dispatch(
            'insert_order_book',
            {'cc': cc, 'order_book': order_book}
        )
        print(
            f"Order book received: {len(order_book['bids'])} bids "
            f"and {len(order_book['asks'])} asks."
        )

    @rpc
    def start_stream(self, cc, stream, speed):
        socket = f'{self.STREAM_SOCKET}{cc}@{stream}@{speed}'
        ws = WebSocketApp(socket, on_message=self.on_message, on_close=self.on_close)
        ws.run_forever()

    @rpc
    def log_trigger(self):
        self.order_book = defaultdict(list)
