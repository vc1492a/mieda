import datetime
from mieda.intervals import Merge

intervals = [
    {"start": "A", "finish": "D", "set_items": {"1"}},
    {"start": "B", "finish": "E", "set_items": {"2"}},
    {"start": "B", "finish": "E", "set_items": {"3"}}
]


output = Merge.union(intervals=intervals)

print("\n --- merged intervals ---")
for i in output:
    print(i)

