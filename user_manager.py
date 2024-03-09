import pandas as pd
from copy import copy
from student import Student
from pse_credential import PseCredential


class UserManager(object):
    def __init__(self) -> None:
        self.students: list[Student] = []
        self.load_students()

    @staticmethod
    def load_pse_credentials() -> dict[str, PseCredential]:
        pse_dict: dict[str, PseCredential] = {}
        df_credentials = pd.read_csv('files/pse_credentials.csv', delimiter=';')

        for i in range(len(df_credentials)):
            student_id: str = df_credentials['student_id'][i]
            pse_dict[student_id] = PseCredential(
                full_name=df_credentials['full_name'][i], type_client=df_credentials['type_client'][i],
                num_id=df_credentials['num_id'][i], email=df_credentials['email'][i],
                bank=df_credentials['bank'][i], type_id=df_credentials['type_id'][i]
            )

        return pse_dict

    def load_students(self) -> None:
        df_students: pd.DataFrame = pd.read_csv('files/student.csv', delimiter=';')
        pse_credentials: dict[str, PseCredential] = self.load_pse_credentials()

        for i in range(len(df_students)):
            self.students.append(Student(
                student_id=df_students['id'][i], name=df_students['name'][i],
                pse_credentials=copy(pse_credentials[df_students['id'][i]])
            ))

    def search_students(self, student_id) -> int:
        """Search a student from the list of students given a Student ID
        :param student_id: str. The student ID to search for
        :return: int. Returns index of the resource, otherwise returns -1"""
        index: int = -1

        try:
            index = list(map(lambda s: s.id, self.students)).index(student_id)
        except ValueError:
            pass

        return index

    def get_student(self, index: int) -> Student:
        """Get the student from the list of students given an index
        :param index: int. The index of the student to get. We supposed that the index is previously validated
        :return: Student. Returns the Student object in the students list"""
        return copy(self.students[index])


if __name__ == '__main__':
    user: UserManager = UserManager()

    for k, student in enumerate(user.students):
        print(f'{k+1}. {student}')
