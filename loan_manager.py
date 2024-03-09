from student import Student
from resource import Resource
from rented_resource import RentedResource
from purchasable_resource import PurchasableResource
from inventory import Inventory


class LoanManager(object):
    def __init__(self, inventory: Inventory) -> None:
        """
        :param inventory: Inventory. The inventory of all resources
        """
        self.inventory: Inventory = inventory

    def rent_resource(self, student: Student, resource_id: str, num_days: int) -> bool:
        """
        Rent a resource for a given number of days.

        :param student: Student. The student who wants to rent the resource.
        :param resource_id: str. The ID of the resource to rent.
        :param num_days: int. The number of days for the rental period.
        :return: bool. True if the resource was successfully rented, False otherwise.
        """
        index: int = self.inventory.search_resource(resource_id)
        if index == -1:
            print(f'Resource with ID {resource_id} not found in inventory')
            return False

        resource: Resource = self.inventory.get_resources(index)
        if not isinstance(resource, RentedResource):
            print("Resource is not a rentable resource.")
            return False

        if not resource.is_available():
            print('Resource not available for rent')
            return False

        if not resource.rent(student.id, num_days):
            print('Failed to rent the resource')
            return False

        total_amount: float = resource.price_day * num_days
        student.pse_credentials.make_payment_for_rent(total_amount, resource.name, resource.id,
                                                      student.name, resource.end_time)

        return True

    def purchase_resource(self, student: Student, resource_id: str, quantity: int) -> bool:
        """
        Purchase a resource with a given quantity.

        :param student: Student. The student who wants to purchase the resource.
        :param resource_id: str. The ID of the resource to purchase.
        :param quantity: str. The quantity of the resource to purchase.
        :return: bool. True if the resource was successfully purchased, False otherwise.
        """
        index: int = self.inventory.search_resource(resource_id)
        if index == -1:
            print(f"Resource with ID {resource_id} not found in inventory")
            return False

        resource = self.inventory.get_resources(index)
        if not isinstance(resource, PurchasableResource):
            print("Resource is not a purchasable resource")
            return False

        if not resource.sell(student.id, quantity):
            print("Not enough quantity available for purchase")
            return False

        total_amount: float = resource.unit_price * quantity
        student.pse_credentials.make_payment_for_purchasable(total_amount, resource.id, resource.name,
                                                             student.name, quantity)

        return True
