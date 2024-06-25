from src.utils import markdownify_html


def parse_useful_data_from_table_of_contents_response(toc: dict):
    data = {
        'chapters': []
    }

    chapters = toc['zybooks'][0]['chapters']

    for chapter in chapters:
        chapter_data = {
            'number': chapter['number'],
            'title': chapter['title'],
            'sections': []
        }

        for section in chapter['sections']:
            section_data = {
                'number': section['number'],
                'title': section['title']
            }

            chapter_data['sections'].append(section_data)

        data['chapters'].append(chapter_data)

    return data


def parse_useful_data_from_instructor_notes(data: dict):
    notes = {
        'notes': [],
    }

    for note in data['instructor_notes']:
        notes['notes'].append({
            'type': 'instructor_note',
            'note': markdownify_html(note['note'])
        })

    return notes


def parse_useful_data_from_section_response(section: dict):
    data = {
        'contents': []
    }

    resources = section['section']['content_resources']

    for resource in resources:
        if resource['type'] == 'html':
            data['contents'].append({
                'type': 'markdown',
                'markdown': markdownify_html(resource['payload']['html'])
            })
            continue

        if resource['type'] == 'container':
            name = resource['payload']['name']

            if name.lower() in ('figure', 'table'):
                continue

            if name:
                data['contents'].append({
                    'type': name.lower(),
                    'markdown': markdownify_html(resource['payload']['html'])
                })
                continue

            print('Unhandled container:', name)
            continue

        if resource['type'] == 'custom':
            continue

        if resource['type'] == 'multiple_choice':
            questions = []

            for question in resource['payload']['questions']:
                question_data = {
                    'question': markdownify_html(question['text']),
                    'choices': []
                }

                for choice in question['choices']:
                    question_data['choices'].append({
                        'text': markdownify_html(choice['label']),
                        'is_correct': choice['correct'],
                        'explanation': markdownify_html(choice['explanation'])
                    })

                questions.append(question_data)

            data['contents'].append({
                'type': 'multiple_choice',
                'questions': questions
            })
            continue

        if resource['type'] in ('exercise', 'image', 'short_answer'):
            continue

        print('Unhandled resource:', resource['type'])

    return data
