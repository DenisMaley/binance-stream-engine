import os
import json

from typing import Union
from nameko.events import event_handler
from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession
from sqlalchemy.sql import func

from logger.exceptions import NotFound
from logger.schemas import OrderSchema, VolumeSchema
from logger.models import DeclarativeBase, Order


class LoggerService:

    name = 'logger'

    db = DatabaseSession(DeclarativeBase)

    @rpc
    def get_volume(self, o_type):
        volume = self.db.query(
            func.sum(Order.quantity).label('volume'),
            func.sum(Order.price).label('total'),
        ).filter(
            Order.type == o_type
        )

        return VolumeSchema().dump(volume, many=True).data

    @rpc
    def get_order(self, order_id):
        order = self.db.query(Order).get(order_id)

        if not order:
            raise NotFound('Order with id {} not found'.format(order_id))

        return OrderSchema().dump(order).data

    def build_orders(self, order_details):
        cc = order_details['s']
        orders = []
        for o_type in ['a', 'b']:
            for record in order_details[o_type]:
                orders.append(
                    Order(
                        cc=cc,
                        type=o_type,
                        price=float(record[0]),
                        quantity=float(record[1]),
                    )
                )

        return orders

    def build_orders_from_order_book(self, order_book_details):
        cc = order_book_details['cc']
        order_book = order_book_details['order_book']
        orders = []
        key_map = {'a': 'asks', 'b': 'bids'}
        for o_type in ['a', 'b']:
            ob_type = key_map[o_type]
            for record in order_book[ob_type]:
                orders.append(
                    Order(
                        cc=cc,
                        type=o_type,
                        price=float(record[0]),
                        quantity=float(record[1]),
                    )
                )

        return orders

    @event_handler("listener", "insert_order_book")
    def insert_order_book(self, order_book_details):
        orders = self.build_orders_from_order_book(order_book_details)
        self.bulk_save_orders(orders)

    @event_handler("listener", "insert_orders")
    def insert_orders(self, order_details):
        orders = self.build_orders(order_details)
        self.bulk_save_orders(orders)

    def bulk_save_orders(self, orders):
        self.db.bulk_save_objects(orders)
        self.db.commit()

    @event_handler("listener", "log_records")
    def log_records(
            self,
            records: list,
            file: Union[str, bytes, os.PathLike] = 'log.json'
    ):
        with open(file, encoding='utf-8', mode='a') as log_file:
            json.dump(
                records, log_file, ensure_ascii=False, indent=4, sort_keys=True
            )
