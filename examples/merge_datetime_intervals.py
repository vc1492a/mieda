import datetime
from mieda.intervals import Merge

intervals = [
    {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
     "set_items": {"1"}},
    {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
     "set_items": {"2"}},
    {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
     "set_items": {"3"}}
]


output = Merge.union(intervals=intervals)

print("\n --- merged intervals ---")
for i in output:
    print(i)

