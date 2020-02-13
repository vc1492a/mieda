import datetime
from typing import Tuple, Union


def create_interval(start: Union[str, int, float, 'datetime.datetime'], finish: Union[str, int, float, 'datetime.datetime'], keys: dict, key: Union[str, int, float, 'datetime.datetime']) -> dict:
    """
    Takes a set of data pertaining to an interval and creates a properly formed interval dictionary object.
    :param start: A string, integer, float, or datetime object indicating the start of an interval.
    :param finish:  A string, integer, float, or datetime object indicating the finish of an interval.
    :param keys: A set of keys for the interval, usually indicating its source.
    :param key:  A string, integer, float, or datetime object to use as the key for the interval.
    :return: a properly formed interval dictionary object.
    """

    new_interval = dict({"start": start, "finish": finish})
    new_interval[key] = keys
    return new_interval


def get_main_permutations(intervals: list, key: Union[str, int, float, 'datetime.datetime']) -> Tuple[bool, list]:
    """
    Takes a set of intervals and returns the main permutations and a boolean indicating whether a conflict is
    present in the intervals passed.
    :param intervals: A list of intervals.
    :param key: A string, integer, float, or datetime object to use as the key for the intervals.
    :return: A boolean and list of intervals.
    """

    conflicts = False
    new_intervals = list()
    for start_interval in intervals:
        for compare_interval in intervals:
            if start_interval["start"] >= compare_interval["finish"] or start_interval["finish"] <= compare_interval[
                    "start"]:
                continue
            conflicts = True

            first_finish = start_interval["start"]
            if start_interval["start"] != compare_interval["start"]:
                first_start = min(start_interval["start"], compare_interval["start"])
                first_finish = max(start_interval["start"], compare_interval["start"])
                keys = start_interval[key] if start_interval["start"] < compare_interval["start"] else compare_interval[
                    key]
                new_interval = create_interval(first_start, first_finish, keys, key)
                if new_interval not in new_intervals:
                    new_intervals.append(new_interval)

            last_start = start_interval["finish"]
            if start_interval["finish"] != compare_interval["finish"]:
                last_start = min(start_interval["finish"], compare_interval["finish"])
                last_finish = max(start_interval["finish"], compare_interval["finish"])
                keys = start_interval[key] if start_interval["finish"] > compare_interval["finish"] else \
                    compare_interval[key]
                new_interval = create_interval(last_start, last_finish, keys, key)
                if new_interval not in new_intervals:
                    new_intervals.append(new_interval)

            new_interval = create_interval(first_finish, last_start, start_interval[key].union(compare_interval[key]),
                                          key)
            if new_interval not in new_intervals:
                new_intervals.append(new_interval)
    return conflicts, new_intervals


def resolve_conflicts(intervals: list, key: Union[str, int, float, 'datetime.datetime']) -> Tuple[bool, list]:
    """
    Takes a list of intervals and returns a new list of intervals and a boolean indicating whether or not the
    conflicts have been resolved.
    :param intervals: A list of intervals.
    :param key: A string, integer, float, or datetime object to use as the key for the intervals.
    :return: A boolean and list of intervals.
    """

    resolved_intervals = list()
    skip = dict()
    unresolved = False
    for i, start_interval in enumerate(intervals):
        if (start_interval["start"], start_interval["finish"]) in skip:
            continue

        conflict = False
        for j, compare_interval in enumerate(intervals):
            if start_interval["start"] == compare_interval["start"] and start_interval["finish"] > compare_interval[
                    "finish"]:
                compare_interval[key] = compare_interval[key].union(start_interval[key])
                conflict = True
                break

            if start_interval["start"] < compare_interval["start"] < start_interval["finish"]:
                unresolved = True

            elif (start_interval["start"], start_interval["finish"]) == (
                    compare_interval["start"], compare_interval["finish"]):
                start_interval[key] = start_interval[key].union(compare_interval[key])
                skip[(start_interval["start"], start_interval["finish"])] = True

        if not conflict:
            resolved_intervals.append(start_interval)
    return unresolved, resolved_intervals


class Merge:

    @staticmethod
    def union(intervals: list, key: str = "set_items"):
        """
        Combines a list of potentially conflicting intervals into a list of de-conflicted intervals with joined labels
        :param intervals: A list of intervals.
        :param key: A string to use as the key for the interval.
        :return: A set of merged intervals.
        """

        while True:
            conflict, intervals = get_main_permutations(intervals, key)
            unresolved, intervals = resolve_conflicts(intervals, key) if conflict else (False, intervals)
            if not unresolved:
                break

        return intervals
