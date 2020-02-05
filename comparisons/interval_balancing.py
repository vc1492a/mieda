from operator import itemgetter


def create_interval(start, finish, keys, key):
    new_interval = {"start": start, "finish": finish}
    new_interval[key] = keys
    return new_interval


def get_max_list_intervals(max_list, key):
    max_list = sorted(max_list, key=lambda x: x["point"])
    intervals = []
    open_ints = set()
    last_interval = max_list[0]
    for interval in max_list:
        if open_ints and last_interval["point"] != interval["point"]:
            intervals.append(create_interval(last_interval["point"], interval["point"], open_ints, key))
        open_ints = open_ints.union(interval["keys"]) if interval["label"] == "start" else open_ints.difference(interval["keys"])
        last_interval = interval
    return intervals


def create_vertex(interval, label, key):
    vertex = {"point": interval[label], "keys": interval[key], "label": label}
    return vertex


class Merge:
    @staticmethod
    def union(intervals: list, key: str = "set_items"):
        max_list = []
        for interval in intervals:
            max_list.append(create_vertex(interval, "start", key))
            max_list.append(create_vertex(interval, "finish", key))
        
        return get_max_list_intervals(max_list, key) if max_list else []