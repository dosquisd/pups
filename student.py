from copy import copy
from pse_credential import PseCredential


class Student(object):
    def __init__(self, student_id: str = '', name: str = '',
                 pse_credentials: PseCredential = None) -> None:
        """
        :param student_id: str. Student ID
        :param name: str. Student name
        :param pse_credentials: PseCredential. PSE credentials of the Student to make pays"""
        if pse_credentials is None:
            pse_credentials = {}

        self.id: str = student_id
        self.name: str = name
        self.pse_credentials: PseCredential = copy(pse_credentials)

    def __str__(self) -> str:
        return f'Student ID: {self.id}, Name: {self.name}\nPSE Credentials: {self.pse_credentials}'
