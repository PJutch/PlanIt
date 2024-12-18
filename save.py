import json


def save(subjects, tasks):
    with open('save.json', 'w') as f:
        json.dump({'subjects': subjects.target_scores(), 'tasks': tasks.tasks()}, f, ensure_ascii=True, indent=4)
