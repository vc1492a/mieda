from operator import itemgetter

def createInterval(start, finish, keys, key):
    new_interval = {}
    new_interval["start"] = start
    new_interval["finish"] = finish
    new_interval[key] = keys.copy()
    return new_interval


def getMainPermutations(intervals, key):
    conflicts = False
    new_intervals = []
    intervals = sorted(intervals, key=itemgetter("start", "finish"))
    for start_interval in intervals:
        min_start = start_interval["start"]
        max_list = [start_interval["finish"]]
        for compare_interval in intervals:
            if compare_interval["finish"] <= start_interval["start"]:
                continue
            elif compare_interval["start"] > start_interval["finish"]:
                break
            conflicts = True

            if start_interval["start"] < compare_interval["start"] < start_interval["finish"]:
                max_list.append(compare_interval["start"])
            if start_interval["start"] < compare_interval["finish"] < start_interval["finish"]:
                max_list.append(compare_interval["finish"])

        max_list = sorted(max_list)
        for end in max_list:
            if min_start == end:
                continue
            new_intervals.append(createInterval(min_start, end, start_interval[key], key))
            min_start = end


    return conflicts, new_intervals


def resolveConflicts(intervals, key):
    resolved_intervals = []
    skip = {}
    for i, start_interval in enumerate(intervals):
        if (start_interval["start"], start_interval["finish"]) in skip:
            continue

        conflict = False
        for j, compare_interval in enumerate(intervals):
            if start_interval["start"] == compare_interval["start"] and start_interval["finish"] > compare_interval["finish"]:
                compare_interval[key] = compare_interval[key].union(start_interval[key])
                conflict = True
                break

            elif (start_interval["start"], start_interval["finish"]) == (compare_interval["start"], compare_interval["finish"]):
                start_interval[key] = start_interval[key].union(compare_interval[key])
                skip[(start_interval["start"], start_interval["finish"])] = True

        if not conflict:
            resolved_intervals.append(start_interval)
    return resolved_intervals

class Merge:
    @staticmethod
    def union(intervals: list, key: str = "set_items"):
        conflict, intervals = getMainPermutations(intervals, key)
        if conflict:
            intervals = resolveConflicts(intervals, key)
        return intervals