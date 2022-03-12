from typing import Dict
import re
from taiko import NoteType, Course

nodetype2archetype = {
    NoteType.DON: 2,
    NoteType.KA: 3,
    NoteType.BIG_DON: 4,
    NoteType.BIG_KA: 5,
    NoteType.DRUMROLL: 6,
    NoteType.BIG_DRUMROLL: 7,
    NoteType.BALLOON: 8,  # TODO: this is a guess
}


def convert_to_sonolus_info(course: Course) -> Dict:
    return {
        "version": 1,
        "rating": int(course.metadata["LEVEL"]),
        "engine": "taiko.classic",
        "useSkin": {
            "useDefault": True
        },
        "useBackground": {
            "useDefault": True
        },
        "useEffect": {
            "useDefault": True
        },
        "useParticle": {
            "useDefault": True
        },
        "title": {
            "en": re.sub(r"[^a-zA-Z0-9\s]", "", course.metadata["TITLE"])
        },
        "artists": {
            "en": ""
        },
        "author": {
            "en": ""
        },
        "description": {
            "en": ""
        }
    }


def convert_to_sonolus_data(course: Course) -> Dict:
    notes = []
    for note in course.notes:
        values = [
            float(course.metadata["BPM"]),
            note.start_time,
        ]
        if note.end_time != None:
            values.append(note.end_time)
        sonolus_note = {
            "archetype": nodetype2archetype[note.note_type],
            "data": {
                "index": 0,
                "values": values,
            }
        }
        notes.append(sonolus_note)
    return {
        "entities": [
            {
                "archetype": 0
            },
            {
                "archetype": 1
            },
            *notes,
        ]
    }
