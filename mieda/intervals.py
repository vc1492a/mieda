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
from typing import Tuple
import warnings


class Merge:

    @staticmethod
    def check_input_interval_set_type(interval_set) -> Tuple[bool, set]:
        """
        Checks to see if the set is the interval is the correct format. If not, attempts to convert the indicated set.
        :return: a boolean indicating whether the test has passed and a set if the input could be converted.
        """
        passed = True
        if isinstance(interval_set, list):
            interval_set = set(interval_set)
            passed = False

        return passed, interval_set

    @staticmethod
    def union(intervals: list, key: str = "set_items") -> list:

        """
        Utilizes a directed graph to merge intervals according to unions in 'key' and update adjacent
        intervals to their new time ranges. If 2 comes before 3, then the intervals [1,3], [2,3] become [1], [2,3], [3].
        :param intervals: a list of dictionaries containing the fields 'start', 'finish', 'key', and
        'group' which describe each interval.
        :param key: a string which identifies the key to use when merging intervals based on the sets contained in the
        intervals. Default value is 'set_items'.
        :return: a list of aggregated intervals (NetworkX edge objects).
        """

        # check to see if the sets in the interval indicated is the proper format
        converted = False
        for i in intervals:
            status, interval_set = Merge.check_input_interval_set_type(i[key])
            if status is False:
                converted = True
            i[key] = interval_set
        if converted is True:
            warnings.warn("The correct input format is a set - converted lists to sets.")

        # first, merge together any intervals that span the same range (e.g. start and end indices)
        # the directed-graph algorithm is not intended to solve this use case which often comes up in practice
        interval_pairs = combinations(intervals, 2)
        for ip in interval_pairs:

            # if the start and end times are the same
            if (ip[0]["start"] == ip[1]["start"]) & (ip[0]["finish"] == ip[1]["finish"]):
                # merge them into a single interval
                interval_new = ip[0]
                interval_new[key] = interval_new[key].union(ip[1][key])

                # remove the old intervals from the input list (removes first matching value)
                intervals.remove(ip[0])
                intervals.remove(ip[1])

                # add the new interval
                intervals.append(interval_new)

        # create a directed Graph
        graph = nx.DiGraph()

        # sort the intervals by their start time to ensure a directional scan
        intervals = sorted(intervals, key=itemgetter('start'))

        # start by adding the start and ends of the first interval as nodes
        graph.add_node(intervals[0]["start"])
        graph.add_node(intervals[0]["finish"])

        # add an edge between the nodes
        graph.add_edge(
            **{"u_of_edge": intervals[0]["start"], "v_of_edge": intervals[0]["finish"], key: intervals[0][key]}
        )

        # add an edge between the nodes with its respective key and 'group' as attributes
        for i in range(0, len(intervals)):

            # get the current pairs of nodes or edges
            # since we are going through in a sorted fashion, we do not need to scan through all pairs
            # if we have sorted pairs, we only need to check most recent interval
            # this is an improvement over the previous approach which scanned through all pairs
            pairs = sorted(graph.edges(data=True), key=lambda x: x[0])

            # check if the new interval starts in between another edges start and end
            # if it is, bisect the interval, create a shared interval and adjust the old ones

            # since we sort the edges by the start interval,
            for p in range(len(pairs)):

                # if the start time falls between the pair
                if pairs[p][0] < intervals[i]["start"] < pairs[p][1]:

                    # check to see if the interval ends before the considered pair
                    # if so, pair start to interval start, interval start to interval end, and interval end to pair end
                    if intervals[i]["finish"] < pairs[p][1]:
                        # gather the adjacent attributes
                        left_attrs = set(graph[pairs[p][0]][pairs[p][1]][key])
                        right_attrs = set(intervals[i][key]).union(left_attrs)

                        # add edges
                        graph.add_edge(
                            **{"u_of_edge": pairs[p][0], "v_of_edge": intervals[i]["start"], key: left_attrs})
                        graph.add_edge(**{"u_of_edge": intervals[i]["start"], "v_of_edge": intervals[i]["finish"],
                                          key: right_attrs})
                        graph.add_edge(**{"u_of_edge": intervals[i]["finish"], "v_of_edge": pairs[p][1],
                                          key: graph[pairs[p][0]][pairs[p][1]][key]})

                        # remove the old edge
                        graph.remove_edge(pairs[p][0], pairs[p][1])

                        break

                    # check if the interval ends outside of the previous one
                    if pairs[p][1] <= intervals[i]["finish"]:

                        # first make an alteration based on the start
                        left_attrs = set(graph[pairs[p][0]][pairs[p][1]][key])
                        right_attrs = set(graph[pairs[p][0]][pairs[p][1]][key]).union(
                            intervals[i][key])

                        # add edges
                        graph.add_edge(
                            **{"u_of_edge": pairs[p][0], "v_of_edge": intervals[i]["start"], key: left_attrs})
                        graph.add_edge(
                            **{"u_of_edge": intervals[i]["start"], "v_of_edge": pairs[p][1], key: right_attrs})

                        if pairs[p][1] < intervals[i]["finish"]:
                            graph.add_edge(**{"u_of_edge": pairs[p][1], "v_of_edge": intervals[i]["finish"],
                                              key: intervals[i][key]})

                        # remove the old edge
                        graph.remove_edge(pairs[p][0], pairs[p][1])

                        break

                # if they start at the same time
                if pairs[p][0] == intervals[i]["start"]:

                    # if the current interval ends before
                    if intervals[i]["finish"] < pairs[p][1]:
                        # gather the adjacent attributes
                        left_attrs = set(graph[pairs[p][0]][pairs[p][1]][key]).union(
                            intervals[i][key])
                        right_attrs = graph[pairs[p][0]][pairs[p][1]][key]

                        # add edges
                        graph.add_edge(
                            **{"u_of_edge": pairs[p][0], "v_of_edge": intervals[i]["finish"], key: left_attrs})
                        graph.add_edge(
                            **{"u_of_edge": intervals[i]["finish"], "v_of_edge": pairs[p][1], key: right_attrs})

                        # remove the old edge
                        graph.remove_edge(pairs[p][0], pairs[p][1])

                        break

                    # if they start at the same time but the current interval ends after
                    if pairs[p][1] < intervals[i]["finish"]:
                        # gather the adjacent attributes
                        graph[pairs[p][0]][pairs[p][1]][key] = graph[pairs[p][0]][pairs[p][1]][key].union(
                            intervals[i][key])

                        # add edges
                        graph.add_edge(
                            **{"u_of_edge": pairs[p][1], "v_of_edge": intervals[i]["finish"], key: intervals[i][key]})

                # if the current interval starts before - this comes up only due to adding new pairs prior to resorting
                # in the next for loop
                if intervals[i]["start"] < pairs[p][0]:

                    # if it ends before
                    if intervals[i]["finish"] < pairs[p][1]:
                        # gather the adjacent attributes
                        left_attrs = set(graph[pairs[p][0]][pairs[p][1]][key]).union(
                            intervals[i][key])
                        right_attrs = graph[pairs[p][0]][pairs[p][1]][key]

                        # add edges
                        graph.add_edge(
                            **{"u_of_edge": pairs[p][0], "v_of_edge": intervals[i]["finish"], key: left_attrs})
                        graph.add_edge(
                            **{"u_of_edge": intervals[i]["finish"], "v_of_edge": pairs[p][1], key: right_attrs})

                        # remove the old edge
                        graph.remove_edge(pairs[p][0], pairs[p][1])

                        break

                    # if it ends after
                    if pairs[p][1] < intervals[i]["finish"]:
                        # gather the adjacent attributes
                        left_attrs = set(graph[pairs[p][0]][pairs[p][1]][key]).union(
                            intervals[i][key])
                        right_attrs = intervals[i][key]

                        # add edges
                        graph[pairs[p][0]][pairs[p][1]][key] = left_attrs
                        graph.add_edge(
                            **{"u_of_edge": pairs[p][1], "v_of_edge": intervals[i]["finish"], key: right_attrs})

                        # remove the old edge
                        graph.remove_edge(pairs[p][0], intervals[i]["finish"])

                        break

        # return the new sorted intervals
        graph_edges = sorted(graph.edges(data=True), key=lambda x: x[0])
        intervals = list()
        for e in graph_edges:
            intervals.append(
                {"start": e[0], "finish": e[1], key: e[2][key]}
            )

        return intervals
