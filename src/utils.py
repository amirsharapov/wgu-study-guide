import markdownify


def markdownify_html(html: str | dict | list):
    res = None

    if isinstance(html, str):
        res = markdownify.markdownify(html)

    if isinstance(html, dict):
        text = html.get('text')
        if text:
            res = markdownify.markdownify(html['text'])
        else:
            res = ''

    if isinstance(html, list):
        markdowns = []
        for item in html:
            markdowns.append(markdownify_html(item))

        res = '\n'.join(markdowns)

    if res is not None:
        return res.strip().replace('\n\n', '\n')

    raise ValueError('Invalid HTML data')
