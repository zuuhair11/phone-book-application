class PhoneBook:
    def __init__(self) -> None:
        self.__persons = {}

    @property
    def persons(self) -> dict:
        return self.__persons

    def add_number(self, name: str, number: str) -> None:
        if name not in self.__persons:
            self.__persons[name] = []

        self.__persons[name].append(number)

    def get_numbers(self, name: str) -> list:
        if name not in self.__persons:
            return None

        return self.__persons[name]


class FileHandler:
    def __init__(self, filename: str) -> None:
        self.__filename = filename

    def load_file(self) -> dict:
        phone_book_data: dict = {}

        with open(self.__filename, mode='r') as file:
            for line in file:
                line = line.strip()
                name, *numbers = line.split(';')

                phone_book_data[name] = numbers

        return phone_book_data
    
    def save_file(self, phone_book: PhoneBook) -> None:
        with open(self.__filename, mode='w') as file:
            for name, numbers in phone_book.persons.items():
                line = [name] + numbers
                line = ';'.join(line)

                file.write(line + '\n')


class UserInterface:
    def __init__(self) -> None:
        self.__phone_book = PhoneBook()
        self.__file_handler = FileHandler('phonebook.txt')

        for name, numbers in self.__file_handler.load_file().items():
            for number in numbers:
                self.__phone_book.add_number(name, number)

    def help(self) -> None:
        print('Commands: ')
        print('0- Exit: ')
        print('1- Add entry: ')
        print('2- Search: ')

    def exit(self) -> None:
        self.__file_handler.save_file(self.__phone_book)

    def add_entry(self) -> None:
        name: str = input('Enter your name: ')
        number: str = input('Enter your number: ')

        self.__phone_book.add_number(name, number)

    def search(self) -> None:
        name: str = input('Enter the name: ')

        numbers: list = self.__phone_book.get_numbers(name)

        if numbers == None:
            print('Number unknown!')
            return

        for number in numbers:
            print(number)

    def execute(self) -> None:
        self.help()

        while True:
            print('')
            command: str = input('>>> ')

            if command == '0':
                self.exit()
                break
            elif command == '1':
                self.add_entry()
            elif command == '2':
                self.search()


if __name__ == '__main__':
    ui: UserInterface = UserInterface()
    ui.execute()
