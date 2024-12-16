import copy
import collections


Task = collections.namedtuple('Tasks', ['name', 'subject', 'score', 'time', 'deadline'])


def plan(current_time: int, target_score: dict[str, int], tasks: list[Task]) -> list[int]:
    reached_score = {subject: 0 for subject in target_score}
    for task in tasks:
        reached_score[task.subject] += task.score

    order = sorted((i for i in range(len(tasks))), key=lambda index: tasks[index].deadline)
    done_tasks = []
    for i in order:
        if current_time + tasks[i].time <= tasks[i].deadline:
            done_tasks.append(i)
            current_time += tasks[i].time
        else:
            rollback_time = current_time
            will_cancel = []
            for cancelled in reversed(done_tasks):
                if rollback_time + tasks[i].time <= tasks[i].deadline:
                    break

                rollback_time -= tasks[cancelled].time
                will_cancel.append(cancelled)

            score_after_cancel = copy.copy(reached_score)
            for cancelled in will_cancel:
                score_after_cancel[tasks[cancelled].subject] -= tasks[cancelled].score

            target_losses = sum(max(target_score[subject] - score_after_cancel[subject], 0)
                                for subject in target_score)
            extra_losses = sum(max(reached_score[subject] - max(target_score[subject], score_after_cancel[subject]), 0)
                               for subject in target_score)

            subject = tasks[i].subject
            target_benefit = max(target_score[subject] - reached_score[subject] + tasks[i].score, 0)
            extra_benefit = max(min(tasks[i].score, reached_score[subject] - target_score[subject]), 0)

            if target_benefit > target_losses or target_benefit == target_losses and extra_benefit > extra_losses:
                for cancelled in will_cancel:
                    reached_score[tasks[cancelled].subject] -= tasks[cancelled].score

                done_tasks = done_tasks[:-len(will_cancel)]
                done_tasks.append(i)

                current_time = rollback_time + tasks[i].time
            else:
                reached_score[subject] -= tasks[i].score

    return done_tasks
