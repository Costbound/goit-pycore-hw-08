import atexit
import signal
import sys
from handlers import add_contact, change_contact, get_phones, get_all_contacts, add_birthday, show_birthday, birthdays
from address_book import AddressBook
import pickle

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def load_book(filename='addressbook.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return AddressBook()

def save_book(book: AddressBook, filename='addressbook.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(book, f)
    print("Address book saved.")

def main():
    book = load_book()

    atexit.register(save_book, book)

    def signal_handler(sig, frame):
        save_book(book)
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    print("Welcome to the assistant bot!")
    try:
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == 'phone':
                print(get_phones(args, book))
            elif command == 'all':
                print(get_all_contacts(book))
            elif command == 'add-birthday':
                print(add_birthday(args, book))
            elif command == 'show-birthday':
                print(show_birthday(args, book))
            elif command == 'birthdays':
                print(birthdays(book))
            else:
                print("Invalid command.")
    finally:
        save_book(book)

if __name__ == "__main__":
    main()
