def createInterval(start, finish, keys, key):
    new_interval = {}
    new_interval["start"] = start
    new_interval["finish"] = finish
    new_interval[key] = keys.copy()
    return new_interval


def getMainPermutations(intervals, key):
    conflicts = False
    new_intervals = []
    for start_interval in intervals:
        for compare_interval in intervals:
            if start_interval["start"] >= compare_interval["finish"] or start_interval["finish"] <= compare_interval["start"]:
                continue
            conflicts = True

            first_finish = start_interval["start"]
            if start_interval["start"] != compare_interval["start"]:
                first_start = min(start_interval["start"], compare_interval["start"])
                first_finish = max(start_interval["start"], compare_interval["start"])
                keys = start_interval[key] if start_interval["start"] < compare_interval["start"] else compare_interval[key]
                new_interval = createInterval(first_start, first_finish, keys, key)
                if new_interval not in new_intervals:
                    new_intervals.append(new_interval)

            last_start = start_interval["finish"]
            if start_interval["finish"] != compare_interval["finish"]:
                last_start = min(start_interval["finish"], compare_interval["finish"])
                last_finish = max(start_interval["finish"], compare_interval["finish"])
                keys = start_interval[key] if start_interval["finish"] > compare_interval["finish"] else compare_interval[key]
                new_interval = createInterval(last_start, last_finish, keys, key)
                if new_interval not in new_intervals:
                    new_intervals.append(new_interval)

            new_interval = createInterval(first_finish, last_start, start_interval[key].union(compare_interval[key]), key)
            if new_interval not in new_intervals:
                new_intervals.append(new_interval)
    return conflicts, new_intervals


def resolveConflicts(intervals, key):
    resolved_intervals = []
    skip = {}
    unresolved = False
    for i, start_interval in enumerate(intervals):
        if (start_interval["start"], start_interval["finish"]) in skip:
            continue

        conflict = False
        for j, compare_interval in enumerate(intervals):
            if start_interval["start"] == compare_interval["start"] and start_interval["finish"] > compare_interval["finish"]:
                compare_interval[key] = compare_interval[key].union(start_interval[key])
                conflict = True
                break

            if start_interval["start"] < compare_interval["start"] < start_interval["finish"]:
                unresolved = True

            elif (start_interval["start"], start_interval["finish"]) == (compare_interval["start"], compare_interval["finish"]):
                start_interval[key] = start_interval[key].union(compare_interval[key])
                skip[(start_interval["start"], start_interval["finish"])] = True

        if not conflict:
            resolved_intervals.append(start_interval)
    return unresolved, resolved_intervals

class Merge:
    @staticmethod
    def union(intervals: list, key: str = "set_items"):
        while True:
            conflict, intervals = getMainPermutations(intervals, key)
            unresolved, intervals = resolveConflicts(intervals, key) if conflict else (False, intervals)
            if not unresolved:
                break
            
        return intervals