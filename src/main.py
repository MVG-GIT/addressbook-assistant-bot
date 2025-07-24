from src.models.contacts import AddressBook
from src.models.notes import Notes
from src.utils.autocomplete import smart_guess
from src.storage.persistence import load_contacts, save_contacts, load_notes, save_notes
from src.commands import COMMANDS, ALIASES, parse_input, show_help

from src.utils.styling import err, wrn, grt, suc, inp

def main():
    book = load_contacts()
    notes = load_notes()

    print(grt("Welcome to the Assistant Bot!"))
    show_help()

    while True:
        try:
            user_input = input(inp("Enter a command: ")).strip()

            if not user_input:
                continue

            command, args = parse_input(user_input)

            guessed_command = smart_guess(command, COMMANDS, ALIASES)

            if guessed_command in ["close", "exit"]:
                save_contacts(book)
                save_notes(notes)
                print(grt("Good bye! Data saved (and sent to Pentagon)."))
                break

            if guessed_command is None:
                print(err(f"Unknown command '{command}'. Type 'help' to see available commands."))
                continue

            # If guessed command differs from input command, ask for confirmation
            if guessed_command != command:
                answer = input(wrn(f"Not sure what '{command}' meant. Did you mean '") + suc(guessed_command) + wrn("'? (Y/N): ")).strip().lower()
                if answer != 'y':
                    continue

            # Execute command with args
            result = COMMANDS[guessed_command][0](args, book, notes)
            if result:
                print(result)

        except Exception as e:
            print(err(f"[bold red]Unexpected error: {e}"))

if __name__ == "__main__":
    main()
