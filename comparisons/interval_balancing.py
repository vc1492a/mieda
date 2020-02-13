import datetime
from typing import Union


def create_interval(start: Union[str, int, float, 'datetime.datetime'], finish: Union[str, int, float, 'datetime.datetime'], keys: dict, key: Union[str, int, float, 'datetime.datetime']) -> dict:
    """
    Takes a set of data pertaining to an interval and creates a properly formed interval dictionary object.
    :param start: A string, integer, float, or datetime object indicating the start of an interval.
    :param finish:  A string, integer, float, or datetime object indicating the finish of an interval.
    :param keys: A set of keys for the interval, usually indicating its source.
    :param key:  A string, integer, float, or datetime object to use as the key for the interval.
    :return: a properly formed interval dictionary object.
    """

    new_interval = dict({"start": start, "finish": finish})
    new_interval[key] = keys
    return new_interval


def reconstruct_intervals_from_vertices(vtx_list: list, key: Union[str, int, float, 'datetime.datetime']) -> list:
    """
    Takes a list of vertices from deconstructed, potentially conflicting intervals and returns a list of deconflicted
    intervals.
    :param vtx_list: A list of vertices from deconstructed, potentially conflicting intervals.
    :param key: A string, integer, float, or datetime object to use as the key for the intervals.
    :return: A list of deconflicted intervals.
    """

    vtx_list = sorted(vtx_list, key=lambda x: x["point"])
    intervals = []
    open_ints = set()
    last_vertex = vtx_list[0]
    for vertex in vtx_list:
        if open_ints and last_vertex["point"] != vertex["point"]:
            intervals.append(create_interval(last_vertex["point"], vertex["point"], open_ints, key))
        open_ints = open_ints.union(vertex["keys"]) if vertex["label"] == "start" else open_ints.difference(vertex["keys"])
        last_vertex = vertex
    return intervals


def create_vertex(interval: list, label: Union[str, int, float, 'datetime.datetime'], key: Union[str, int, float, 'datetime.datetime']) -> dict:
    """
    Creates a vertex for an interval with information about the point, label, and keys for the interval.
    :param interval: The interval in which to create a vertex for.
    :param label: A string, integer, float, or datetime object used to indicate which label to use for the point.
    :param key: A string, integer, float, or datetime object to use as the key for the interval.
    :return: A dictionary representing the vertex for the provided interval.
    """

    vertex = dict({"point": interval[label], "keys": interval[key], "label": label})
    return vertex


class Merge:

    @staticmethod
    def union(intervals: list, key: str = "set_items"):
        """
        Combines a list of potentially conflicting intervals into a list of de-conflicted intervals with joined labels
        :param intervals: A list of intervals.
        :param key: A string to use as the key for the interval.
        :return: A set of merged intervals.
        """

        vtx_list = []
        for i, interval in enumerate(intervals):
            interval[key] = interval[key] if key in interval else {i}
            vtx_list.append(create_vertex(interval, "start", key))
            vtx_list.append(create_vertex(interval, "finish", key))
        
        return reconstruct_intervals_from_vertices(vtx_list, key) if vtx_list else []