from student import Student
from inventory import Inventory
from loan_manager import LoanManager
from rented_resource import RentedResource
from purchasable_resource import PurchasableResource
from user_manager import UserManager
import pandas as pd
import datetime
import csv


class Pusp(object):
    def __init__(self) -> None:
        self.inventory: Inventory = Inventory()
        self.user_manager: UserManager = UserManager()
        self.loan_manager: LoanManager = LoanManager(self.inventory)

    def load_resources(self) -> None:
        """Load resources from files"""
        self.load_purchase_resources()
        self.load_rent_resources()

    def load_purchase_resources(self) -> None:
        """Load purchase resources from files"""
        df_purchase: pd.DataFrame = pd.read_csv('files/purchase.csv', delimiter=';')
        df_date_purchased: pd.DataFrame = pd.read_csv('files/purchased_resources.csv', delimiter=';')

        for i in range(len(df_purchase)):
            resource: PurchasableResource = PurchasableResource(
                resource_id=str(df_purchase['id'][i]), resource_name=str(df_purchase['name'][i]),
                quantity_available=int(df_purchase['quantity'][i]), unit_price=float(df_purchase['unit_price'][i])
            )

            date_purchased: pd.Series = df_date_purchased[
                df_date_purchased['id_resource'] == df_purchase['id'][i]
            ]['last_time_purchased']

            if len(date_purchased) > 0:
                resource.last_time_purchased = datetime.datetime.strptime(max(date_purchased), '%Y-%m-%d').date()

            self.inventory.add_resource(resource)

    def load_rent_resources(self) -> None:
        """Load rent resources from files"""
        df_rent: pd.DataFrame = pd.read_csv('files/rent.csv', delimiter=';')
        df_rented_resources: pd.DataFrame = pd.read_csv('files/rented_resource.csv', delimiter=';')

        for i in range(len(df_rent)):
            resource: RentedResource = RentedResource(
                resource_id=str(df_rent['id'][i]), resource_name=str(df_rent['name'][i]),
                status=str(df_rent['status'][i]), price_day=float(df_rent['price_day'][i])
            )

            end_date_rented: pd.Series = df_rented_resources[
                df_rented_resources['id_resource'] == df_rent['id'][i]
            ]['end_date']

            if len(end_date_rented) > 0:
                resource.last_time_purchased = datetime.datetime.strptime(max(end_date_rented), '%Y-%m-%d').date()
                resource.update_availability()

            self.inventory.add_resource(resource)

    def rent_resource(self, student_id: str, resource_id: str, num_days: int) -> None:
        student: Student = self.get_student(student_id)
        if student is None:
            return

        self.loan_manager.rent_resource(student, resource_id, num_days)

    def purchase_resource(self, student_id: str, resource_id: str, quantity: int) -> None:
        student: Student = self.get_student(student_id)
        if student is None:
            return

        self.loan_manager.purchase_resource(student, resource_id, quantity)

    def get_student(self, student_id: str) -> Student | None:
        index: int = self.user_manager.search_students(student_id)

        if index == -1:
            return None

        return self.user_manager.get_student(index)

    def reports(self) -> None:
        # For rented resources
        avg_num_days: int = 0
        n_rented: int = 0
        n_rent_resource: int = 0

        print('Rent resources:\n')
        for i, r in enumerate(self.inventory.get_rent_resources()):
            print(f'{i+1}. {r}')

            n_rent_resource += 1
            if r.is_available():
                continue
            avg_num_days += (r.end_time - r.start_time).days
            n_rented += 1

        avg_num_days /= n_rented

        print(f'Number of total rent service; {n_rent_resource}')
        print(f'Number of rented resources: {n_rented}')
        print(f"Avg number of days rented: {avg_num_days}")

        # For purchased resources
        avg_num_quantities: int = 0
        n_purchase_resource: int = 0

        print('\n\nPurchase resources:\n')
        for i, r in enumerate(self.inventory.get_purchase_resources()):
            print(f'{i+1}. {r}')

            n_purchase_resource += 1
            avg_num_quantities += r.quantity

        avg_num_quantities /= n_purchase_resource

        print(f'Number of purchase resources: {n_purchase_resource}')
        print(f'Average number of quantities: {avg_num_quantities}')

    def save_purchased_resources(self) -> None:
        purchased_resources: list[PurchasableResource] = self.inventory.get_purchase_resources()

        with open('files/purchase.csv', 'w', newline='') as file:
            fieldnames: list[str] = ['id', 'name', 'quantity', 'unit_price']

            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for resource in purchased_resources:
                writer.writerow({
                    'id': resource.id,
                    'name': resource.name,
                    'quantity': resource.quantity,
                    'unit_price': resource.unit_price
                })

        with open('files/purchased_resources.csv', 'r', newline='') as file:
            fieldnames: list[str] = ['id_resource', 'id_student', 'last_time_purchased']

            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for resource in purchased_resources:
                writer.writerow({
                    'id_resource': resource.id,
                    'id_student': resource.student_id,
                    'last_time_purchased': resource.last_time_purchased
                })

    def save_rented_resources(self) -> None:
        rented_resources: list[RentedResource] = self.inventory.get_rent_resources()

        with open('files/rent.csv', 'w', newline='') as file:
            fieldnames: list[str] = ['id_resource', 'name', 'status', 'price_day']

            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for resource in rented_resources:
                writer.writerow({
                    'id_resource': resource.id,
                    'name': resource.name,
                    'status': resource.status,
                    'price_day': resource.price_day
                })

        with open('files/rented_resource.csv', 'w', newline='') as file:
            fieldnames: list[str] = ['id_resource', 'id_student', 'start_date', 'end_date']

            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for resource in rented_resources:
                if not resource.is_available():
                    writer.writerow({
                        'id_resource': resource.id,
                        'id_student': resource.student_id,
                        'start_date': resource.start_time,
                        'end_date': resource.end_time
                    })
