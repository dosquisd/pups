import datetime
from resource import Resource


class RentedResource(Resource):
    def __init__(self, resource_id: str = '', resource_name: str = '', student_id: str = '',
                 status: str = '', price_day: float = 0.0) -> None:
        """
        :param resource_id: str. ID of the resource
        :param resource_name: str. Name of the resource
        :param student_id: str. ID of the student who rented the resource
        :param status: str. Status of the resource. Could be 'Available' or 'Rented'
        :param price_day: float. Price per day of the resource
        """
        super().__init__(resource_id, 'Rentable', resource_name, student_id)
        self.status: str = status
        self.price_day: float = price_day
        self.start_time: datetime.date | None = None
        self.end_time: datetime.date | None = None

    def rent(self, student_id: str, num_days: int) -> bool:
        """Rent the resource
        :param student_id: str. ID of the student who rented the resource
        :param num_days: int. Number of days to rent
        :return: bool. True if the resource is available, false otherwise
        """
        if not self.is_available():
            return False

        self.status = 'Rented'
        self.student_id = student_id
        self.start_time = datetime.date.today()
        self.end_time = self.start_time + datetime.timedelta(days=num_days)
        return True

    def is_available(self) -> bool:
        return self.status == 'Available'

    def update_availability(self) -> None:
        if datetime.date.today() <= self.end_time:
            return
        self.status = 'Available'

    def __str__(self) -> str:
        output: str = f'{super().__str__()}, Status: {self.status}, Price per Hour: {self.price_day}, '
        output += f'Start Rent: {self.start_time}, End Rent: {self.end_time}'

        return output
