from exeptions import PhoneValidationError, RecordNotFound, PhoneDuplicate, PhoneNotFound

default_message = 'Invalid input. Please check your command.'

def input_error(func):
    def inner(*args, **kwargs) -> str:
        try:
            return func(*args, **kwargs)
        except PhoneValidationError as e:
            return str(e)
        except PhoneDuplicate as e:
            return handle_phone_duplicate_error(e)
        except RecordNotFound as e:
            return handle_record_not_found_error(e)
        except PhoneNotFound as e:
            return handle_phone_not_found_error(e)
        except ValueError as e:
            return handle_value_error(func.__name__)
        except IndexError as e:
            return handle_index_error(func.__name__)
        except Exception as e: 
            return str(e)
    return inner


def handle_value_error(func_name: str) -> str:
    error_messages = {
        'add_contact': 'Enter both a name and phone number after the "add" command.',
        'change_contact': 'name, phone number to change and new phone number is required after the "change" command.',
        'add_birthday': 'name and birthday is required after the "add-birthday" command.' 
    }
    return error_messages.get(func_name, default_message)


def handle_index_error(func_name: str) -> str:
    error_messages = {
        'get_phone': 'Enter a name after the "phone" command.'
    }
    return error_messages.get(func_name, default_message)


def handle_phone_not_found_error(err: PhoneNotFound):
    if err.entered_name and err.entered_phone:
        return f'Phone {err.entered_phone} does not exist on contact {err.entered_name}.'
    elif err.entered_phone:
        return f'Phone {err.entered_phone} does not exist on this contact.'
    elif err.entered_name:
        return f'Entered phone does not exist on contact {err.entered_name}'
    else:
        return err.message
    

def handle_phone_duplicate_error(err: PhoneDuplicate):
    if err.entered_name and err.entered_phone:
        return f'Phone {err.entered_phone} already exists on contact {err.entered_name}'
    elif err.entered_phone:
        return f'Phone {err.entered_phone} already exists on this contact.'
    elif err.entered_name:
        return f'Entered phone already exists on contact {err.entered_name}'
    else:
        return err.message
    

def handle_record_not_found_error(err: RecordNotFound):
    return f'Contact {err.entered_name} not found.' if err.entered_name else err.message