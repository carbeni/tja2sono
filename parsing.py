import re
from typing import List
from taiko import NoteType, Note, Course

metadata_re = re.compile(r"^([A-Z]+):(.+)$")
notes_re = re.compile(r"^(\d+),\s*(//.+)?$")


class Parser:
    """Parse TJA
    """

    def __init__(self, f):
        self.line_idx = 0
        self.lines = f.readlines()
        self.courses = []
        self.metadata = {}
        self.is_end = False
        self.is_parsing_song = False
        self.song_time = 0  # current song time in seconds
        self.current_course = None
        self.bpm = None
        self.measure = 1
        self.offset = None

    def parse(self):
        while self.has_more():
            self.step()

    def has_more(self) -> bool:
        return not self.is_end

    def step(self):
        if self.line_idx >= len(self.lines):
            self.is_end = True
            return

        line = self.lines[self.line_idx].strip()
        if line.startswith("#"):
            # Parse operation
            if line.startswith("#START"):
                self.__parse_start()
            elif line.startswith("#END"):
                self.__parse_end()
            elif line.startswith("#MEASURE"):
                self.__parse_measure(line)
            else:
                # no-op, ignore
                pass
        elif notes_re.match(line) != None:
            # Parse notes
            self.__parse_notes(line)
        elif metadata_re.match(line):
            # Parse metadata
            self.__parse_metadata(line)

        self.line_idx += 1

    def __parse_start(self):
        self.is_parsing_song = True
        self.song_time = -float(self.metadata["OFFSET"])
        self.bpm = int(self.metadata["BPM"])
        self.current_course = Course(
            slug=generate_slug(
                self.metadata["TITLE"], self.metadata["COURSE"]),
            metadata=self.metadata.copy(),
        )

    def __parse_end(self):
        self.is_parsing_song = False
        self.courses.append(self.current_course)

    def __parse_metadata(self, line: str):
        m = metadata_re.match(line)
        self.metadata[m.group(1)] = m.group(2)

    def __parse_measure(self, line: str):
        raw_frac = line.split(" ")[1].split("/")
        self.measure = int(raw_frac[0]) / int(raw_frac[1])

    def __parse_notes(self, line: str):
        m = notes_re.match(line)
        notes = [int(n) for n in m.group(1)]
        measure_dt = 60 * self.measure * 4 / self.bpm
        note_dt = measure_dt / len(notes)
        for note in notes:
            if note == 0:
                pass
            elif note == 1:
                self.current_course.add_note(
                    Note(NoteType.DON, self.song_time)
                )
            elif note == 2:
                self.current_course.add_note(
                    Note(NoteType.KA, self.song_time)
                )
            elif note == 3:
                self.current_course.add_note(
                    Note(NoteType.BIG_DON, self.song_time)
                )
            elif note == 4:
                self.current_course.add_note(
                    Note(NoteType.BIG_KA, self.song_time)
                )
            elif note == 5:
                self.current_course.add_note(
                    Note(NoteType.DRUMROLL, self.song_time)
                )
            elif note == 6:
                self.current_course.add_note(
                    Note(NoteType.BIG_DRUMROLL, self.song_time)
                )
            elif note == 7:
                self.current_course.add_note(
                    Note(NoteType.BALLOON, self.song_time)
                )
            elif note == 8:
                self.current_course.get_last_note().end_time = self.song_time

            self.song_time += note_dt


def generate_slug(*args: List[str]):
    return ".".join([
        "_".join([
            re.sub(r"[^a-zA-Z0-9]", "", part).lower() for part in s.split(" ")
        ])
        for s in args
    ])
