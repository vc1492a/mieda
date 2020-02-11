"""
========================================================================================================
Copyright 2020, by the California Institute of Technology. ALL RIGHTS RESERVED.
United States Government Sponsorship acknowledged. Any commercial use must be negotiated with the Office of Technology
Transfer at the California Institute of Technology. This software may be subject to U.S. export control laws. By
accepting this software, the user agrees to comply with all applicable U.S. export laws and regulations. User has the
responsibility to obtain export licenses, or other export authority as may be required before exporting such
information to foreign countries or providing access to foreign persons.
========================================================================================================
"""

from itertools import combinations
import networkx as nx
from operator import itemgetter
from typing import Tuple, Union
import warnings

from . import helpers


class Merge:
    warn = True

    @staticmethod
    def check_input_interval_set_type(interval_set: Union[list, set]) -> Tuple[bool, set]:
        """
        Checks to see if the set is the interval is the correct format. If not, attempts to convert the indicated set.
        :param interval_set: an interval which is checked for proper formatting as a set.
        :return: a boolean indicating whether the test has passed and a set if the input could be converted.
        """

        passed = isinstance(interval_set, set)
        if not passed:
            interval_set = set(interval_set) if isinstance(interval_set, list) else set(list(str(interval_set)))
            passed = False

        return passed, interval_set

    @staticmethod
    def validate_intervals(intervals: list, key: str) -> list:
        """
        Ensures passed intervals are properly formed and warns if not.
        :param intervals: a list of dictionaries containing the fields 'start', 'finish', 'key', and
        'group' which describe each interval.
        :param key: a string which identifies the key to use when merging intervals based on the sets contained in the
        intervals.
        :return: a list of intervals, some of which may be converted to the proper format.
        """

        converted = False
        for i, interval in enumerate(intervals): 
            interval[key] = interval[key] if key in interval else set(list(i))
            correct_type, interval_set = Merge.check_input_interval_set_type(interval[key])
            converted = True if not correct_type else converted
            interval[key] = interval_set
        if Merge.warn and converted:
            warnings.warn("The correct input format is a set - converted lists to sets.")

        return intervals

    @staticmethod
    def merge_same_intervals(intervals: list, key: str) -> list:
        """
        Combines all identical intervals into one.
        :param intervals: a list of dictionaries containing the fields 'start', 'finish', 'key', and
        'group' which describe each interval.
        :param key: a string which identifies the key to use when merging intervals based on the sets contained in the
        intervals.
        :return: a list of aggregated intervals.
        """
        interval_pairs = combinations(intervals, 2)
        for ip in interval_pairs:
            # if the start and end times are the same
            if (ip[0]["start"] == ip[1]["start"]) and (ip[0]["finish"] == ip[1]["finish"]):
                # merge them into a single interval
                interval_new = ip[0].copy()
                interval_new[key] = ip[0][key].union(ip[1][key])

                # attempt to remove any old intervals if they still exist in the data
                try:
                    intervals.remove(ip[0])
                except ValueError:
                    pass

                try:
                    intervals.remove(ip[1])
                except ValueError:
                    pass

                # append the new, merged interval
                intervals.append(interval_new)
        return intervals

    @staticmethod
    def union(intervals: list, key: str = "set_items", return_graph: bool = False) -> Union[list, nx.DiGraph]:
        """
        Utilizes a directed graph to merge intervals according to unions in 'key' and update adjacent
        intervals to their new time ranges. If 2 comes before 3, then the intervals [1,3], [2,3] become [1], [2,3], [3].
        :param intervals: a list of dictionaries containing the fields 'start', 'finish', 'key', and
        'group' which describe each interval.
        :param key: (optional) a string which identifies the key to use when merging intervals based on the sets contained in the
        intervals. Default value is 'set_items'.
        :param return_graph: (optional) when True, returns a NetworkX directed graph object instead of a list of intervals.
        :return: a list of aggregated intervals (NetworkX edge objects).
        """

        # check to see if the sets in the interval indicated is the proper format
        intervals = Merge.validate_intervals(intervals, key)

        # first, merge together any intervals that span the same range (e.g. start and end indices)
        # the directed-graph algorithm is not intended to solve this use case which often comes up in practice
        intervals = Merge.merge_same_intervals(intervals, key)

        # sort the intervals by their start time to ensure a directional scan
        intervals = sorted(intervals, key=itemgetter('start'))

        # create a directed Graph from intervals
        graph = helpers.create_directed_graph(intervals, key)

        # add an edge between the nodes with its respective key and 'group' as attributes
        for _, interval in enumerate(intervals):

            # get the current pairs of nodes or edges
            # since we are going through in a sorted fashion, we do not need to scan through all pairs
            # if we have sorted pairs, we only need to check most recent interval
            # this is an improvement over the previous approach which scanned through all pairs
            pairs = sorted(graph.edges(data=True), key=lambda x: x[0])[-2:]

            # check if the new interval starts in between another edges start and end
            # if it is, bisect the interval, create a shared interval and adjust the old ones
            interval_split = False

            # iterate through the pairs
            for _, pair in enumerate(pairs):

                # if the start time falls between the pair
                if pair[0] < interval["start"] < pair[1]:
                    interval_split = True

                    # check to see if the interval ends before the considered pair
                    # if so, pair start to interval start, interval start to interval end, and interval end to pair end
                    if interval["finish"] < pair[1]:
                        graph = helpers.interval_starts_in_ends_before(graph, pair, interval, key)
                        break

                    # check if the interval ends outside of the previous one
                    if pair[1] <= interval["finish"]:
                        graph = helpers.interval_starts_in_ends_after(graph, pair, interval, key)

                # if they start at the same time
                elif pair[0] == interval["start"]:
                    interval_split, graph = helpers.interval_starts_together(graph, pair, interval, key)

                # if the current interval starts before - this comes up only due to adding new pairs prior to resorting
                # in the next for loop
                if interval["start"] < pair[0]:
                    interval_split, graph = helpers.interval_starts_before(graph, pair, interval, key)
                    
            # if the interval wasn't split or processed, it still needs to be included in the graph
            if not interval_split:
                graph.add_edge(**{"u_of_edge": interval["start"], "v_of_edge": interval["finish"],
                                key: interval[key]})

        # return the new sorted intervals
        if return_graph is True:
            return graph
        else:
            graph_edges = sorted(graph.edges(data=True), key=lambda x: x[0])
            intervals = list()
            for e in graph_edges:
                intervals.append(
                    {"start": e[0], "finish": e[1], key: e[2][key]}
                )

            return intervals
