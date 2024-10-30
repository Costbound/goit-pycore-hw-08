from collections import UserDict
from exeptions import PhoneValidationError, PhoneDuplicate, DateFormatError, BirthdayDuplicate
from datetime import datetime, timedelta
import calendar
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
		pass


class Phone(Field):
    def __init__(self, value: str):
        if not re.match(r'^\d{10}$', value):
            raise PhoneValidationError()
        self.value = value


class Birthday(Field):
    __birthday_regexp = re.compile(r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})$')

    def __init__(self, value):
        if not re.match(Birthday.__birthday_regexp, value):
            raise DateFormatError()
        birthday_obj = datetime.strptime(value, '%d.%m.%Y').date()
        self.value = birthday_obj

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, new_phone: str):
        for phone in self.phones:
             if phone.value == new_phone:
                  raise PhoneDuplicate()
        self.phones.append(Phone(new_phone))

    def remove_phone(self, phone_to_remove: str):
        init_phones_lenght = len(self.phones)
        self.phones = [phone for phone in self.phones if phone.value != phone_to_remove]
        return init_phones_lenght > len(self.phones)

    def edit_phone(self, phone_to_edit: str, new_phone: str):
        for phone in self.phones:
            if phone.value == phone_to_edit:
                phone.value = new_phone
                return True
        return False

    def find_phone(self, phone_search: str):
        for phone in self.phones:
             if phone.value == phone_search:
                  return phone
        return None
    
    def add_birthday(self, birthday: str):
        if self.birthday:
           raise BirthdayDuplicate
        self.birthday = Birthday(value=birthday) 

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: \n{'\n'.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def remove_record(self, name: str):
        if name in self.data:
            del self.data[name]

    def find_record(self, name: str):
        return self.data.get(name, None)
    
    def get_upcoming_birthdays(self):
        result= []
        for record in self.data.values():
            congratulation_date = self.__get_upcoming_birthday(record.birthday) if record.birthday else None
            if congratulation_date:
                congratulation_date_str = congratulation_date.strftime('%d.%m.%Y')
                birthday_str = record.birthday.value.strftime('%d.%m.%Y')
                result.append(f'{str(record.name):^20} | {birthday_str:^20} | {congratulation_date_str:^20}')
        return result
    
    def __get_upcoming_birthday(self, birthday: Birthday):
        birth_date = birthday.value
        today = datetime.today().date()
        #Check if next birthday this year or next
        next_birthday = self.__get_next_birthday(birth_date)
        #Check how much days to next birthday and if more than 7 return None
        days_to_birthday = next_birthday.toordinal() - today.toordinal()
        if days_to_birthday > 7:
            return None
        #Check weekday of next birthday and if this date is weekend change congratulation date to next Monday
        congratulation_date = self.__get_congratulation_date(next_birthday)
        return congratulation_date
    
    def __get_next_birthday(self, birthday: datetime):
        today = datetime.today().date()
        #In case birthday is on 29th February, transfer it to 1st March if now is not leap year
        birthday_this_year = ''
        if birthday.month == 2 and birthday.day == 29:
            if calendar.isleap(today.year):
                birthday_this_year = birthday.replace(year=today.year)
            else:
                birthday_this_year = birthday.replace(year=today.year, month=3, day=1)
        else:
            birthday_this_year = birthday.replace(year=today.year)
        #Get next birthday date
        next_birthday = birthday_this_year
        if birthday_this_year < today:
            if calendar.isleap(birthday_this_year.year):
                next_birthday += timedelta(days=366)
            else:
                next_birthday += timedelta(days=365)
        return next_birthday
    
    def __get_congratulation_date(self, next_birthday: datetime):
        birthday_weekday = next_birthday.weekday()
        congratulation_date = next_birthday
        if birthday_weekday == 5:
            congratulation_date += timedelta(days=2)
        elif birthday_weekday == 6:
            congratulation_date += timedelta(days=1)
        return congratulation_date
