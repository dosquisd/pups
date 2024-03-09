import os
from inventory import Inventory
from resource import Resource
from dotenv import load_dotenv
load_dotenv()


class Administrator(object):
    def __init__(self, admin_id: str = os.getenv('ADMIN_ID'),
                 admin_user: str = os.getenv('ADMIN_USER')) -> None:
        self.admin_id: str = admin_id
        self.admin_user: str = admin_user

    @staticmethod
    def add_resource(inventory: Inventory, resource: Resource) -> None:
        inventory.add_resource(resource)

    @staticmethod
    def remove_resource(inventory: Inventory, id_resource: str) -> None:
        inventory.delete_resource(id_resource)
