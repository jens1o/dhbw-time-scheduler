import random
import sys
import time
from constraint import *
from itertools import chain

from functions.functions import get_half_hour_range

# 24-hour formatted value when the student goes to bed
GO_TO_BED_TIME = 22
HOURS_OF_SLEEP = 8

MONDAY = 0
TUESDAY = MONDAY + 24
WEDNESDAY = TUESDAY + 24
THURSDAY = WEDNESDAY + 24
FRIDAY = THURSDAY + 24
SATURDAY = FRIDAY + 24
SUNDAY = SATURDAY + 24


class Lecture():
    def __init__(self, name: str, lecture_start: int, lecture_end: int, self_study_time_per_day: float) -> None:
        assert lecture_start < lecture_end and lecture_start >= MONDAY and lecture_end < SUNDAY + 24

        self.name = name
        self.lecture_start = lecture_start
        self.lecture_end = lecture_end
        self.self_study_time = self_study_time_per_day

    def __str__(self) -> str:
        return self.name

def get_awake_hours() -> list:
    assert GO_TO_BED_TIME > 0 and GO_TO_BED_TIME < 24
    assert HOURS_OF_SLEEP > 0 and HOURS_OF_SLEEP < 24

    # special handling when we are not sleeping at midnight
    if (GO_TO_BED_TIME + HOURS_OF_SLEEP) < 24:
        return list(chain(get_half_hour_range(0, GO_TO_BED_TIME), get_half_hour_range(GO_TO_BED_TIME + HOURS_OF_SLEEP, 24 - GO_TO_BED_TIME + HOURS_OF_SLEEP)))

    return list(get_half_hour_range((GO_TO_BED_TIME + HOURS_OF_SLEEP) % 24, GO_TO_BED_TIME))


AWAKE_HOURS = []

for hour in get_awake_hours():
    for day in range(0, 8):
        AWAKE_HOURS.append(hour + day * 24)
AWAKE_HOURS.sort()

problem = Problem()

lectures = [
    Lecture("Databases", WEDNESDAY + 13, WEDNESDAY + 15.5, 0.5),
    Lecture("Formal Languages and Automata",
            WEDNESDAY + 9, WEDNESDAY + 12, 1),
    Lecture("Maths", MONDAY + 8, MONDAY + 11, 1),
    Lecture("Computer Architecture", TUESDAY + 8.5, TUESDAY + 12, 0.5),
    Lecture("Communication and Networks", TUESDAY + 16, TUESDAY + 17.5, 0.5),
    Lecture("Software Engineering", THURSDAY + 8, THURSDAY + 12.5, 0.5),
    Lecture("Web-Engineering", FRIDAY + 8.5, FRIDAY + 12, 1)
]

random.shuffle(lectures)

# gather hours where the student is sitting in a lecture
lecture_times = []
for lecture in lectures:
    lecture_times.extend(get_half_hour_range(
        lecture.lecture_start, lecture.lecture_end))

lunch_break_times = set()

lunch_break_range = get_half_hour_range(12.5, 13.5)
for i in range(0, 8):
    for lunch_break_timepoint in lunch_break_range:
        lunch_break_times.add(lunch_break_timepoint + 24 * i)

hours_available_for_learning = list(
    set(AWAKE_HOURS) - set(lecture_times) - lunch_break_times)
print(hours_available_for_learning)

for lecture in lectures:
    problem.addVariable("selfstudy_" + lecture.name,
                        hours_available_for_learning)


checks_run = 0


def check_non_overlapping_self_study_times_constraint(*args):
    global checks_run

    assert len(args) == len(lectures)

    i = 0
    blocked_times = set()
    for lecture in lectures:
        proposed_self_study_time = args[i]

        for item in get_half_hour_range(
                proposed_self_study_time, proposed_self_study_time + lecture.self_study_time):

            if item in blocked_times:
                checks_run += 1
                if checks_run % 50000 == 0:
                    print(f"{checks_run}…")
                return False

            blocked_times.add(item)

        i += 1

    return True

problem.addConstraint(AllDifferentConstraint())
problem.addConstraint(check_non_overlapping_self_study_times_constraint)

start_time = time.monotonic()

for solution in problem.getSolutionIter():
    duration = time.monotonic() - start_time

    print(f"needed to do {checks_run} checks")
    print(solution)
    print(duration)
