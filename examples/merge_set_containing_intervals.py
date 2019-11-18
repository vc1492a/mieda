import datetime
from mieda.intervals import Merge

intervals = [
    {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
     "set_items": {"1"}},
    {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 3, 1, 0, 0),
     "set_items": {"2"}}
]

print(Merge.union(intervals=intervals))

