import random
import json
from pathlib import Path
import time

import dotenv

from src.api import (
    get_table_of_contents,
    get_section_content,
    get_instructor_notes
)
from src.api_parser import (
    parse_useful_data_from_table_of_contents_response,
    parse_useful_data_from_instructor_notes,
    parse_useful_data_from_section_response
)


def get_and_save_table_of_contents(course_id: str):
    """TODO Later"""
    asset_dir = Path('assets/courses') / course_id
    asset_dir.mkdir(parents=True, exist_ok=True)

    toc_file = asset_dir / 'toc_raw.json'

    if not toc_file.exists():
        print('Fetching table of contents...')
        toc = get_table_of_contents(course_id)
        toc_file.write_text(json.dumps(toc, indent=4))

    else:
        toc = json.loads(toc_file.read_text())

    return toc


def main():
    course_id = 'WGUD426v2'

    asset_dir = Path('assets/courses') / course_id
    asset_dir.mkdir(parents=True, exist_ok=True)

    toc_file = asset_dir / 'toc_raw.json'

    if not toc_file.exists():
        print('Fetching table of contents...')
        toc = get_table_of_contents(course_id)
        toc_file.write_text(json.dumps(toc, indent=4))

    else:
        toc = json.loads(toc_file.read_text())

    toc = parse_useful_data_from_table_of_contents_response(toc)
    toc_file = asset_dir / 'toc_useful.json'
    toc_file.write_text(json.dumps(toc, indent=4))

    for chapter in toc['chapters']:
        chapter_text = '# ' + chapter['title'] + '\n\n'

        for section in chapter['sections']:
            if section['title'].upper().startswith('LAB'):
                print(f'Skipping {chapter["number"]}.{section["number"]}. (lab section)')
                continue

            data_file = asset_dir / f'{chapter["number"]}' / f'{section["number"]}' / 'raw.json'
            data_file.parent.mkdir(parents=True, exist_ok=True)

            instructor_notes_file = (
                asset_dir /
                f'{chapter["number"]}' /
                f'{section["number"]}' /
                'instructor_notes_raw.json'
            )

            instructor_notes_file.parent.mkdir(parents=True, exist_ok=True)

            if not data_file.exists():
                data = get_section_content(course_id, chapter['number'], section['number'])
                data_file.write_text(json.dumps(data, indent=4))

                instructor_notes = get_instructor_notes(course_id, chapter['number'], section['number'])
                instructor_notes_file.write_text(json.dumps(instructor_notes, indent=4))

                delay = random.uniform(8, 12)
                print(f'Fetched {chapter["number"]}.{section["number"]}. Waiting {delay:.2f} seconds...')

                time.sleep(delay)
            
            else:
                data = json.loads(data_file.read_text())

            if not instructor_notes_file.exists():
                instructor_notes = get_instructor_notes(course_id, chapter['number'], section['number'])
                instructor_notes_file.write_text(json.dumps(instructor_notes, indent=4))

                delay = random.uniform(8, 12)
                print(f'Fetched instructor notes for {chapter["number"]}.{section["number"]}. Waiting {delay:.2f} seconds...')

                time.sleep(delay)

            else:
                instructor_notes = json.loads(instructor_notes_file.read_text())

            print(f'Processing {chapter["number"]}.{section["number"]}...')

            # USEFUL DATA

            data = parse_useful_data_from_section_response(data)
            data_file = asset_dir / f'{chapter["number"]}' / f'{section["number"]}' / 'useful.json'
            data_file.write_text(json.dumps(data, indent=4))

            instructor_notes = parse_useful_data_from_instructor_notes(instructor_notes)
            instructor_notes_file = (
                asset_dir /
                f'{chapter["number"]}' /
                f'{section["number"]}' /
                'instructor_notes_useful.json'
            )
            instructor_notes_file.write_text(json.dumps(instructor_notes, indent=4))

            # CONVERT TO TEXT

            data_text = ''

            for content in data['contents']:
                if content['type'] in ('markdown', 'terminology'):
                    data_text += content['markdown'] + '\n\n'

                if content['type'] in ('multiple_choice',):
                    data_text += f'## Multiple Choice\n\n'

                    for question in content['questions']:
                        data_text += f'### {question["question"]}\n\n'
                        correct_choice = None

                        for choice in question['choices']:
                            data_text += f'- {choice["text"]}\n'
                            if choice['is_correct']:
                                correct_choice = choice

                        if not correct_choice:
                            print(f'No correct choice found for question {question["question"]}')
                            continue

                        data_text += '\n\n'
                        data_text += f'**Correct Answer:** {correct_choice["text"]}\n\n'

            instructor_notes_text = '## Instructor Notes\n\n'

            for note in instructor_notes['notes']:
                instructor_notes_text += f'- {note["note"]}\n'

            # SAVE TEXT

            section_text = f'## {section["title"]}\n\n{data_text}\n\n{instructor_notes_text}'
            section_text = section_text.replace('\n\n\n\n', '\n\n')
            section_text = section_text.replace('\n\n\n', '\n\n')

            section_text_file = asset_dir / f'{chapter["number"]}' / f'{section["number"]}/text.md'
            section_text_file.write_text(section_text)

            chapter_text += section_text + '\n\n'

        chapter_text = chapter_text.replace('\n\n\n\n', '\n\n')
        chapter_text = chapter_text.replace('\n\n\n', '\n\n')

        chapter_text_file = asset_dir / f'{chapter["number"]}/text.md'
        chapter_text_file.write_text(chapter_text)


def reset_everything_except_raw():
    path = Path('assets/courses/WGUD426v2')

    for file in path.rglob('*.json'):
        if 'raw' not in file.stem:
            file.unlink()

    for file in path.rglob('*.md'):
        file.unlink()


if __name__ == '__main__':
    dotenv.load_dotenv()
    reset_everything_except_raw()
    main()
