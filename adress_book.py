import pickle
from collections import UserDict
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if len(value) < 2:
            raise ValueError("Ім'я повинно містити мінімум 2 літери.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Номер телефону має містити рівно 10 цифр.")
        super().__init__(value)


class Address(Field):
    def __init__(self, value):
        if len(value) < 5:
            raise ValueError("Адреса повинна містити мінімум 5 символів.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, new_phone):
        self.phones = [Phone(new_phone)]

    def add_address(self, address):
        self.address = Address(address)

    def edit_address(self, new_address):
        self.address = Address(new_address)

    def edit_name(self, new_name):
        self.name = Name(new_name)

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        address = self.address.value if self.address else "N/A"
        return f"Контакт: {self.name.value}, телефони: {phones}, адреса: {address}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def __getstate__(self):
        return self.data

    def __setstate__(self, state):
        self.data = state


def add_contact(name, phone, address, book):
    record = Record(name)
    record.add_phone(phone)
    record.add_address(address)
    book.add_record(record)
    return f"Контакт {name} додано."


def change_name(old_name, new_name, book):
    record = book.find(old_name)
    if not record:
        return "Контакт не знайдено."
    book.delete(old_name)
    record.edit_name(new_name)
    book.add_record(record)
    return f"Ім'я контакту змінено на {new_name}."


def change_phone(name, new_phone, book):
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    record.edit_phone(new_phone)
    return "Номер телефону змінено."


def change_address(name, new_address, book):
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    record.edit_address(new_address)
    return "Адресу змінено."


def get_phone(name, book):
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    return f"Номер телефону контакту {record.name.value}: {', '.join(phone.value for phone in record.phones)}"


def show_address(name, book):
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    return f"Адреса контакту {record.name.value}: {record.address.value}"


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    print("Ласкаво просимо до адресної книги!")
    while True:
        print("\nАдресна книга:")
        for record in book.values():
            print(record)
        print("\n1. Додати контакт")
        print("2. Знайти контакт")
        print("3. Видалити контакт")
        print("4. Показати номер телефону")
        print("5. Показати адресу")
        print("6. Змінити ім'я контакту")
        print("7. Змінити номер телефону")
        print("8. Змінити адресу")
        print("9. Вийти")
        choice = input("Виберіть дію: ")

        if choice == '1':
            while True:
                name = input("Введіть ім'я (або 0 для виходу): ")
                if name == '0':
                    break
                try:
                    Name(name)
                    break
                except ValueError as e:
                    print(e)
            if name == '0':
                continue
            while True:
                phone = input(
                    "Введіть номер телефону (10 цифр, або 0 для виходу): ")
                if phone == '0':
                    break
                try:
                    Phone(phone)
                    break
                except ValueError as e:
                    print(e)
            if phone == '0':
                continue
            while True:
                address = input("Введіть адресу (або 0 для виходу): ")
                if address == '0':
                    break
                try:
                    Address(address)
                    break
                except ValueError as e:
                    print(e)
            if address == '0':
                continue
            print(add_contact(name, phone, address, book))

        elif choice == '2':
            while True:
                name = input("Введіть ім'я (або 0 для виходу): ")
                if name == '0':
                    break
                result = get_phone(name, book)
                if result == "Контакт не знайдено.":
                    print(result)
                else:
                    print(result)
                    break

        elif choice == '3':
            while True:
                name = input("Введіть ім'я (або 0 для виходу): ")
                if name == '0':
                    break
                if book.delete(name):
                    print(f"Контакт {name} видалено.")
                    break
                else:
                    print("Контакт не знайдено.")

        elif choice == '4':
            while True:
                name = input("Введіть ім'я (або 0 для виходу): ")
                if name == '0':
                    break
                result = get_phone(name, book)
                if result == "Контакт не знайдено.":
                    print(result)
                else:
                    print(result)
                    break

        elif choice == '5':
            while True:
                name = input("Введіть ім'я (або 0 для виходу): ")
                if name == '0':
                    break
                result = show_address(name, book)
                if result == "Контакт не знайдено.":
                    print(result)
                else:
                    print(result)
                    break

        elif choice == '6':
            while True:
                old_name = input("Введіть поточне ім'я (або 0 для виходу): ")
                if old_name == '0':
                    break
                if book.find(old_name):
                    while True:
                        new_name = input(
                            "Введіть нове ім'я (або 0 для виходу): ")
                        if new_name == '0':
                            break
                        try:
                            Name(new_name)
                            break
                        except ValueError as e:
                            print(e)
                    if new_name == '0':
                        break
                    print(change_name(old_name, new_name, book))
                    break
                else:
                    print("Контакт не знайдено.")

        elif choice == '7':
            while True:
                name = input("Введіть ім'я (або 0 для виходу): ")
                if name == '0':
                    break
                if book.find(name):
                    while True:
                        new_phone = input(
                            "Введіть новий номер телефону (10 цифр, або 0 для виходу): ")
                        if new_phone == '0':
                            break
                        try:
                            Phone(new_phone)
                            break
                        except ValueError as e:
                            print(e)
                    if new_phone == '0':
                        break
                    print(change_phone(name, new_phone, book))
                    break
                else:
                    print("Контакт не знайдено.")

        elif choice == '8':
            while True:
                name = input("Введіть ім'я (або 0 для виходу): ")
                if name == '0':
                    break
                if book.find(name):
                    while True:
                        new_address = input(
                            "Введіть нову адресу (або 0 для виходу): ")
                        if new_address == '0':
                            break
                        try:
                            Address(new_address)
                            break
                        except ValueError as e:
                            print(e)
                    if new_address == '0':
                        break
                    print(change_address(name, new_address, book))
                    break
                else:
                    print("Контакт не знайдено.")

        elif choice == '9':
            save_data(book)
            print("Дані збережені, до побачення!")
            break

        else:
            print("Невірна команда. Доступні команди: 1 (Додати контакт), 2 (Знайти контакт), 3 (Видалити контакт), 4 (Показати номер телефону), 5 (Показати адресу), 6 (Змінити ім'я контакту), 7 (Змінити номер телефону), 8 (Змінити адресу), 9 (Вийти).")


if __name__ == '__main__':
    main()
