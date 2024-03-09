import datetime
from resource import Resource


class PurchasableResource(Resource):
    def __init__(self, resource_id: str = '', resource_name: str = '', student_id: str = '',
                 quantity_available: int = 0, unit_price: float = 0.0) -> None:
        """
        :param resource_id: str. ID of the resource
        :param resource_name: str. Name of the resource
        :param student_id: str. ID of the student who purchased the resource
        :param quantity_available: int. Quantity available for the resource
        :param unit_price: float. Unit price of the resource
        """
        super().__init__(resource_id, 'Purchasable', resource_name, student_id)
        self.quantity: int = quantity_available
        self.unit_price: float = unit_price
        self.last_time_purchased: datetime.date | None = None

    def sell(self, student_id: str, quantity: int) -> bool:
        """Sell a quantity of items
        :param student_id: str. ID of the student who purchased the resource
        :param quantity: int. Number of items to sell
        :return: bool. If there is enough items, returns True. False otherwise"""
        if self.quantity < quantity:
            return False

        self.student_id = student_id
        self.quantity -= quantity
        self.last_time_purchased = datetime.date.today()
        return True

    def is_available(self) -> bool:
        return self.quantity > 0

    def __str__(self) -> str:
        return f'{super().__str__()}, Quantity: {self.quantity}, Unit Price: {self.unit_price}'
