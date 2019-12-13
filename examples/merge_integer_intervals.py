from mieda.intervals import Merge

intervals = [
    {"start": 1, "finish": 4, "set_items": {"1"}},
    {"start": 2, "finish": 6, "set_items": {"2"}},
    {"start": 2, "finish": 6, "set_items": {"3"}}
]

output = Merge.union(intervals=intervals)

print("\n --- merged intervals ---")
for i in output:
    print(i)

