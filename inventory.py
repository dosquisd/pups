from copy import copy
from resource import Resource
from rented_resource import RentedResource
from purchasable_resource import PurchasableResource


class Inventory(object):
    def __init__(self) -> None:
        self.resources: list[Resource] = []

    def add_resource(self, resource: Resource) -> None:
        """Add a resource to the list of inventory"""
        self.resources.append(copy(resource))

    def delete_resource(self, id_resource: str) -> None:
        """Delete a resource from the list of inventory given a Resource ID
        :param id_resource: str. The Resource ID to delete"""
        try:
            index: int = list(map(lambda r: r.id, self.resources)).index(id_resource)
            self.resources.pop(index)
        except ValueError as e:
            print(repr(e))

    def search_resource(self, id_resource: str) -> int:
        """Search a resource from the list of inventory given a Resource ID
        :param id_resource: str. The Resource ID to search
        :return: int. Returns index of the resource, otherwise returns -1"""
        index: int = -1
        try:
            index = list(map(lambda r: r.id, self.resources)).index(id_resource)
        except ValueError:
            pass

        return index

    def get_resources(self, index: int) -> Resource:
        """Get a resource from the list of inventory given an index
        :param index: int. The index of the resource to get. We supposed that the index is previously validated
        :return: Resource. Returns the resource in the array for the given index"""
        return copy(self.resources[index])

    def print_all(self) -> None:
        """Print all resources in the inventory"""
        for i, resource in enumerate(self.resources):
            print(f'{i+1}. {resource}')

    def get_rent_resources(self) -> list[RentedResource]:
        """Get all rent resources in the inventory
        :return: list[RentResource]. All rent resources in the inventory"""
        return list(filter(lambda r: isinstance(r, RentedResource), self.resources))

    def get_purchase_resources(self) -> list[PurchasableResource]:
        """Get all purchase resources in the inventory
        :return: list[PurchasableResource]. All purchase resources in the inventory"""
        return list(filter(lambda r: isinstance(r, PurchasableResource), self.resources))

    def get_available_resources(self, type_resource: str | None = None) -> list[Resource]:
        """Get all the available resources from the resources specified by type_resource

        :param type_resource: str. The type of resource to get ('Rentable' or 'Purchasable').
        If it's None, all available resources are returned

        :return: list[Resource]. The list of available resources"""
        temp: list[Resource] = list(filter(lambda r: type_resource is None or r.type == type_resource, self.resources))
        return list(filter(lambda r: r.is_available(), temp))

    @staticmethod
    def print_list_resources(resources: list[Resource]) -> None:
        """Print the resources given a list of resources"""
        for i, resource in enumerate(resources):
            print(f'{i+1}. {resource}')
