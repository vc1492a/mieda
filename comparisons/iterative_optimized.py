from operator import itemgetter

def mergeDuplicates(new_intervals, key):
    for interval in new_intervals:
        for i, compare_interval in enumerate(new_intervals):
            if interval is compare_interval:
                continue

            if interval["start"] == compare_interval["start"] and interval["finish"] == compare_interval["finish"]:
                interval[key] = interval[key].union(compare_interval[key])
                del new_intervals[i]
    return new_intervals


def startIntervalIsInBetween(start_interval, end_interval, new_intervals, key):
    if start_interval["start"] != end_interval["start"]:
        new_intervals.append(
            dict(zip(("start", "finish", key), 
            (end_interval["start"], start_interval["start"], 
            end_interval[key])))
        )

    if start_interval["finish"] < end_interval["finish"]:
        new_intervals += [
            dict(zip(("start", "finish", key), 
            (start_interval["start"], start_interval["finish"], 
            {start_interval[key]}))),
            dict(zip(("start", "finish", key), 
            (start_interval["finish"], end_interval["finish"], 
            end_interval[key])))
        ]

    elif start_interval["finish"] == end_interval["finish"]:
        new_intervals.append(
            dict(zip(("start", "finish", key), 
            (start_interval["start"], end_interval["finish"], 
            start_interval[key].union(end_interval[key]))))
        )

    elif start_interval["finish"] > end_interval["finish"]:
        new_intervals += [
            dict(zip(("start", "finish", key), 
            (start_interval["start"], end_interval["finish"], 
            start_interval[key].union(end_interval[key])))),
            dict(zip(("start", "finish", key), 
            (end_interval["finish"], start_interval["finish"], 
            start_interval[key])))
        ]

    return new_intervals


class Merge:
    @staticmethod
    def union(intervals: list, key: str = "set_items"):
        new_intervals = []

        intervals = sorted(intervals, key=itemgetter('start'))

        for i, start_interval in enumerate(intervals):
            split_intervals = False
            for end_interval in intervals[i+1:]:
                if start_interval["start"] <= end_interval["start"] < start_interval["finish"]:
                    split_intervals = True
                    continue

                if end_interval["start"] <= start_interval["start"] < end_interval["finish"]:
                    split_intervals = True
                    new_intervals = startIntervalIsInBetween(start_interval, end_interval, new_intervals, key)

            if not split_intervals:
                new_intervals.append(start_interval)

        new_intervals = mergeDuplicates(new_intervals, key)

        return new_intervals