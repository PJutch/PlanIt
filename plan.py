import copy
import collections

Task = collections.namedtuple('Tasks', ['name', 'subject', 'score', 'time', 'deadline'])


def score(current_score: dict[str, int], target_score: dict[str, int]):
    target = sum(min(target_score[subject], current_score[subject]) for subject in target_score)
    extra = sum(max(current_score[subject] - target_score[subject], 0) for subject in target_score)
    return target, extra


def plan(current_time: int, target_score: dict[str, int], tasks: list[Task]) -> list[int]:
    dp = [{current_time: {subject: 0 for subject in target_score.keys()}}]
    is_taken = [{}]

    order = sorted(range(len(tasks)), key=lambda i: tasks[i].deadline)
    for task_idx in order:
        dp.append(copy.copy(dp[-1]))
        is_taken.append({time: False for time in dp[-1]})

        for time, scores in dp[-2].items():
            end_time = time + tasks[task_idx].time
            if end_time > tasks[task_idx].deadline:
                continue

            new_current_score = copy.copy(scores)
            new_current_score[tasks[task_idx].subject] += tasks[task_idx].score

            if end_time not in dp[-1] or score(new_current_score, target_score) > score(dp[-1][end_time], target_score):
                dp[-1][end_time] = new_current_score
                is_taken[-1][end_time] = True

    best = None
    for time, scores in dp[-1].items():
        if best is None or score(scores, target_score) > score(dp[-1][best], target_score):
            best = time

    taken = []
    for i in range(len(dp) - 1, 0, -1):
        if is_taken[i][best]:
            best -= tasks[order[i - 1]].time
            taken.append(order[i - 1])
    return list(reversed(taken))
