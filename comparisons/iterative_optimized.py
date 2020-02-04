from operator import itemgetter

def createInterval(start, finish, keys, key):
    new_interval = {}
    new_interval["start"] = start
    new_interval["finish"] = finish
    new_interval[key] = keys.copy()
    return new_interval


def getMaxListIntervals(min_start, max_list, key):
    intervals = []
    max_list = sorted(max_list, key=lambda x: x["point"])
    for i, end in enumerate(max_list):
        if i == 0 or min_start["point"] == end["point"]:
            if len(max_list) == 1:
                intervals.append(createInterval(min_start["point"], end["point"], end["keys"], key))
            min_start["keys"] = min_start["keys"].union(end["keys"])
            continue

        keys = set()
        if min_start["label"] == "start":
            keys = min_start["keys"].union(intervals[-1][key]) if len(intervals) > 0 else min_start["keys"]
        elif end["label"] == "finish":
            if i + 1 < len(max_list):
                if max_list[i+1]["label"] == "start" and intervals:
                    keys = intervals[-1][key].difference(max_list[i-1]["keys"])
                else:
                    keys = end["keys"].union(max_list[i+1]["keys"])
            else:
                keys = end["keys"]
        else:
            keys = intervals[-1][key].difference(min_start["keys"]).difference(end["keys"])

        intervals.append(createInterval(min_start["point"], end["point"], keys, key))
        min_start = end
    return intervals


def mergeSameIntervals(intervals, key):
    new_intervals = []
    last_interval = intervals[0]
    for interval in intervals[1:]:
        if (last_interval["start"], last_interval["finish"]) == (interval["start"], interval["finish"]):
            last_interval[key] = last_interval[key].union(interval[key])
        else:
            new_intervals.append(last_interval)
            last_interval = interval
    if not new_intervals or new_intervals[-1] != last_interval:
        new_intervals.append(last_interval)
    return new_intervals


def create_vertex(interval, label, key):
    vertex = {"point": interval[label], "keys": interval[key], "label": label}
    return vertex


def getMainPermutations(intervals, key):
    conflicts = False
    new_intervals = []
    intervals = sorted(intervals, key=itemgetter("start", "finish"))
    intervals = mergeSameIntervals(intervals, key)
    
    min_start = create_vertex(intervals[0], "start", key)
    max_end = intervals[0]["finish"]
    max_list = [create_vertex(intervals[0], "start", key), create_vertex(intervals[0], "finish", key)]
    for interval in intervals[1:]:
        if min_start["point"] < interval["start"] < max_end:
            max_list.append(create_vertex(interval, "start", key))
            max_list.append(create_vertex(interval, "finish", key))
            max_end = max(max_end, interval["finish"])
        elif min_start["point"] < interval["finish"] < max_end:
            max_list.append(create_vertex(interval, "finish", key))
        elif min_start["point"] == interval["start"] and interval["finish"] > max_end:
            min_start["keys"] = min_start["keys"].union(interval[key])
            max_list.append(create_vertex(interval, "finish", key))
            max_end = interval["finish"]
        
        if interval["start"] >= max_end:
            new_intervals += getMaxListIntervals(min_start, max_list, key)
            min_start = create_vertex(interval, "start", key)
            max_list = [create_vertex(interval, "finish", key)]
    new_intervals += getMaxListIntervals(min_start, max_list, key)

    return conflicts, new_intervals


def resolveConflicts(intervals, key):
    resolved_intervals = []
    current_interval = intervals[0]
    for interval in intervals[1:]:
        if interval["start"] > current_interval["start"]:
            resolved_intervals.append(current_interval)
            current_interval = interval
        else:
            current_interval[key] = current_interval[key].union(interval[key])
    resolved_intervals.append(current_interval)
    return resolved_intervals


class Merge:
    @staticmethod
    def union(intervals: list, key: str = "set_items"):
        conflict, intervals = getMainPermutations(intervals, key)
        if conflict:
            intervals = sorted(intervals, key=itemgetter("start", "finish"))
            intervals = resolveConflicts(intervals, key)
        return intervals