import csv
import pandas as pd
from pse_credential import PseCredential
from valid_inputs import valid_two_options
from menus import register_new_student_menu


def verify_availability(student_id: str, username: str) -> bool:
    df_accounts: pd.DataFrame = pd.read_csv('files/student.csv', delimiter=';')
    df_accounts = df_accounts.astype(str)

    if student_id in df_accounts['id'].tolist():
        return False

    if username in df_accounts['username'].tolist():
        return False

    return True


def register_new_student() -> str:
    while True:
        register_new_student_menu()

        print('Basic information')
        student_id: str = input('Enter student ID: ')
        name: str = input('Enter name: ')
        username: str = input('Enter username: ')
        password: str = input('Enter password: ')

        print('\nPSE Credentials')
        type_client: str = valid_two_options('Type client [Natural/Juridical]: ', {'natural', 'juridical'}).capitalize()
        num_id: str = input('Enter id number: ')
        type_id: str = valid_two_options('Type of identification [C.C/C.E]: ', {'c.c', 'c.e'}).upper()
        email: str = input('Email: ')
        bank: str = input('Bank name: ').capitalize()

        if not verify_availability(student_id, username):
            print(f'student ID, username or pse credentials repeated. Try again')
            continue
        break

    pse: PseCredential = PseCredential(name, type_client, num_id, type_id, email, bank)

    # Save new user on files
    with open('files/student.csv', 'a', newline='') as file:
        field_names: list[str] = ['id', 'name', 'username', 'password']
        writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
        writer.writerow({
            'id': student_id, 'name': name, 'username': username, 'password': password
        })

    # Save PSE Credentials
    with open('files/pse_credentials.csv', 'a', newline='') as file:
        field_names: list[str] = ['full_name', 'type_client', 'num_id', 'type_id', 'email', 'bank', 'student_id']
        writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')

        writer.writerow({
            'full_name': pse.full_name, 'type_client': pse.type_client, 'num_id': pse.num_id,
            'type_id': pse.type_id, 'email': pse.email, 'bank': pse.bank, 'student_id': student_id
        })

    return student_id
