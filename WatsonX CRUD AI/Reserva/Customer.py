# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
"""Here's an example of how you could add docstrings to all methods:"""

class Customer:
    """Class representing a customer"""

    def __init__(self, firstName, lastName, address, street, zip, city, dob):
        """Initialize a new customer

        Args:
            firstName (str): First name of the customer
            lastName (str): Last name of the customer
            address (str): Address of the customer
            street (str): Street of the customer
            zip (int): ZIP code of the customer
            city (str): City of the customer
        """
        self.__firstName = firstName
        self.__lastName = lastName
        self.__address = address
        self.__street = street
        self.__zip = zip
        self.__city = city
        self.__dob = dob

    # getters and setters for firstName attribute
    @property
    def firstName(self):
        return self.__firstName

    @firstName.setter
    def firstName(self, value):
        if not isinstance(value, str):
            raise ValueError("First name must be a string")
        self.__firstName = value

    # getters and setters for lastName attribute
    @property
    def lastName(self):
        return self.__lastName

    @lastName.setter
    def lastName(self, value):
        if not isinstance(value, str):
            raise ValueError("Last name must be a string")
        self.__lastName = value

    # getters and setters for address attribute
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        if not isinstance(value, str):
            raise ValueError("Address must be a string")
        self.__address = value

    # getters and setters for street attribute
    @property
    def street(self):
        return self.__street

    @street.setter
    def street(self, value):
        if not isinstance(value, str):
            raise ValueError("Street must be a string")
        self.__street = value

    # getters and setters for zip attribute
    @property
    def zip(self):
        return self.__zip

    @zip.setter
    def zip(self, value):
        if not isinstance(value, int):
            raise ValueError("ZIP code must be an integer")
        self.__zip = value

    # getters and setters for city attribute
    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, value):
        if not isinstance(value, str):
            raise ValueError("City must be a string")
        self.__city = value

    # getters and setters for dob attribute
    @property
    def dob(self, dob):
        return self.__dob

    @dob.setter
    def dob(self, value):
        if not isinstance(value, int):
            raise ValueError("Day Of Birth must be a string")
        self.__dob = value


    # rest of the class definition
