import os
import json

from typing import Union
from nameko.events import event_handler
from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession

from logger.models import DeclarativeBase, Order


class LoggerService:

    name = 'logger'

    db = DatabaseSession(DeclarativeBase)

    def build_orders(self, order_details):
        cc = order_details['s']
        orders = []
        for type in ['a', 'b']:
            for record in order_details[type]:
                orders.append(
                    Order(
                        cc=cc,
                        type=type,
                        price=record[0],
                        quantity=record[1],
                    )
                )

        return orders

    @event_handler("listener", "insert_orders")
    def insert_orders(self, order_details):
        orders = self.build_orders(order_details)
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
