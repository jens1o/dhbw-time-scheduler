from numpy import arange


def get_half_hour_range(start: float, end: float) -> list:
    return list(arange(start=start, stop=end, step=0.5))