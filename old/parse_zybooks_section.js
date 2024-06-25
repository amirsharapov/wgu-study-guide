function getSetOfClassLists() {
    let items;

    items = Array.from(document.querySelector('div.section-content-resources-container').children)
    items = items.map(e => Array.from(e.classList).join(','))
    items = Array.from(new Set(items))
    items = items.map(classList => classList.split(','))
    items = items.map(x => `[listToHashableKey('${x.join("', '")}')]`)

    return items
}


function listToHashableKey(list) {
    return list.sort().join(',');
}


function getTypeByElement(element) {
    const classList = Array.from(element.classList);

    const map = {
        [listToHashableKey(['content-resource', 'html-resource', 'html-content-resource', 'ember-view'])]: (
            'text'
        ),
        [listToHashableKey(['interactive-activity-container', 'animation-player-content-resource', 'participation', 'large', 'ember-view'])]: (
            'animation_player'
        ),
        [listToHashableKey(['instructor-note-container'])]: (
            'instructor_note'
        ),
        [listToHashableKey(['interactive-activity-container', 'custom-content-resource', 'participation', 'large', 'ember-view'])]: (
            'custom-resource'
        ),
        [listToHashableKey(['static-container', 'container-content-resource', 'aside-elaboration', 'large', 'ember-view'])] : (
            'aside'
        ),
        [listToHashableKey(['interactive-activity-container', 'multiple-choice-content-resource', 'participation', 'large', 'ember-view'])]: (
            'multiple_choice'
        ),
    };
    
    return map[listToHashableKey(classList)];
}

function getUsefulDataFromElement(element) {
    const type = getTypeByElement(element);
    
    if (type === 'text') {
        return getUsefulDataFromTextType(element);
    }
    if (type === 'instructor_note') {
        return getUsefulDataFromInstructorNoteType(element);
    }
    if (type === 'multiple_choice') {
        return getUsefulDataFromMultipleChoiceType(element);
    }
}

function getUsefulDataFromTextType(element) {
    const markdown = []

    for (const child of Array.from(element.children)) {
        if (child.tagName === 'H3') {
            markdown.push(`### ${child.innerText}`);
        }
        if (child.tagName === 'P') {
            markdown.push(child.innerText);
        }
        if (child.tagName === 'UL') {
            const localMarkdown = Array.from(child.children).map(li => {
                return `- ${li.innerText}`;
            }).join('\n');

            markdown.push(localMarkdown);
        }
        if (child.tagName === 'OL') {
            const localMarkdown = Array.from(child.children).map((li, index) => {
                return `${index + 1}. ${li.innerText}`;
            }).join('\n');

            markdown.push(localMarkdown);
        }
    }

    return {
        markdown: markdown.join('\n'),
    }
}

function getUsefulDataFromInstructorNoteType(element) {
    const content = element.querySelector('div.instructor-note-content');

    return {
        content: content.innerText
    }
}

function getUsefulDataFromAsideType(element) {
    const header = element.querySelector('div.static-container-header');
    const content = element.querySelector('div.static-container-payload');

    return {
        header: header.innerText,
        content: content.innerText
    }
}

function getUsefulDataFromMultipleChoiceType(element) {
    const question = element.querySelector('div.question-content').innerText;

    return {
        description: null,
        question: null,
        answers: null
    }
}

function getUsefulDataFromZyBooks() {
    return Array.from(document.querySelector('div.section-content-resources-container').children).map(element => {
        return {
            type: getTypeByElement(element),
            data: getUsefulDataFromElement(element),
            element,
        }
    })
}

getUsefulDataFromZyBooks()