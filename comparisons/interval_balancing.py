from operator import itemgetter


def create_interval(start, finish, keys, key):
    """Returns a properly formed interval dictionary object."""
    new_interval = {"start": start, "finish": finish}
    new_interval[key] = keys
    return new_interval


def reconstruct_intervals_from_vertices(vtx_list, key):
    """Takes a list of vertices from deconstructed, potentially conflicting intervals and returns a list of deconflicted intervals."""
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


def create_vertex(interval, label, key):
    vertex = {"point": interval[label], "keys": interval[key], "label": label}
    return vertex


class Merge:
    @staticmethod
    def union(intervals: list, key: str = "set_items"):
        """Combines a list of potentially conflicting intervals into a list of de-conflicted intervals with joined labels."""
        vtx_list = []
        for i, interval in enumerate(intervals):
            interval[key] = interval[key] if key in interval else {i}
            vtx_list.append(create_vertex(interval, "start", key))
            vtx_list.append(create_vertex(interval, "finish", key))
        
        return reconstruct_intervals_from_vertices(vtx_list, key) if vtx_list else []