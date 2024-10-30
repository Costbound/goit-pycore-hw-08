from err_handlers import input_error
from address_book import Record, AddressBook
from exeptions import RecordNotFound, PhoneNotFound


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record: Record | None = book.find_record(name)
    if not record:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return f'Contact "{name}" added.'
    record.add_phone(phone)
    return f'Phone {phone} added for contact {record.name}'


@input_error
def change_contact(args, book: AddressBook):
    name, phone_to_change, new_phone = args
    record = book.find_record(name)

    if not(record):
        raise RecordNotFound(entered_name=name)
    
    is_edited = record.edit_phone(phone_to_change, new_phone)
    if not is_edited:
        raise PhoneNotFound(entered_name=name, entered_phone=phone_to_change)

    return f'Contact "{name}" modified.'


@input_error
def get_phones(args, book:AddressBook):
    name = args[0]
    record: Record | None = book.find_record(name)
    if not record:
        raise RecordNotFound(entered_name=name)
    return record
    

def get_all_contacts(book: AddressBook):
    contact_strings = []
    for key in book:
        contact_strings.append(key)
    if len(contact_strings) < 1:
        return 'Adress book is empty.'
    return '\n'.join(contact_strings)
     

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record: Record | None = book.find_record(name)
    if not record:
        raise RecordNotFound(entered_name=name)
    record.add_birthday(birthday=birthday)
    return f'Birthday added for {record.name}'

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record: Record | None = book.find_record(name)
    if not record:
        raise RecordNotFound(entered_name=name)
    if not record.birthday:
        return f'Birthday is not selected for {record.name}'
    return f'Birthday for {record.name} is: {record.birthday}'

def birthdays(book: AddressBook):
    birthdays = '\n'.join(book.get_upcoming_birthdays())
    return f'Upcoming birthdays:\n{'Contact':^20} | {'Birthday':^20} | {'Congratulation date':^20}\n{'-' * 20} | {'-' * 20} | {'-' * 20}\n{birthdays}'