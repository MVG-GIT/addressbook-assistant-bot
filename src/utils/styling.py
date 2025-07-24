from colorama import Fore, Back, Style, init
from rich.table import Table
from rich import box
from rich.console import Console

console = Console()
init(autoreset=True)

STYLES = {
    "success": f"{Fore.GREEN}{Style.BRIGHT}",
    "error": f"{Fore.RED}{Style.BRIGHT}",
    "warning": f"{Fore.YELLOW}{Style.BRIGHT}",
    
    "input": f"{Fore.YELLOW}",
    
    "greet": f"{Fore.CYAN}{Style.BRIGHT}",
    
    "info": f"{Fore.BLUE}",
    "info2": f"{Fore.BLUE}{Style.BRIGHT}",

    "reset": f"{Style.RESET_ALL}",

    "search": f"{Fore.CYAN}"
}

def style(type_, text):
    prefix = STYLES.get(type_, STYLES["reset"])
    return style_custom(prefix, text)

def style_custom(prefix, text):
    return f"{prefix}{text}{Style.RESET_ALL}"

def err(text):
    return style("error", text)

def wrn(text):
    return style("warning", text)

def inf2(text):
    return style("info2", text)

def inf1(text):
    return style("info", text)

def suc(text):
    return style("success", text)

def inp(text):
    return style("input", text)

def grt(text):
    return style("greet", text)

def sch(text):
    return style("search", text)


def table_display_notes(items, title):
    table = Table(title=title, title_style="bold magenta", box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("Title", style="bold green")
    table.add_column("Content", style="cyan")
    table.add_column("Tags", style="yellow")

    for note in items:
        tags = note.str_tags()
        content = note.str_content_short()
        table.add_row(note.title, content, tags)

    console.print(table)
    return ""


def table_display_contacts(items, title):
    table = Table(title=title, title_style="bold magenta", box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("Name", style="bold green")
    table.add_column("Phones", style="cyan")
    table.add_column("Emails", style="yellow")
    table.add_column("Birthday", style="blue")
    table.add_column("Addresses", style="magenta")
    
    for record in items:
        name = record.str_name()
        phones = record.str_phones()
        email = record.str_emails()
        birthday = record.str_birthday()
        addresses = record.str_addresses()

        table.add_row(name, phones, email, birthday, addresses)

    console.print(table)
    return ""


def table_display_help(commands, aliases):
    table = Table(title="Available Commands", title_style="bold cyan", box=box.SIMPLE_HEAVY)
    table.add_column("Command", style="bold green", no_wrap=True)
    table.add_column("Aliases", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Usage", style="dim")

    # Reverse map: command -> list of its aliases
    command_aliases = {}
    for alias, canonical in aliases.items():
        command_aliases.setdefault(canonical, []).append(alias)

    # Group commands by their group name
    grouped_commands = {}
    for cmd, (func, usage, desc, group) in commands.items():
        grouped_commands.setdefault(group, []).append((cmd, usage, desc))

    # Sort groups alphabetically
    for group in sorted(grouped_commands.keys()):
        # Add a header row for group
        table.add_row(f"[bold magenta][center]{group}[/center][/bold magenta]", "", "", "")
        
        # Sort commands inside group alphabetically by command name
        for cmd, usage, desc in sorted(grouped_commands[group], key=lambda x: x[0]):
            aliases = ", ".join(sorted(command_aliases.get(cmd, [])))
            table.add_row(cmd, aliases, desc, usage)


    console.print(table)
    return ""
