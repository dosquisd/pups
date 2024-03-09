from pusp import Pusp
from time import sleep
from administrator import Administrator
from register_student import register_new_student
from login import login_validating
from resource import Resource
from rented_resource import RentedResource
from purchasable_resource import PurchasableResource
from valid_inputs import *
from menus import *


def login() -> tuple[str, str]:
    login_menu()
    username: str = input('Username: ')
    password: str = input('Password: ')

    return login_validating(username, password)


def start() -> tuple[str, str]:
    while True:
        start_menu()
        op: int = valid_input_menus('Option: ')

        match op:
            case 1:
                rol, id_student = login()
                if rol != '':
                    break

            case 2:
                rol, id_student = 'student', register_new_student()

            case 3:
                rol, id_student = '', ''
                break

            case _:
                print('Invalid input')

        print('\n\n')

    return rol, id_student


def student_full_menu(pusp: Pusp, student_id: str) -> None:
    while True:
        student_menu()
        op: int = valid_input_menus('Option: ')

        match op:
            case 1:
                resource_id: str = input('Resource ID to rent: ')
                num_days: int = int_greater_than_zero('Number of days to rent: ')
                pusp.rent_resource(student_id, resource_id, num_days)
                print('\n')

            case 2:
                resource_id: str = input('Resource ID to purchase: ')
                quantity: int = int_greater_than_zero('Quantity to purchase: ')
                pusp.purchase_resource(student_id, resource_id, quantity)
                print('\n')

            case 3:
                print('Returning to main menu...')
                sleep(1)
                break

            case _:
                print('Invalid input')

        print('\n\n')


def admin(pusp: Pusp) -> None:
    administrator: Administrator = Administrator()

    while True:
        admin_menu()
        op: int = valid_input_menus('Option: ')

        match op:
            case 1:
                resource_type: str = valid_two_options('Resource type [Rentable/Purchasable]',
                                                       {'Rentable', 'Purchasable'})
                resource_id: str = input('Resource ID: ')
                resource_name: str = input('Resource name: ')

                if resource_type == 'Rentable':
                    price_day: int = int_greater_than_zero('Price per day: ')
                    resource: Resource = RentedResource(resource_id, resource_name, price_day=price_day)
                else:
                    quantity: int = int_greater_than_zero('Quantity available: ')
                    unit_price: float = float_greater_than_zero('Unit price: ')
                    resource: Resource = PurchasableResource(resource_id, resource_name,
                                                             quantity_available=quantity, unit_price=unit_price)

                administrator.add_resource(pusp.inventory, resource)

            case 2:
                resource_id: str = input('Resource ID to delete: ')
                administrator.remove_resource(pusp.inventory, resource_id)

            case 3:
                pusp.reports()

            case 4:
                break

            case _:
                print('Invalid input')

        print('\n\n')


def main() -> None:
    pusp: Pusp = Pusp()
    rol, id_student = start()

    match rol:
        case '':
            return

        case 'student':
            student_full_menu(pusp, id_student)

        case 'admin':
            admin(pusp)

    pusp.save_purchased_resources()
    pusp.save_rented_resources()
