import enum
from typing import Dict


class NoteType(enum.Enum):
    """Taiko note types
    """
    DON = 1
    KA = 2
    BIG_DON = 3
    BIG_KA = 4
    DRUMROLL = 5
    BIG_DRUMROLL = 6
    BALLOON = 7


class Note:
    """Generic taiko note
    """

    def __init__(self, note_type: NoteType, start_time: float):
        self.note_type = note_type
        self.start_time = start_time
        self.end_time = None


class Course:
    """Taiko course
    """

    def __init__(self, slug: str, metadata: Dict):
        self.slug = slug
        self.metadata = metadata
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def get_last_note(self) -> "Note":
        return self.notes[-1]
