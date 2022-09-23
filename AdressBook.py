'''Task 9 + 10
Bot. A console bot helper that will recognize commands entered
from the keyboard and respond accordingly.
The bot accepts commands:
"hello", replies to the console "How can I help you?"
"add ...". With this command, the bot saves a new contact in memory. Instead of ... the user enters the name and phone number, necessarily with a space.
"change ..." With this command, the bot stores the new phone number of the existing contact in memory. Instead of ... the user enters the name and phone number, necessarily with a space.
"phone ...." With this command, the bot outputs the phone number for the specified contact to the console. Instead of ... the user enters the name of the contact whose number should be displayed.
"show all". With this command, the bot outputs all saved contacts with phone numbers to the console.
"good bye", "close", "exit" by any of these commands, the bot ends its work after outputting "Good bye!" to the console.
And from 10:
All classes from the task have been implemented.
Record entries in AddressBook are stored as values in a dictionary. Record.name.value is used as keys.
Record stores the Name object in a separate attribute.
Record stores a list of Phone objects in a separate attribute.
Record implements methods for adding/removing/editing Phone objects.
AddressBook implements the add_record method, which adds a Record to self.data.

"add phone ..." With this command, the bot saves a new phones to an existing contact record in memory. Instead of ... the user enters the name and phone number(s), necessarily with a space.'''

from collections import UserDict
from datetime import datetime, timedelta
import re
# import os
# import pickle
import random


# ------------------------------------------------------------------------ 1
def my_generator_names(quantity_limit: int) -> str:
    """Simplest generator Names (example: Name_0, Name_1, ...) in limited quantities
    incoming: quantity_limit (int)
    return: yield next name
    """
    counter = 0
    while counter < quantity_limit:
        yield f"Name_{counter}"
        counter += 1


# ------------------------------------------------------------------------- 2
def my_generator_phones(quantity_limit: int) -> str:
    """Simplest generator Phones (example: +38(063)0000000, +38(063)0000001,...) in limited quantities
    incoming: quantity_limit (int)
    return: yield next phone
    """
    counter = 0
    while counter < quantity_limit:
        yield "+38(063){:07}".format(counter)
        counter += 1


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record
        # self.COUNTER_OF_RECORDS += 1

    def iterator(self, N_count: int):
        # self.MAX_LIMIT = N_count
        # self.current_value = 0
        current_value = 0
        dictionary_iterator = iter(self.data)
        while current_value < len(self.data):
            volume = []
            for i in range(N_count):
                try:
                    volume.append(self.data[next(dictionary_iterator)])
                except:
                    current_value = len(self.data)
            yield volume
            current_value += N_count

    # def __iter__(self): # inherited from dictionary(UserDict) method
    #     return self


class Field:  # super for all fields ... for the future
    pass


class Name(Field):

    def __init__(self, value):
        # super().__init__(name) ... for the future
        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):  # not needed ?
        return f"{self.value}"


class Phone(Field):

    def __preformating(self, value: str) -> str:

        value = value.replace("-", "")
        if value[3] != "(":
            value = "(".join((value[: 3], value[3:]))
        if value[7] != ")":
            value = ")".join((value[: 7], value[7:]))

        return value

    def __init__(self, value):
        # super().__init__(phone) ... for the future
        self.value = self.__preformating(value)

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):  # not needed ?
        return f"{self.value}"


class Birthday(Field):

    def _check_birthday(self, birthday: str) -> datetime:

        birthday_data = birthday.split('-')
        birthday_data = datetime(year=int(birthday_data[0]), month=int(
            birthday_data[1]), day=int(birthday_data[2]))

        return birthday_data

    def __init__(self, value):
        # super().__init__(name) ... for the future
        self.value = self._check_birthday(value)

    def __repr__(self):
        return f"{self.value.date()}"

    def __str__(self):  # not needed
        return f"{self.value.date()}"


class Record():  # add remove change  field

    birthday = None

    def __init__(self, name, *phones):

        self.name = Name(name)
        self.phones = []
        if phones:
            for phone in phones:
                self.add_phone(phone)

    def days_to_birthday(self):

        if self.birthday:
            user_day = datetime(year=datetime.now().date(
            ).year, month=self.birthday.value.month, day=self.birthday.value.day)
            days_left = user_day.date() - datetime.now().date()
            if days_left.days <= 0:
                user_day = datetime(year=datetime.now().date(
                ).year + 1, month=self.birthday.value.month, day=self.birthday.value.day)
                return (user_day.date() - datetime.now().date()).days
            return days_left.days

    def years_old(self):

        if self.birthday:
            full_years_old = datetime.now().date(
            ) + timedelta(days=self.days_to_birthday()) - self.birthday.value.date()
            return full_years_old.days//365

    def add_birthday(self, birthday):

        if not self.birthday:
            self.birthday = Birthday(birthday)
            return (True,)
        else:
            return (False, f"Birthday already recorded for {self.name.value}. You can change it.")

    def change_birthday(self, birthday):

        if not self.birthday:
            return (False, f"Birthday not specified for {self.name.value}. You can add it.")
        else:
            self.birthday = Birthday(birthday)
            return (True,)

    def add_phone(self, phone_new):

        phone_new = Phone(phone_new).value
        for phone in self.phones:
            if phone_new == phone.value:
                print(f"{phone_new} already recorded for {self.name.value}")
                return False

        self.phones.append(Phone(phone_new))
        return True

    def remove_phone(self, phone_to_remove):

        phone_to_remove = Phone(phone_to_remove).value
        for phone in self.phones:
            if phone.value == phone_to_remove:
                self.phones.remove(phone)
                return True  # Is it correct instead of a break?

    def change_phone(self, phone_to_change, phone_new):

        phone_to_change = Phone(phone_to_change).value
        phone_new = Phone(phone_new).value
        verdict = False

        for phone in self.phones:

            if phone.value == phone_new:
                return (False, f"{phone_new} already recorded for {self.name.value}")

            if phone.value == phone_to_change:
                verdict = True

        if not verdict:
            return (verdict, f"{phone_to_change} not specified in the contact {self.name.value}")

        for index, phone in enumerate(self.phones):
            if phone.value == phone_to_change:
                self.phones.remove(phone)
                self.phones.insert(index, Phone(phone_new))
                return (True,)  # Is it correct instead of a break?


# ------------------------------------------------------------3
def gen_address_book(max_names: int) -> AddressBook:
    """Simplest generator simplest AddressBook
    incoming: max_names is quantity limit (int)
    return: address_book - instance of the filled class AddressBook
    """
    address_book = AddressBook()
    counter = 0
    name = my_generator_names(max_names)
    phone = my_generator_phones(max_names * 3)
    while counter < max_names:
        record = Record(next(name))
        phones_quantity = random.choice([1, 2, 3, ])

        while phones_quantity:
            record.add_phone(next(phone))
            phones_quantity -= 1

        birthday_ = random.choice([0, 1, ])
        if birthday_:
            record.add_birthday(
                str(random.randint(1922, 2005))+"-"+str(random.randint(1, 12))+"-"+str(random.randint(1, 28)))

        address_book.add_record(record)
        counter += 1

    return address_book


contact_dictionary = gen_address_book(100)
# contact_dictionary = AddressBook()


def validation_add(user_command, number_format, name):

    if len(user_command) < 2:
        return "Give me name OR name and phone please\n"

    if name in contact_dictionary:
        return "Such an entry is already in the book. Add or change a number."

    if name[0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"

    if len(user_command) >= 2:
        for phone_candidate in user_command[2:]:
            if not re.search(number_format, phone_candidate):
                return "The number(s) is invalid.\nThe number must be in the following format with 12 digits(d): +dd(ddd)ddd-dddd\n"


def validation_add_phone(user_command, number_format, name):

    if len(user_command) < 3:
        return "Give me name and new phone(s) please\n"

    if name[0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"

    for phone_candidate in user_command[2:]:
        if not re.search(number_format, phone_candidate):
            return "The number(s) is invalid.\nThe number must be in the following format with 12 digits(d): +dd(ddd)ddd-dddd\n"


def validation_change(user_command, number_format, name):

    if not contact_dictionary:
        return "No contact records available. You can add records\n"

    if len(user_command) < 4:
        return "Give me name and 2 phones please (current and new)\n"

    if name[0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"

    if not re.search(number_format, user_command[2]):
        return "The number(s) is invalid: contains invalid characters or incorrect length\nThe number must be in the following format with 12 digits(d): +dd(ddd)ddd-dddd\n"


def validation_phone(user_command, name):

    if not contact_dictionary:
        return "No contact records available\n"

    if len(user_command) < 2:
        return "Give me a name too, please\n"

    if name[0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"


def validation_show(user_command):

    if not contact_dictionary:
        return "No contact records available\n"

    if len(user_command) < 2:
        return "Give me a name, please\n"

    if user_command[1][0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not user_command[1][0].isalpha():
        return "The name can only begin with Latin characters!\n"


def validation_birthday(user_command, name):

    if not contact_dictionary:
        return "No contact records available\n"

    if len(user_command) < 3:
        return "Give me a name and birthday, please\n"

    if name[0].isdigit():
        return "A name cannot begin with a number!\n"

    elif not name[0].isalpha():
        return "The name can only begin with Latin characters!\n"

    if 1900 > int(user_command[2].split("-")[0]) > datetime.now().year - 16:
        return "The year of birth is not correct!\n"
    else:
        birthday_data = user_command[2].split('-')
        try:
            birthday_data = datetime(year=int(birthday_data[0]), month=int(
                birthday_data[1]), day=int(birthday_data[2]))
        except Exception:
            return "The calendar date is not possible!\n"


def input_error(handler):
    '''User error handler
    incoming: handler (function)
    return: result(str) or exception_function(handler(user_command))'''
    # => user input command items in the list
    def exception_function(user_command):

        number_format = r'^\+[0-9)(-]{12,16}$'
        validation = None
        if len(user_command) > 1:
            name = user_command[1]

        if handler.__name__ == "handler_showall":
            if not contact_dictionary:
                return "No contact records available\n"

        elif handler.__name__ == "handler_show":
            validation = validation_show(user_command)

        elif handler.__name__ == "handler_phone":
            validation = validation_phone(user_command, name)

        elif handler.__name__ == "handler_add_phone":
            validation = validation_add_phone(
                user_command, number_format, name)

        elif handler.__name__ == "handler_add_birthday":
            validation = validation_birthday(user_command, name)

        if handler.__name__ == "handler_add":
            validation = validation_add(user_command, number_format, name)

        elif handler.__name__ == "handler_change_birthday":
            validation = validation_birthday(user_command, name)

        elif handler.__name__ == "handler_change":
            validation = validation_change(user_command, number_format, name)

        if validation:
            return validation

        try:
            result = handler(user_command)

        except KeyError as error:
            return f"An incorrect name was entered ({error}), not found in the book"

        except ValueError as error:
            return f"I don't know such commands ({error})"

        except IndexError as error:
            return f"No values in database ({error})"

        except Exception as error:
            return f"Something went wrong ({error})"

        if result is None:
            return "No contact record available..."

        return result

    return exception_function


@ input_error
def handler_phone(user_command: list) -> str:
    '''"phone ...." With this command, the bot outputs the phone number for the specified
    contact to the console. Instead of ... the user enters the name of the contact
    whose number should be displayed.
    incoming: list of user command (name of user)
    return: phone number of user'''
    phones = ""
    name = user_command[1]
    for phone in (contact_dictionary[name]).phones:
        phones += f"{phone.value}; "

    return phones


@ input_error
def handler_change(user_command: list) -> str:  # list of str
    '''"change ..." With this command, the bot stores the new phone number
    of the existing contact in memory. Instead of ... the user enters
    the name and phone numbers (current and new), necessarily with a space.
    incoming: list of user command (name of user)
    return: string'''
    name = user_command[1]
    current_phone = user_command[2]
    new_phone = user_command[3]
    verdict = contact_dictionary[name].change_phone(current_phone, new_phone)

    # with open(helper_opener()[1], "wb") as db_file:
    #     pickle.dump(contact_dictionary, db_file)
    if verdict[0]:
        return "The record has been updated\n"
    else:
        return f"No changes have been made\n{verdict[1]}"


@ input_error
def handler_add(user_command: list) -> str:
    '''"add ...". With this command, the bot saves
    a new contact in memory (in the dictionary, for
    example). Instead of ... the user enters the name
    and phone number(s), necessarily with a space.
    incoming: list of user command (name of user)
    return: string'''
    name = user_command[1]
    new_record = Record(name)  # Record(Name(name))
    contact_dictionary.add_record(new_record)
    if len(user_command) > 2:
        phones = user_command[2:]
        verdict = False
        for new_phone in phones:
            verdict = contact_dictionary[name].add_phone(new_phone) or verdict
        if not verdict:
            return "There were no new entries to add\n"
    # with open(helper_opener()[1], "wb") as db_file:
    #     pickle.dump(contact_dictionary, db_file)
    return "A record(s) have been added\n"


@ input_error
def handler_add_phone(user_command: list) -> str:
    '''"add ...". With this command, the bot saves
    a new phones to contact in memory (in the dictionary, for
    example). Instead of ... the user enters the name
    and phone number(s), necessarily with a space.
    incoming: list of user command (name of user)
    return: string'''
    name = user_command[1]
    phones = user_command[2:]
    verdict = False
    for new_phone in phones:
        verdict = contact_dictionary[name].add_phone(new_phone) or verdict
    if not verdict:
        return "There were no new entries to add\n"
    # with open(helper_opener()[1], "wb") as db_file:
    #     pickle.dump(contact_dictionary, db_file)
    return "A record have been added\n"


def handler_exit(_=None) -> str:
    return "Good bye!"


@ input_error
def handler_showall(_=None) -> str:
    '''"show all". With this command, the bot outputs all saved
    contacts with phone numbers to the console.
    incoming: not_matter: any
    return: string of all users'''

    all_list = "Entries in your contact book:"
    for name in contact_dictionary:
        if contact_dictionary[name].birthday:
            all_list += f"\n\n{name}, birthday: {contact_dictionary[name].birthday} ({contact_dictionary[name].days_to_birthday()} days to next birthday. Will be {contact_dictionary[name].years_old()} years old)\n-> phone(s): "
        else:
            all_list += f"\n\n{name}, birthday: {contact_dictionary[name].birthday}\n-> phone(s): "
        for phone in contact_dictionary[name].phones:
            all_list += f"{phone.value}; "

    return all_list


@ input_error
def handler_show(user_command: list) -> str:
    '''"show information about a specific user". With this command, the bot outputs
    birthday, number of days until next birthday and
    phone numbers to the console.
    incoming: user_command[1] is name of user
    return: string of info about user'''

    name = user_command[1]
    if contact_dictionary[name].birthday:
        user_information = f"\n\n{name}, birthday: {contact_dictionary[name].birthday} ({contact_dictionary[name].days_to_birthday()} days to next birthday. Will be {contact_dictionary[name].years_old()} years old)\n-> phone(s): "
    else:
        user_information = f"\n\n{name}, birthday: {contact_dictionary[name].birthday}\n-> phone(s): "
    for phone in contact_dictionary[name].phones:
        user_information += f"{phone.value}; "

    return user_information


@ input_error
def handler_add_birthday(user_command: list) -> str:
    '''"add birthday...". With this command, the bot saves
    a new information about user in memory (in the dictionary, for
    example). Instead of ... the user enters the name
    and birthday (in format YYYY-MM-DD), necessarily with a space.
    incoming: list of user command (name of user and birthday)
    return: string'''
    name = user_command[1]
    verdict = contact_dictionary[name].add_birthday(user_command[2])

    # with open(helper_opener()[1], "wb") as db_file:
    #     pickle.dump(contact_dictionary, db_file)
    if verdict[0]:
        return f"Information about {name} have been updated\n"
    else:
        return f"No changes have been made\n{verdict[1]}"


@ input_error
def handler_change_birthday(user_command: list) -> str:  # list of str
    '''"change birthday ..." With this command, the bot stores the
    "new birthday" (if the previous one was wrong)
    of the existing contact in memory. Instead of ... the user enters
    the name and birthday (in format YYYY-MM-DD), necessarily with a space.
    incoming: list of user command (name of user, and birthday)
    return: string'''
    name = user_command[1]
    user_birthday = user_command[2]
    verdict = contact_dictionary[name].change_birthday(user_birthday)

    # with open(helper_opener()[1], "wb") as db_file:
    #     pickle.dump(contact_dictionary, db_file)
    if verdict[0]:
        return f"The record {name} has been updated\n"
    else:
        return f"No changes have been made\n{verdict[1]}"


def main_handler(user_command: list):
    '''All possible bot commands
    incoming: user command
    return: function according to the command'''
    all_command = {"hello": handler_hello,
                   "add": handler_add,
                   "addphone": handler_add_phone,
                   "change": handler_change,
                   "phone": handler_phone,
                   "showall": handler_showall,
                   "goodbye": handler_exit,
                   "close": handler_exit,
                   "exit": handler_exit,
                   "show": handler_show,
                   "addbirthday": handler_add_birthday,
                   "changebirthday": handler_change_birthday, }

    if all_command.get(user_command[0].lower(), "It is unclear") != "It is unclear":
        return all_command.get(user_command[0].lower())(user_command)

    return "It is unclear"


def handler_hello(_=None) -> str:
    return "How can I help you?\n"


def parser(user_input: str) -> list:
    '''Command parser. The part responsible for parsing
    strings entered by the user, extracting keywords and
    command modifiers from the string.
    incoming: string from user
    return: list of comands'''
    words = user_input.strip().split(" ")
    if len(words) >= 2 and words[0].lower() == "good" and words[1].lower() == "bye":
        words = ["goodbye"]
    elif len(words) >= 2 and words[1].lower() == "all" and words[0].lower() == "show":
        words = ["showall"]
    elif len(words) >= 2 and words[1].lower() == "phone" and words[0].lower() == "add":
        words = ["addphone"] + words[2:]
    elif len(words) >= 2 and words[0].lower() == "add" and words[1].lower() == "birthday":
        words = ["addbirthday"] + words[2:]
    elif len(words) >= 2 and words[0].lower() == "change" and words[1].lower() == "birthday":
        words = ["changebirthday"] + words[2:]
    words[0] = words[0].lower()

    return words


def main():
    """A new address book was generated at the beginning
    line 112: contact_dictionary = gen_AddressBook(16)
    """
    # global contact_dictionary
    # load contact dict if it available:
    # contact_dictionary = helper_opener()[0]

    while True:
        user_command = input()
        user_request = parser(user_command)
        bot_answer = main_handler(user_request)
        print(bot_answer)
        if bot_answer == "Good bye!":
            break

    exit()


if __name__ == "__main__":
    for i in contact_dictionary.iterator(6):
        print(i)
    exit(main())
