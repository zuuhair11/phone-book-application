import json

# Encapsulates the data related to a person
class Person:
    def __init__(self, name: str) -> None:
        self.name = name
        self.__phone_numbers = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def phone_numbers(self) -> list:
        return self.__phone_numbers

    @name.setter
    def name(self, new_name) -> None:
        if new_name:
            self.__name = new_name
        else:
            raise ValueError('Not valid!')

    def add_phone_number(self, phone_number: str) -> None:
        self.__phone_numbers.append(phone_number)

    def __str__(self) -> str:
        return '{}: {}'.format(self.__name, ', '.join(self.phone_numbers))


# Handles the logic of adding, finding, and listing people in the phone book
class PhoneBook:
    def __init__(self) -> None:
        self.__persons = []

    def add_person(self, person: Person) -> None:
        self.__persons.append(person)

    def find_person(self, name: str) -> Person:
        for person in self.__persons:
            if person.name == name:
                return person
        return None

    def list_persons(self) -> list:
        return self.__persons


# Handles all interactions with the user
class UserInterface:
    def __init__(self, phone_book: PhoneBook) -> None:
        self.phone_book = phone_book

    def display_menu(self) -> None:
        print('Phone Book Application')
        print('1. Add Person')
        print('2. Add Phone Number')
        print('3. Find Person')
        print('4. List All People')
        print('5. Quit')

    def add_person(self) -> None:
        name: str = input('Enter the name of the person: ')
        person: Person = Person(name)
        self.phone_book.add_person(person)

        print(f'{name} has been added to the phone book.')

    def add_phone_number(self) -> None:
        name: str = input('Enter the name of the person: ')
        person: Person = self.phone_book.find_person(name)

        if person:
            phone_number: str = input('Enter the phone number: ')
            person.phone_numbers.append(phone_number)

            print(f'Phone number {phone_number} has been added to {name}.')
        else:
            print(f'No person found with the name {name}.')

    def find_person(self) -> None:
        name: str = input('Enter the name of the person: ')
        person: Person = self.phone_book.find_person(name)

        if person:
            print(person)
        else:
            print(f'No person found with the name {name}.')

    def list_all_persons(self) -> None:
        persons: list = self.phone_book.list_persons()

        if persons:
            for person in persons:
                print(person)
        else:
            print('The phone book is empty.')

    def run(self) -> None:
        while True:
            self.display_menu()
            choice = input('Choose an option: ')

            if choice == '1':
                self.add_person()
            elif choice == '2':
                self.add_phone_number()
            elif choice == '3':
                self.find_person()
            elif choice == '4':
                self.list_all_persons()
            elif choice == '5':
                print('Goodbye!')
                break
            else:
                print('Invalid choice. Please try again.')


# Handles the persistent storage of the phone book data.
class FileHandler:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    @property
    def filename(self) -> str:
        return self.__filename

    @filename.setter
    def filename(self, new_filename: str) -> None:
        if new_filename:
            self.__filename = new_filename
        else:
            raise ValueError('Empty. Please try again!')

    def save_phone_book(self, phone_book: PhoneBook) -> None:
        data: list = []

        for person in phone_book.list_persons():
            data.append({
                'name': person.name,
                'phone_numbers': person.phone_numbers
            })

            with open(self.filename, mode='w') as file:
                json.dump(data, file, indent=4)

    def load_phone_book(self, phone_book: PhoneBook) -> None:
        try:
            with open(self.filename, mode='r') as file:
                data: list = json.load(file)

                for entry in data:
                    person: Person = Person(entry['name'])

                    for phone_number in entry['phone_numbers']:
                        person.add_phone_number(phone_number)

                    phone_book.add_person(person)
        except FileNotFoundError:
            print('No previous phone book found.')


if __name__ == '__main__':
    phone_book = PhoneBook()
    file_handler = FileHandler('phone_book.json')

    file_handler.load_phone_book(phone_book)

    ui = UserInterface(phone_book)
    ui.run()

    file_handler.save_phone_book(phone_book)
