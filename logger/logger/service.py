import os
import json

from typing import Union
from nameko.events import event_handler


class LoggerService:

    name = 'logger'

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
