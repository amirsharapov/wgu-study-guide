import requests

from src.constants import BASE_URL, BEARER_TOKEN


def make_headers():
    return {
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }


def handle_response(response):
    response.raise_for_status()

    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        print(response.text)
        return None

    return response.json()


def get_table_of_contents(course_id: str):
    url = BASE_URL + '/zybooks'
    params = {'zybooks': f'["{course_id}"]'}
    headers = make_headers()

    response = requests.get(
        url=url,
        headers=headers,
        params=params
    )

    return handle_response(response)


def get_section_content(course_id: str, chapter_number: int, section_number: int):
    url = BASE_URL + f'/zybook/{course_id}/chapter/{chapter_number}/section/{section_number}'
    headers = make_headers()

    response = requests.get(
        url=url,
        headers=headers
    )

    return handle_response(response)


def get_instructor_notes(course_id: str, chapter_number: int, section_number: int):
    url = BASE_URL + f'/zybook/{course_id}/chapter/{chapter_number}/section/{section_number}/instructor_notes'
    headers = make_headers()

    response = requests.get(
        url=url,
        headers=headers
    )

    return handle_response(response)
