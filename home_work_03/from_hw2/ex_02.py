from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, List, Tuple


@dataclass
class Movie:
    title: str
    dates: List[Tuple[datetime, datetime]]

    def schedule(self) -> Generator[datetime, None, None]:
        day = timedelta(hours=24)
        # расставим отрезки по возрастанию даты начала показа,
        # также учтём, что дата начала и окончания могут быть поменяны местами
        # результат вернем в свой список кортежей, не уверен, что изменить
        # оргинальный это хорошая идея
        sorted_dates = sorted(self.dates, key=lambda x: min(x[0], x[1]))
        #последний день когда был показ фильма
        last_day = datetime(1, 1, 1)

        for p in sorted_dates:
            if p[0] > p[1]:
                curr_day = p[1]
                end_day = p[0]
            else:
                curr_day = p[0]
                end_day = p[1]
            #отсечём дни в которые уже были показы
            curr_day = max(curr_day, last_day)
            while curr_day <= end_day:
                yield curr_day
                last_day = curr_day
                curr_day += day

        return []

