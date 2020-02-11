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


import networkx as nx
from typing import Tuple


def create_directed_graph(intervals: list, key: str) -> nx.DiGraph:
    """
    Takes a list of intervals as an input and constructs a directed graph, using
    only the first item in the list of intervals.
    :param intervals: a list of dictionaries containing the fields 'start', 'finish', 'key', and
    'group' which describe each interval.
    :param key: a string which identifies the key to use when merging intervals based on the sets contained in the
    intervals.
    :return: a nx.DiGraph directed-graph, with the initial item in the list of intervals contained therein.
    """
    # create a directed Graph
    graph = nx.DiGraph()

    # start by adding the start and ends of the first interval as nodes
    graph.add_node(intervals[0]["start"])
    graph.add_node(intervals[0]["finish"])

    # add an edge between the nodes
    graph.add_edge(
        **{"u_of_edge": intervals[0]["start"], "v_of_edge": intervals[0]["finish"], key: intervals[0][key]}
    )
    return graph


def interval_starts_in_ends_before(graph: nx.DiGraph, pair, interval: dict, key: str) -> nx.DiGraph:
    """
    Checks to see whether the interval starts in and ends before and splits the interval appropriately
    and updates the graph.
    :param graph: a ni.DiGraph object.
    :param pair: a pair of ids which are used to lookup an adjacent interval in the directed-graph.
    :param interval: the interval to be compared to the input pair.
    :param key: a string which identifies the key to use when merging intervals based on the sets contained in the
    intervals.
    :return: a nx.DiGraph directed-graph updated as a result of the merge.
    """

    # gather the adjacent attributes
    left_attrs = set(graph[pair[0]][pair[1]][key])
    right_attrs = set(interval[key]).union(left_attrs)

    # add edges
    graph.add_edge(**{"u_of_edge": pair[0], "v_of_edge": interval["start"], key: left_attrs})
    graph.add_edge(**{"u_of_edge": interval["start"], "v_of_edge": interval["finish"], key: right_attrs})
    graph.add_edge(**{"u_of_edge": interval["finish"], "v_of_edge": pair[1], key: graph[pair[0]][pair[1]][key]})

    # remove the old edge
    graph.remove_edge(pair[0], pair[1])

    return graph


def interval_starts_in_ends_after(graph: nx.DiGraph, pair, interval: dict, key: str) -> nx.DiGraph:
    """
    Checks to see whether the interval starts in and ends after and splits the interval appropriately
    and updates the graph.
    :param graph: a ni.DiGraph object.
    :param pair: a pair of ids which are used to lookup an adjacent interval in the directed-graph.
    :param interval: the interval to be compared to the input pair.
    :param key: a string which identifies the key to use when merging intervals based on the sets contained in the
    intervals.
    :return: a nx.DiGraph directed-graph updated as a result of the merge.
    """

    # first make an alteration based on the start
    left_attrs = set(graph[pair[0]][pair[1]][key])
    right_attrs = set(graph[pair[0]][pair[1]][key]).union(interval[key])

    # add edges
    graph.add_edge(**{"u_of_edge": pair[0], "v_of_edge": interval["start"], key: left_attrs})
    graph.add_edge(**{"u_of_edge": interval["start"], "v_of_edge": pair[1], key: right_attrs})

    if pair[1] < interval["finish"]:
        graph.add_edge(**{"u_of_edge": pair[1], "v_of_edge": interval["finish"], key: interval[key]})

    # remove the old edge
    graph.remove_edge(pair[0], pair[1])

    return graph


def interval_ends_before(graph: nx.DiGraph, pair, interval: dict, key: str) -> nx.DiGraph:
    """
    Checks to see whether the interval starts ends before and splits the interval appropriately
    and updates the graph.
    :param graph: a ni.DiGraph object.
    :param pair: a pair of ids which are used to lookup an adjacent interval in the directed-graph.
    :param interval: the interval to be compared to the input pair.
    :param key: a string which identifies the key to use when merging intervals based on the sets contained in the
    intervals.
    :return: a nx.DiGraph directed-graph updated as a result of the merge.
    """

    # gather the adjacent attributes
    left_attrs = set(graph[pair[0]][pair[1]][key]).union(interval[key])
    right_attrs = graph[pair[0]][pair[1]][key]

    # add edges
    graph.add_edge(**{"u_of_edge": pair[0], "v_of_edge": interval["finish"], key: left_attrs})
    graph.add_edge(**{"u_of_edge": interval["finish"], "v_of_edge": pair[1], key: right_attrs})

    # remove the old edge
    graph.remove_edge(pair[0], pair[1])

    return graph


def interval_starts_together(graph: nx.DiGraph, pair, interval: dict, key: str) -> Tuple[bool, nx.DiGraph]:
    """
    Checks to see whether the interval starts together and splits the interval appropriately
    and updates the graph.
    :param graph: a ni.DiGraph object.
    :param pair: a pair of ids which are used to lookup an adjacent interval in the directed-graph.
    :param interval: the interval to be compared to the input pair.
    :param key: a string which identifies the key to use when merging intervals based on the sets contained in the
    intervals.
    :return: a nx.DiGraph directed-graph updated as a result of the merge.
    """

    interval_split = False
    # if the current interval ends before
    if interval["finish"] < pair[1]:
        graph = interval_ends_before(graph, pair, interval, key)
        interval_split = True

    # if they start at the same time but the current interval ends after
    if pair[1] < interval["finish"]:
        # gather the adjacent attributes
        graph[pair[0]][pair[1]][key] = graph[pair[0]][pair[1]][key].union(
            interval[key])

        # add edges
        graph.add_edge(
            **{"u_of_edge": pair[1], "v_of_edge": interval["finish"], key: interval[key]})

        interval_split = True

    return interval_split, graph


def interval_starts_before(graph: nx.DiGraph, pair, interval: dict, key: str) -> Tuple[bool, nx.DiGraph]:
    """
    Checks to see whether the interval starts before and splits the interval appropriately
    and updates the graph.
    :param graph: a ni.DiGraph object.
    :param pair: a pair of ids which are used to lookup an adjacent interval in the directed-graph.
    :param interval: the interval to be compared to the input pair.
    :param key: a string which identifies the key to use when merging intervals based on the sets contained in the
    intervals.
    :return: a nx.DiGraph directed-graph updated as a result of the merge.
    """

    interval_split = False
    # if it ends before
    if interval["finish"] < pair[1]:
        # gather the adjacent attributes
        left_attrs = set(graph[pair[0]][pair[1]][key]).union(
            interval[key])
        right_attrs = graph[pair[0]][pair[1]][key]

        # add edges
        graph.add_edge(
            **{"u_of_edge": pair[0], "v_of_edge": interval["finish"], key: left_attrs})
        graph.add_edge(
            **{"u_of_edge": interval["finish"], "v_of_edge": pair[1], key: right_attrs})

        # remove the old edge
        graph.remove_edge(pair[0], pair[1])

        interval_split = True

    # if it ends after
    if pair[1] < interval["finish"]:
        # gather the adjacent attributes
        left_attrs = set(graph[pair[0]][pair[1]][key]).union(
            interval[key])
        right_attrs = interval[key]

        # add edges
        graph[pair[0]][pair[1]][key] = left_attrs
        graph.add_edge(
            **{"u_of_edge": pair[1], "v_of_edge": interval["finish"], key: right_attrs})

        # remove the old edge
        try:
            graph.remove_edge(pair[0], interval["finish"])
        except nx.NetworkXException:
            pass

        interval_split = True

    return interval_split, graph
