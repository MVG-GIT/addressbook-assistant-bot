
import sys
from datetime import datetime, timedelta

from src.decorators import input_error
from src.models.contacts import Record
from src.models.notes import Note
from src.utils.validators import validate_phone, validate_email, validate_birthday, validate_address

from src.utils.styling import err, wrn, grt, suc, inp, sch, table_display_contacts, table_display_notes, table_display_help

# Modified parse_input to support string with (white)spaces.
def parse_input(user_input):
    args = []
    current = ""
    in_quotes = False
    quote_char = ""

    for c in user_input.strip():
        if c in ('"', "'"):
            if in_quotes:
                if c == quote_char:
                    in_quotes = False
                    quote_char = ""
                else:
                    current += c
            else:
                in_quotes = True
                quote_char = c
        elif c == " " and not in_quotes:
            if current:
                args.append(current)
                current = ""
        else:
            current += c

    if current:
        args.append(current)

    if not args:
        return "", []
    return args[0].lower(), args[1:]


def is_value_unique(book, field, value, current_name=None):
    for name, record in book.data.items():
        if name == current_name:
            continue
        items = getattr(record, field)
        if any(item.value == value for item in items):
            return name  # found in another record
    return None


def confirm_override_if_duplicate(book, field, value, current_name=None):
    found_in = is_value_unique(book, field, value, current_name)
    if found_in:
        print(wrn(f"This {field[:-1]} is already used in contact '{found_in}'. Proceed anyway? (y/n): "), end="")
        answer = input().strip().lower()
        if answer != 'y':
            print(wrn("Operation cancelled."))
            return False
    return True


@input_error
def show_help(args=None, book=None, notes=None):
    """
    Show available commands with aliases, descriptions, usage, grouped by category.
    """
    return table_display_help(COMMANDS, ALIASES)


@input_error
def hello(args=None, book=None, notes=None):
    return grt("How can I help you, my Lord?")


@input_error
def add_contact(args=None, book=None, notes=None):
    """
    Interactively add a new contact, one field at a time.
    Prevents duplicate names. Uses other handlers for fields like phones/emails.
    """
    if len(args) > 0:
        return(wrn("To add a value, enter the add command and press Enter."))
        
    while True:
        name = input(inp('Enter contact name (Write "Cancel" to stop): ')).strip()
        if name.lower() == "cancel":
            return (wrn(f"Contact creation cancelled."))
        if not name:
            print(wrn("Name cannot be empty."))
            continue
        if name.title() in book.data:
            print(wrn(f"Contact '{name}' already exists."))
            continue
        else:
            break

    record = Record(name)
    book.add_record(record)

    print(suc("Now add fields to the contact. Leave empty to stop each section."))

    # Phones
    while True:
        phone = input(inp("Enter phone number: ")).strip()
        if not phone:
            break
        print(add_phone([name, phone], book))

    # Emails
    while True:
        email = input(inp("Enter email: ")).strip()
        if not email:
            break
        print(add_email([name, email], book))

    # Addresses
    while True:
        address = input(inp("Enter address: ")).strip()
        if not address:
            break
        print(add_address([name, address], book))

    # Birthday
    birthday = input(inp("Enter birthday (DD-MM-YYYY, optional): ")).strip()
    if birthday:
        print(add_birthday([name, birthday], book))

    print(suc(f"Contact '{name}' added successfully."))


@input_error
def add_phone(args=None, book=None, notes=None):
    name, phone = args
    phone = validate_phone(phone)

    if not confirm_override_if_duplicate(book, "phones", phone, name):
        return ""

    record = book.find(name)
    if record:
        record.add_phone(phone)
        return suc(f"Added phone to {name}.")
    return err("Contact not found.")


@input_error
def change_name(args=None, book=None, notes=None):
    name, new_name = args
    record = book.find(name)
    if record:
        record.change_name(new_name)
        book.delete(name)
        book.add_record(record)
        return suc(f"{name}'s name updated.")
    return err("Contact not found.")


@input_error
def change_phone(args=None, book=None, notes=None):
    name, old_phone, new_phone = args
    new_phone = validate_phone(new_phone)

    if not confirm_override_if_duplicate(book, "phones", new_phone, name):
        return ""

    record = book.find(name)
    if record:
        if record.change_phone(old_phone, new_phone):
            return suc(f"{name}'s phone updated.")
        return wrn(f"Couldn't find {name}'s phone '{old_phone}'.")
    return err("Contact not found.")

@input_error
def delete_phone(args=None, book=None, notes=None):
    name, phone = args
    record = book.find(name)
    if record and record.delete_phone(phone):
        return suc(f"{name}'s phone '{phone}' deleted.")
    return err("Contact or phone not found.")


@input_error
def get_phones(args=None, book=None, notes=None):
    name = args[0]
    record = book.find(name)
    if record:
        if record.has_phone():
            phones = record.str_phones()
            return sch(f"{name}'s phones: {phones}")
        return wrn(f"{name} has no phones.")
    return err("Contact not found.")


@input_error
def delete_contact(args=None, book=None, notes=None):
    name = args[0]
    if book.delete(name):
        return suc(f"Contact {name} deleted.")
    return err("Contact not found.")


@input_error
def add_email(args=None, book=None, notes=None):
    name, email = args
    email = validate_email(email)

    if not confirm_override_if_duplicate(book, "emails", email, name):
        return ""

    record = book.find(name)
    if record:
        record.add_email(email)
        return suc(f"Email added to {name}.")
    return err("Contact not found.")


@input_error
def change_email(args=None, book=None, notes=None):
    name, old_email, new_email = args
    new_email = validate_email(new_email)

    if not confirm_override_if_duplicate(book, "emails", new_email, name):
        return ""

    record = book.find(name)
    if record:
        if record.change_email(old_email, new_email):
            return suc(f"{name}'s email updated.")
        return wrn(f"Couldn't find {name}'s email '{old_email}'.")
    return err("Contact not found.")


@input_error
def delete_email(args=None, book=None, notes=None):
    name, email = args
    record = book.find(name)
    if record and record.delete_email(email):
        return suc(f"{name}'s email '{email}' deleted.")
    return err("Contact or email not found.")


@input_error
def add_address(args=None, book=None, notes=None):
    name, address_parts = args
    address = validate_address(address_parts).title()
    record = book.find(name)
    if record:
        record.add_address(address)
        return suc(f"Address added to {name}.")
    return err("Contact not found.")


@input_error
def change_address(args=None, book=None, notes=None):
    name, old_address, new_address = args
    record = book.find(name)
    if record:
        if record.change_address(old_address, new_address):
            return suc(f"Address updated for {name}.")
        return wrn(f"Address '{old_address}' not found for {name}.")
    return err("Contact not found.")


@input_error
def delete_address(args=None, book=None, notes=None):
    name, address_parts = args
    address = validate_address(address_parts).title()
    record = book.find(name)
    if record:
        if record.delete_address(address):
            return suc(f"Address deleted from {name}.")
        return wrn(f"Address '{address}' not found for {name}.")
    return err("Contact not found.")


@input_error
def get_addresses(args=None, book=None, notes=None):
    name = args[0]
    record = book.find(name)
    if record:
        if record.has_address(""):
            addresses = record.str_addresses()
            return sch(f"{name}'s addresses: {addresses}")
        return wrn(f"{name} has no addresses.")
    return err("Contact not found.")


@input_error
def get_emails(args=None, book=None, notes=None):
    name = args[0]
    record = book.find(name)
    if record:
        if record.has_email(""):
            emails = record.str_emails()
            return sch(f"{name}'s emails: {emails}")
        return wrn(f"{name} has no emails.")
    return err("Contact not found.")


@input_error
def add_birthday(args=None, book=None, notes=None):
    name, birthday = args
    birthday = validate_birthday(birthday)
    record = book.find(name)
    if record:
        if record.has_birthday():
            print(wrn("Overwriting an existing birthday."))
            record.add_birthday(birthday)
            return suc(f"{name}'s birthday updated.")
        
        record.add_birthday(birthday)
        return suc(f"{name}'s birthday added.")
    return err("Contact not found.")


@input_error
def change_birthday(args=None, book=None, notes=None):
    name, birthday = args
    birthday = validate_birthday(birthday)
    record = book.find(name)
    if record:
        record.change_birthday(birthday)
        return suc(f"{name}'s birthday updated.")
    return err("Contact not found.")


@input_error
def delete_birthday(args=None, book=None, notes=None):
    name = args[0]
    record = book.find(name)
    if record:
        if record.delete_birthday():
            return suc(f"{name}'s birthday deleted.")
        return wrn("Birthday wasn't set.")
    return err("Contact not found.")


@input_error
def birthdays(args=None, book=None, notes=None):
    delta = int(args[0]) if args else 7
    today = datetime.today().date()
    upcoming = []
    for rec in book.data.values():
        if rec.has_birthday():
            bday = rec.birthday.value.replace(year=today.year)
            if bday < today:
                bday = bday.replace(year=today.year + 1)
            if 0 <= (bday - today).days <= delta:
                upcoming.append(f"{rec.str_name()}: {rec.str_birthday()}")
    if upcoming:
        return sch("\n".join(upcoming))
    return wrn("No upcoming birthdays.")


def find_contact(args=None, book=None, notes=None):
    field, query = args
    found_records = []

    field = field.lower()

    for record in book.data.values():
        if "name" in field:
            if record.has_name(query):
                found_records.append(record)
        elif "phone" in field:
            if record.has_phone(query):
                found_records.append(record)
        elif "email" in field:
            if record.has_email(query):
                found_records.append(record)
        elif "address" in field:
            if record.has_address(query):
                found_records.append(record)
        elif "birthday" in field:
            if record.has_birthday(query):
                found_records.append(record)
        else:
            return wrn(f"Unknown field: '{field}'.")

    if found_records:    
        return table_display_contacts(found_records, "Found Records")

    return wrn("No matching contacts found.")


@input_error
def add_note(args=None, book=None, notes=None):
    if len(args) > 0:
        return(wrn("To add a note, enter the add-note command and press Enter."))
    
    while True:
        title = input(inp("Enter note title: ")).strip()
        if not title:
            print(wrn("Title cannot be empty."))
            continue
        if title in notes.notes:
            print(wrn(f"Note with title '{title}' already exists."))
            continue
        else:
            break

    text = input(inp("Enter note text: ")).strip()

    note = Note(title, text)
    notes.add_note(note)

    print(inp("Add tags for this note (optional). Leave empty to stop."))
    while True:
        tag = input(inp("Enter tag: ")).strip()
        if not tag:
            break
        print(add_tag([title, tag], None, notes))

    print(suc(f"Note '{title}' added successfully."))


@input_error
def change_note(args=None, book=None, notes=None):
    """
    Interactively change the title and text of an existing note.
    """
    if len(args) > 0:
        return(wrn("To change a note, enter the change-note command and press Enter."))
    
    if not notes.notes:
        print(wrn("No notes to change."))
        return

    title = input(inp("Enter the title of the note to change: ")).strip()
    note = notes.find(title)
    if not note:
        print(err(f"Note '{title}' not found."))
        return

    print(sch(f"Current text: {note.content}"))
    new_text = input(inp("Enter new text (leave empty to keep current): ")).strip()
    if new_text:
        note.content = new_text

    while True:
        new_title = input(inp("Enter new title (leave empty to keep current): ")).strip()
        if not new_title:
            break
        if new_title in notes.notes and new_title != title:
            print(wrn(f"Note with title '{new_title}' already exists."))
            continue
        else:
            # Rename in the dict
            notes.notes[new_title] = notes.notes.pop(title)
            note.title = new_title
            break

    print(suc(f"Note '{note.title}' updated successfully."))


@input_error
def change_title(args=None, book=None, notes=None):
    title, new_title = args
    note = notes.find(title)
    if note:
        ## make a copy of record
        note.change_title(new_title)
        ## delete record
        notes.delete_note(title)
        ## add a new record    
        notes.add_note(note)
        return suc(f"{title}'s name updated.")
    return err("Note not found.")


@input_error
def delete_note(args=None, book=None, notes=None):
    title = args[0]
    if notes.delete_note(title):
        return suc(f"Note '{title}' deleted.")
    return err("Note not found.")


@input_error
def find_note(args=None, book=None, notes=None):
    keyword = args[0]
    found = notes.find_note(keyword)
    if found:
        return table_display_notes(found, keyword)
    return sch("No notes found.")


@input_error
def add_tag(args=None, book=None, notes=None):
    title, tag = args
    note = notes.find(title)
    if note:
        note.add_tag(tag)
        return suc(f"Tag '{tag}' added to note '{title}'.")
    return err("Note not found.")


@input_error
def find_tag(args=None, book=None, notes=None):
    tag = args[0]
    found = notes.find_by_tag(tag)
    if found:
        return table_display_notes(found, tag)
    return wrn("No notes found with this tag.")


@input_error
def edit_tag(args=None, book=None, notes=None):
    title, old_tag, new_tag = args
    note = notes.find(title)
    if note:
        note.edit_tag(old_tag, new_tag)
        return suc(f"Tag '{old_tag}' renamed to '{new_tag}' in note '{title}'.")
    return err("Note not found.")


@input_error
def delete_tag(args=None, book=None, notes=None):
    title, tag = args
    note = notes.find(title)
    if note:
        note.delete_tag(tag)
        return suc(f"Tag '{tag}' deleted from note '{title}'.")
    return err("Note not found.")


@input_error
def all_contacts(args=None, book=None, notes=None):
    if not book or not book.data:
        return wrn("No records found.")
    table_display_contacts(book.data.values(), "All Contacts")


def all_notes(args=None, book=None, notes=None):
    if not notes or not notes.notes:
        return wrn("No notes found.")
    return table_display_notes(notes.notes.values(), "All Notes")


@input_error
def exit_bot(args=None, book=None, notes=None):
    """
    Save data and exit the bot.
    """
    print(grt("Saving data and exiting... Goodbye!"))
    book.save_to_file()
    sys.exit()


# Aliases for commands
ALIASES = {
    "quit": "exit",
    "bye": "exit",
    "close": "exit",
    "create": "add",
    "remove": "delete-contact",
}


COMMANDS = {
    "help": (show_help, "help", "Show available commands", "Util"),
    "hello": (hello, "hello", "Greets the user", "Util"),
    "exit": (exit_bot, "exit", "Exit bot", "Util"),

    "all": (all_contacts, "all", "Show all contacts", "Contacts"),
    "add": (add_contact, "add <name> <phone>", "Add new contact and phone", "Contacts"),
    "find": (find_contact, "find <field> <keyword>", "Find contact", "Contacts"),
    "delete-contact": (delete_contact, "delete-contact <name>", "Delete Contact", "Contacts"),

    "add-phone": (add_phone, "add-phone <name> <new_phone>", "Adding a new phone number", "Contacts - Phone"),
    "change-phone": (change_phone, "change <name> <old_phone> <new_phone>", "Change existing phone number", "Contacts - Phone"),
    "delete-phone": (delete_phone, "delete <name> <phone>", "Delete existing phone number", "Contacts - Phone"),
    "phone": (get_phones, "phone <name>", "Show phone numbers for contact", "Contacts - Phone"),
    
    "change-name": (change_name, "change-name <old_name> <new_name>", "Change contact's name", "Contacts - Name"),

    "add-email": (add_email, "add-email <name> <email>", "Add email", "Contacts - Email"),
    "change-email": (change_email, "change-email <name> <new_email>", "Change email", "Contacts - Email"),
    "delete-email": (delete_email, "delete-email <name>", "Delete email", "Contacts - Email"),
    "emails": (get_emails, "emails <name>", "Show emails", "Contacts - Email"),

    "add-birthday": (add_birthday, "add-birthday <name> <DD.MM.YYYY>", "Add birthday", "Contacts - Birthday"),
    "change-birthday": (change_birthday, "change-birthday <name> <DD.MM.YYYY>", "Change birthday", "Contacts - Birthday"),
    "delete-birthday": (delete_birthday, "delete-birthday <name>", "Delete birthday", "Contacts - Birthday"),
    "birthdays": (birthdays, "birthdays <days>", "Show birthdays in next N days", "Contacts - Birthday"),

    "add-address": (add_address, "add-address <name> <address>", "Add address to contact", "Contacts - Address"),
    "change-address": (change_address, "change-address <name> <...>", "Change address", "Contacts - Address"),
    "delete-address": (delete_address, "delete-address <name>", "Delete address", "Contacts - Address"),
    "addresses": (get_addresses, "addresses <name>", "Show addresses", "Contacts - Address"),

    "all-note": (all_notes, "all-note", "Show all notes", "Notes"),
    "add-note": (add_note, "add-note <title> <content>", "Add note", "Notes"),
    "change-title": (change_title, "change-title <old_title> <new_title>", "Change note title", "Notes - Title"),
    "change-note": (change_note, "change-note <title> <new_content>", "Change note content", "Notes - Content"),
    "delete-note": (delete_note, "delete-note <title>", "Delete note", "Notes"),
    "find-note": (find_note, "find-note <keyword>", "Find note", "Notes - Content"),

    "add-tag": (add_tag, "add-tag <title> <tag>", "Add tag to note", "Notes - Tags"),
    "find-tag": (find_tag, "find-tag <tag>", "Find notes by tag", "Notes - Tags"),
    "edit-tag": (edit_tag, "edit-tag <title> <old_tag> <new_tag>", "Edit a tag", "Notes - Tags"),
    "delete-tag": (delete_tag, "delete-tag <title> <tag>", "Delete a tag", "Notes - Tags")
}
