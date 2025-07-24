from typing import List, Dict, Optional

class Note:
    """Class representing a single note with title, content, and tags."""

    def __init__(self, title: str, content: str):
        self.title: str = title
        self.content: str = content
        self.tags = []
            
    def change_title(self, new_title):
        """Change name."""
        self.title = new_title

    def add_tag(self, tag: str) -> None:
        """Add a unique tag to the note."""
        if tag in self.tags:
            raise ValueError(f"Tag '{tag}' already exists in '{self.title}'.")
        self.tags.append(tag)

    def edit_tag(self, old_tag: str, new_tag: str) -> None:
        """Rename an existing tag, ensuring uniqueness."""
        if old_tag not in self.tags:
            raise ValueError(f"Tag '{old_tag}' not found in '{self.title}'.")
        if new_tag in self.tags:
            raise ValueError(f"Tag '{new_tag}' already exists in '{self.title}'.")
        idx = self.tags.index(old_tag)
        self.tags[idx] = new_tag

    def delete_tag(self, tag: str) -> None:
        """Remove a tag from the note."""
        if tag not in self.tags:
            raise ValueError(f"Tag '{tag}' not found in '{self.title}'.")
        self.tags.remove(tag)
        
    def str_tags(self):
        return  ", ".join(self.tags) if self.tags else "No tags"
    
    def str_content_short(self):
        return self.content if len(self.content) <= 50 else self.content[:50] + "..."

    def __str__(self) -> str:
        tags_str = self.str_tags()
        return f"[{self.title}] {self.content} (Tags: {tags_str})"


class Notes:
    """Class for managing multiple notes."""

    def __init__(self):
        self.notes: Dict[str, Note] = {}

    def add_note(self, note: Note) -> None:
        """Add a new note."""
        self.notes[note.title] = note

    def find(self, title: str) -> Optional[Note]:
        """Find a note by its title."""
        return self.notes.get(title)

    def find_note(self, keyword: str) -> List[Note]:
        """Find notes containing the keyword in all (case insensitive)."""
        keyword_lower = keyword.lower()
        return [
            note for note in self.notes.values()
            if keyword_lower in note.content.lower()
            or keyword_lower in note.title.lower()
            or any(keyword_lower in tag.lower() for tag in note.tags)
        ]
        
    def delete_note(self, title: str) -> bool:
        """Delete a note by title."""
        if title in self.notes:
            del self.notes[title]
            return True
        return False

    def change_note(self, title: str, new_content: str) -> bool:
        """Change content of an existing note."""
        note = self.find(title)
        if note:
            note.content = new_content
            return True
        return False
    
    def find_by_tag(self, tag: str) -> List[Note]:
        """Find notes containing a specific tag."""
        return [note for note in self.notes.values() if tag in note.tags]