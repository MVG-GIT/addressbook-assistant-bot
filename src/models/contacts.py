
from collections import UserDict
from src.utils.validators import validate_phone, validate_email, validate_birthday, validate_name, validate_address

# ----------------- Field classes -----------------

class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value: str):
        value = validate_name(value)
        super().__init__(value.title())


class Phone(Field):
    def __init__(self, value):
        super().__init__(validate_phone(value))


class Email(Field):
    def __init__(self, value):
        super().__init__(validate_email(value))


class Birthday(Field):
    def __init__(self, value):
        super().__init__(validate_birthday(value))


class Address(Field):
    def __init__(self, value: str):
        value = validate_address(value)
        super().__init__(value.title())


# ----------------- Record class -----------------

class Record:
    """Record represents a single contact with name, phones, email, birthday and address."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = None
        self.addresses = []


    # Name methods
    def change_name(self, new_name):
        """Change name."""
        self.name = Name(new_name.title())
        
    def has_name(self, name):
        return name.lower() in self.name.value.lower()

    def str_name(self):
        return self.name.value
    

    # Address methods
    def add_address(self, address: str):
        """Add an address to the contact (no duplicates)."""
        address = address.title()
        if any(p.value == address for p in self.addresses):
            raise ValueError(f"Address '{address}' already exists for {self.name.value}.")
        self.addresses.append(Address(address))

    def change_address(self, old_address: str, new_address: str):
        """Change an existing address."""
        old_address = old_address.title()
        new_address = new_address.title()
        for idx, addr in enumerate(self.addresses):
            if addr.value == old_address:
                self.addresses[idx] = Address(new_address)
                return True
        return False

    def delete_address(self, address: str):
        """Delete an address."""
        address = address.title()
        for p in self.addresses:
            if p.value == address:
                self.addresses.remove(p)
                return True
        return False
    
    def has_address(self, address=""):
        return any(address.lower() in a.value.lower() for a in self.addresses)

    def str_addresses(self):
        return '; '.join([p.value for p in self.addresses])


    # Phone methods
    def add_phone(self, phone):
        """Add a phone to the contact (no duplicates)."""
        if any(p.value == phone for p in self.phones):
            raise ValueError(f"Phone '{phone}' already exists for {self.name.value}.")
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        """Change existing phone to a new one."""
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return True
        return False

    def delete_phone(self, phone):
        """Delete a phone from the contact."""
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False
    
    def has_phone(self, phone=""):
        return any(phone in p.value for p in self.phones)
    
    def str_phones(self):
        return ', '.join([p.value for p in self.phones])


    # Email methods
    def add_email(self, email):
        """Add an email to the contact (no duplicates)."""
        if any(e.value == email for e in self.emails):
            raise ValueError(f"Email '{email}' already exists for {self.name.value}.")
        self.emails.append(Email(email))

    def change_email(self, old_email, new_email):
        """Change an existing email."""
        for idx, e in enumerate(self.emails):
            if e.value == old_email:
                self.emails[idx] = Email(new_email)
                return True
        return False

    def delete_email(self, email):
        """Delete an email from the contact."""
        for e in self.emails:
            if e.value == email:
                self.emails.remove(e)
                return True
        return False
    
    def has_email(self, email=""):
        return any(email.lower() in e.value.lower() for e in self.emails)
    
    def str_emails(self):
        return ', '.join([p.value for p in self.emails])
    

    # Birthday methods
    def add_birthday(self, birthday):
        """Add birthday to contact."""
        self.birthday = Birthday(birthday)

    def change_birthday(self, birthday):
        """Overwrite existing birthday."""
        self.add_birthday(birthday)

    def delete_birthday(self):
        """Delete birthday from contact."""
        if self.birthday:
            self.birthday = None
            return True
        return False
    
    def has_birthday(self, birthday=""):
        return self.birthday != None and birthday in self.birthday.value.strftime("%d.%m.%Y")
    
    def str_birthday(self):
        return self.birthday.value.strftime("%d.%m.%Y") if self.birthday else ""


    def __str__(self):
        phones_str = self.str_phones()
        addresses_str = self.str_addresses()
        emails_str = self.str_emails()
        birthday_str = self.str_birthday()

        return f"Name: {self.name.value}, Phones: {phones_str}, Addresses: {addresses_str}, Emails: {emails_str}, Birthday: {birthday_str}"
    

# ----------------- AddressBook class -----------------

class AddressBook(UserDict):
    """AddressBook manages multiple Record objects."""

    def add_record(self, record):
        """Add a new record to the address book."""
        self.data[record.name.value.title()] = record

    def find(self, name):
        """Find record by name."""
        return self.data.get(name.title())

    def delete(self, name):
        """Delete record by name."""
        name = name.title()
        if name in self.data:
            del self.data[name]
            return True
        return False
