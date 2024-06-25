import json
from dataclasses import dataclass, field
from pathlib import Path

BASE_PATH = Path('assets/courses')


@dataclass
class Course:
    id: str
    chapters: list['Chapter'] = field(default_factory=list)

    @property
    def path(self):
        return BASE_PATH / self.id

    def mkdir(self):
        self.path.mkdir(parents=True, exist_ok=True)


@dataclass
class TableOfContents:
    course: Course
    buffer: dict = field(default_factory=dict)

    @property
    def path_to_raw(self):
        return self.course.path / 'toc_raw.json'

    @property
    def path_to_useful(self):
        return self.course.path / 'toc_useful.json'

    def load_useful_buffer(self):
        if not self.buffer:
            self.buffer = json.loads(self.path_to_useful.read_text())

    def list_chapters(self):
        self.load_useful_buffer()
        return [
            Chapter(self.course, chapter['number']) for
            chapter in
            self.buffer['chapters']
        ]

    def list_sections(self, chapter: 'Chapter'):
        self.load_useful_buffer()
        return [
            Section(chapter, section['number']) for
            section in
            self.buffer['chapters'][chapter.number - 1]['sections']
        ]


@dataclass
class Chapter:
    course: 'Course'
    number: int
    sections: list['Section'] = field(default_factory=list)

    @property
    def path(self):
        return self.course.path / f'{self.number}'


@dataclass
class Section:
    section: 'Chapter'
    number: int

    @property
    def path(self):
        return self.section.path / f'{self.number}'

    @property
    def path_to_raw_content(self):
        return self.path / 'raw.json'

    @property
    def path_to_useful_content(self):
        return self.path / 'useful.json'


@dataclass
class InstructorNotes:
    section: 'Section'
    notes: str

    @property
    def path_to_raw(self):
        return self.section.path / 'instructor_notes_raw.json'

    @property
    def path_to_useful(self):
        return self.section.path / 'instructor_notes_useful.json'
