from dataclasses import dataclass
from datetime import date


@dataclass
class PseCredential:
    """PSE credentials
    Attributes:
        full_name: full name of the person
        type_client: type of client ('Natural' or 'Juridical')
        num_id: identification number
        type_id: type of identification ('C.C' or 'C.E')
        email: email address of the person
        bank: bank name of the person"""
    full_name: str
    type_client: str
    num_id: str
    type_id: str
    email: str
    bank: str

    @staticmethod
    def make_payment_for_rent(amount: float, rent_name: str, rent_id: str, student_name: str, end_time: date) -> None:
        """Do the simulation of rent payment via PSE"""
        print(f'Payment approved: ${amount:,}')
        print(f'Resource {rent_name}. (ID: {rent_id}) has been rented by {student_name} until {end_time}')

    @staticmethod
    def make_payment_for_purchasable(amount: float, purchase_id: str, purchase_name: str,
                                     student_name: str, quantity: int) -> None:
        """Do the simulation of purchasable payment via PSE"""
        print(f'Payment approved: ${amount:,}')
        print(f'{student_name} has purchased {quantity} units of {purchase_name} (ID: {purchase_id})')

    def __str__(self) -> str:
        output: str = f'Full name: {self.full_name}, Type Client: {self.type_client}, ID Number: {self.num_id}, '
        output += f'ID Type: {self.type_id}, Email: {self.email}, Bank: {self.bank}'

        return output
