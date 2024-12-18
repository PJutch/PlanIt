import json


def save(subjects, tasks):
    with open('save.json', 'w') as f:
        json.dump({'subjects': subjects.target_scores(), 'tasks': tasks.saved_data()}, f, ensure_ascii=True, indent=4)


def load(subjects, tasks):
    try:
        with open('save.json', 'r') as f:
            data = json.load(f)
            if 'subjects' in data:
                subjects.load_data(data['subjects'])
            if 'tasks' in data:
                tasks.load_data(data['tasks'])
    except FileNotFoundError:
        pass
    except json.decoder.JSONDecodeError:
        pass
    except ValueError:
        pass
    except TypeError:
        pass
