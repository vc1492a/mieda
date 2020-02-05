import random
import datetime

class IntervalGenerator:
    def __init__(self, interval_type="int"):
        self.interval_type = interval_type
    

    def cast_value(self, value, interval_type):
        if interval_type in ["int", "float", "number"]:
            return eval(f"{interval_type}({value})")
        elif interval_type == "datetime":
            return datetime.datetime(1, 1, 1, 0) + datetime.timedelta(days=value)
        elif interval_type in ["char", "str"]:
            return chr(ord("a") + value)


    def generate_random(self, count: int = 1, min_value: int = 0, max_value: int = 100, interval_type=None, seed=None):
        interval_type = interval_type if interval_type else self.interval_type

        intervals = []
        for i in range(count):
            interval = {}
            random.seed(seed + i if seed is not None else seed)
            start = random.randint(min_value, max_value - 1)
            interval["start"] = self.cast_value(start, interval_type)
            interval["finish"] = self.cast_value(random.randint(start + 1, max_value), interval_type)
            interval["set_items"] = {i}
            intervals.append(interval)

        return intervals

    def generate_sequential(self, count: int = 1, start: int = 0, interval_type=None):
        interval_type = interval_type if interval_type else self.interval_type

        intervals = []
        for i in range(count):
            interval = {}
            interval["start"] = self.cast_value(start + i, interval_type)
            interval["finish"] = self.cast_value(start + i + 2, interval_type)
            interval["set_items"] = {i}
            intervals.append(interval)
        
        return intervals


if __name__ == "__main__":
    interval_gen = IntervalGenerator()

    import time

    from copy_mieda.intervals import Merge as mieda_merge
    from interval_balancing import Merge as interval_balancing

    algorithms = {"mieda": mieda_merge, "interval_balancing": interval_balancing}
    
    total_intervals = [interval_gen.generate_sequential(i, i) for i in range(1,1000,10)]

    for algorithm_name, algorithm in algorithms.items():
        avg_time = None
        start_time = time.process_time()
        for intervals in total_intervals:
            single_start = time.process_time()
            test = algorithm.union(intervals)
            elapsed = time.process_time() - single_start
            avg_time = (elapsed + avg_time)/2 if avg_time else elapsed
        print(f"Elapsed for {algorithm_name}:", time.process_time() - start_time)
        print("Average Time/Set:", avg_time)