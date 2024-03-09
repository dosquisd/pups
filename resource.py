class Resource(object):
    def __init__(self, resource_id: str = '', resource_type: str = '',
                 resource_name: str = '', student_id: str = '') -> None:
        """
        :param resource_id: str. ID of the resource
        :param resource_type: str. If the resource could be rentable o purchasable
        :param resource_name: str. Name of the resource
        :param student_id: str. ID of the student who rented/purchased the resource
        """

        self.id: str = resource_id
        self.type: str = resource_type
        self.name: str = resource_name
        self.student_id: str = student_id

    def is_available(self) -> bool:
        """Returns True if the resource is available, False otherwise"""
        pass

    def __str__(self) -> str:
        output: str = f'ID: {self.id}, Type: {self.type}, Name: {self.name}'
        return f'{output}, Student: {self.student_id if self.student_id else "No one"}'
