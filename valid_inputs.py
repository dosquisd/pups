import datetime


def valid_two_options(msg: str, options: list | tuple | set) -> str:
    while True:
        temp: str = input(msg).lower()
        if temp in options:
            return temp


def valid_datetime(msg: str) -> datetime.date:
    while True:
        temp: str = input(msg)

        try:
            day, month, year = [int(value) for value in temp.split('/')]
            date: datetime.date = datetime.date(year, month, day)
        except ValueError as e:
            print(repr(e))
            continue

        return date


def int_greater_than_zero(msg: str) -> int:
    while True:
        try:
            temp: int = int(input(msg))

            if temp >= 0:
                return temp
        except ValueError:
            pass


def float_greater_than_zero(msg: str) -> float:
    while True:
        try:
            temp: float = float(input(msg))

            if temp >= 0:
                return temp
        except ValueError:
            pass


def valid_input_menus(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError as e:
            print(repr(e))


if __name__ == "__main__":
    a = valid_datetime("DD/MM/YYYY:  ")
    print(a)
