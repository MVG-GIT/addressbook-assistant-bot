from datetime import datetime, date
import re

PHONE_PATTERN = re.compile(r"^\+?\d{10,15}$")
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def validate_phone(phone):
    """
    Validate phone number in international format with optional '+'.
    """
    if not PHONE_PATTERN.match(phone):
        raise ValueError("Invalid phone format: use an optional plus and from 10 to 15 digits.")
    return phone

def validate_email(email):
    """
    Validate email address with common pattern.
    """
    if not EMAIL_PATTERN.match(email):
        raise ValueError("Invalid email format: use text@text.text")
    return email

def validate_birthday(birthday):
    """
    Validate birthday in format DD.MM.YYYY and ensure it's not in the future.
    """
    if not isinstance(birthday, date):
        try:
            birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    if birthday > date.today():
        raise ValueError("Birthday cannot be in the future")

    return birthday

def validate_name(value):
    if not value or not value.strip():
        raise ValueError("Name cannot be empty.")
    return value.strip()

def validate_address(value):
    if not value or not value.strip():
        raise ValueError("Address cannot be empty.")
    return value.strip()
    