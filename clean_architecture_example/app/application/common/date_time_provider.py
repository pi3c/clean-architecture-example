from datetime import datetime
from typing import Protocol


class DateTimeProvider(Protocol):
    def get_current_time(self) -> datetime:
        raise NotImplementedError
