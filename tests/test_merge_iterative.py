# Authors: Valentino Constantinou <vconstan@jpl.caltech.edu>, Asitang Mishra <asitang.mishra@jpl.caltech.edu>
# License: Apache 2.0

from comparisons.iterative import Merge

import datetime
import pytest
from operator import itemgetter


# fixtures
@pytest.fixture()
def interval_inputs() -> list:
    """
    This fixture generates a set of all possible scenarios for consideration of one interval against another.
    :return: a list of intervals which contains all possible scenarios.
    """

    # create a list to store various interval types
    intervals = list()

    # B starts and ends after A
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"2"}}
        ]
    )

    # B starts after A but ends at the same time as A
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"2"}}
        ]
    )

    # B starts after A and ends before A
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 3, 1, 0, 0),
             "set_items": {"2"}}
        ]
    )

    # B starts at the same time as A and ends after A
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"2"}}
        ]
    )

    # B starts at the same time as A and ends before A
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 3, 1, 0, 0),
             "set_items": {"2"}}
        ]
    )

    # B starts at the same time as A and ends at the same time as A also
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"2"}}
        ]
    )

    # B starts wholly after A
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 5, 1, 0, 0), "finish": datetime.datetime(2020, 1, 7, 1, 0, 0),
             "set_items": {"2"}}
        ]
    )

    return intervals


@pytest.fixture()
def interval_outputs() -> list:
    """
    This fixture generates a set of correct outputs against the scenarios provided in the output of interval_inputs().
    :return: a list of intervals which contains the correct output for all possible scenarios.
    """

    # create a list to store the various outputs
    outputs = list()

    # B starts and ends after A
    outputs.append(
        [
            {'start': datetime.datetime(2020, 1, 1, 1, 0), 'finish': datetime.datetime(2020, 1, 2, 1, 0),
             'set_items': {'1'}},
            {'start': datetime.datetime(2020, 1, 2, 1, 0), 'finish': datetime.datetime(2020, 1, 4, 1, 0),
             'set_items': {'1', '2'}},
            {'start': datetime.datetime(2020, 1, 4, 1, 0), 'finish': datetime.datetime(2020, 1, 6, 1, 0),
             'set_items': {'2'}}
        ]
    )

    # B starts after A but ends at the same time as A
    outputs.append(
        [
            {'start': datetime.datetime(2020, 1, 1, 1, 0), 'finish': datetime.datetime(2020, 1, 2, 1, 0),
             'set_items': {'1'}},
            {'start': datetime.datetime(2020, 1, 2, 1, 0), 'finish': datetime.datetime(2020, 1, 4, 1, 0),
             'set_items': {'2', '1'}}
        ]
    )

    # B starts after A and ends before A
    outputs.append(
        [
            {'start': datetime.datetime(2020, 1, 1, 1, 0), 'finish': datetime.datetime(2020, 1, 2, 1, 0),
             'set_items': {'1'}},
            {'start': datetime.datetime(2020, 1, 2, 1, 0), 'finish': datetime.datetime(2020, 1, 3, 1, 0),
             'set_items': {'2', '1'}},
            {'start': datetime.datetime(2020, 1, 3, 1, 0), 'finish': datetime.datetime(2020, 1, 4, 1, 0),
             'set_items': {'1'}}
        ]
    )

    # B starts at the same time as A and ends after A
    outputs.append(
        [
            {'start': datetime.datetime(2020, 1, 1, 1, 0), 'finish': datetime.datetime(2020, 1, 4, 1, 0),
             'set_items': {'2', '1'}},
            {'start': datetime.datetime(2020, 1, 4, 1, 0), 'finish': datetime.datetime(2020, 1, 6, 1, 0),
             'set_items': {'2'}}
        ]
    )

    # B starts at the same time as A and ends before A
    outputs.append(
        [
            {'start': datetime.datetime(2020, 1, 1, 1, 0), 'finish': datetime.datetime(2020, 1, 3, 1, 0),
             'set_items': {'1', '2'}},
            {'start': datetime.datetime(2020, 1, 3, 1, 0), 'finish': datetime.datetime(2020, 1, 4, 1, 0),
             'set_items': {'1'}}
        ]
    )

    # B starts at the same time as A and ends at the same time as A also
    outputs.append(
        [
            {'start': datetime.datetime(2020, 1, 1, 1, 0), 'finish': datetime.datetime(2020, 1, 4, 1, 0),
             'set_items': {'2', '1'}}
        ]
    )

    # B starts wholly after A
    outputs.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 5, 1, 0, 0), "finish": datetime.datetime(2020, 1, 7, 1, 0, 0),
             "set_items": {"2"}}
        ]
    )

    return outputs


@pytest.fixture()
def complex_interval_inputs() -> list:
    """
    This fixture generates a set of complex scenarios for consideration of one interval against another.
    :return: a list of intervals which contains some more complex scenarios.
    """

    # create a list to store various interval types
    intervals = list()

    # B starts after A, C starts at the same time as B but ends before B
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"2"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 5, 1, 0, 0),
             "set_items": {"3"}},
        ]
    )

    # B starts after A, C starts at the same time as B but ends after
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"2"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 7, 1, 0, 0),
             "set_items": {"3"}}
        ]
    )

    # B starts after A, C starts at the same time as B and ends at the same time as B
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"2"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"3"}}
        ]
    )

    # B starts after A, C starts at the same time as B and ends at the same time as B, but A contains 2 items
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1", "A"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"2"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"3"}}
        ]
    )

    # B starts after A, but C starts at the same time as B and ends before. D starts at the end time of C and ends last.
    intervals.append(
         [
             {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
              "set_items": {"1"}},
             {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
              "set_items": {"2"}},
             {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 5, 1, 0, 0),
              "set_items": {"3"}},
             {"start": datetime.datetime(2020, 1, 5, 1, 0, 0), "finish": datetime.datetime(2020, 1, 8, 1, 0, 0),
              "set_items": {"4"}}
         ]
    )

    # B starts after A, but C starts at the same time as B and ends before. D starts at the end time of C and ends last.
    # now however there is a "dangling" interval in isolation
    intervals.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"2"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 5, 1, 0, 0),
             "set_items": {"3"}},
            {"start": datetime.datetime(2020, 1, 5, 1, 0, 0), "finish": datetime.datetime(2020, 1, 8, 1, 0, 0),
             "set_items": {"4"}},
            {"start": datetime.datetime(2020, 1, 11, 1, 0, 0), "finish": datetime.datetime(2020, 1, 12, 1, 0, 0),
             "set_items": {"5"}}
        ]
    )

    # test for the ability to handle more than one duplicate interval in the input data
    intervals.append(
        [
            {'start': 1477875126, 'finish': 1477920079, 'set_items': {'1'}},
            {'start': 1477875126, 'finish': 1477920079, 'set_items': {'1'}},
            {'start': 1477875126, 'finish': 1477920079, 'set_items': {'1'}},
            {'start': 1477901090, 'finish': 1477938541, 'set_items': {'2'}},
            {'start': 1477901090, 'finish': 1477938541, 'set_items': {'2'}},
            {'start': 1477901090, 'finish': 1477938541, 'set_items': {'2'}},
            {'start': 1477901090, 'finish': 1477938541, 'set_items': {'2'}},
            {'start': 1477901090, 'finish': 1477938541, 'set_items': {'2'}},
            {'start': 1477901090, 'finish': 1477938541, 'set_items': {'2'}},
            {'start': 1477901090, 'finish': 1477938541, 'set_items': {'2'}},
            {'start': 1477901090, 'finish': 1477938541, 'set_items': {'2'}},
            {'start': 1477915725, 'finish': 1477987473, 'set_items': {'3'}},
            {'start': 1477915725, 'finish': 1477987473, 'set_items': {'3'}},
            {'start': 1477915725, 'finish': 1477987473, 'set_items': {'3'}},
            {'start': 1477915725, 'finish': 1477987473, 'set_items': {'3'}},
            {'start': 1477939605, 'finish': 1477977748, 'set_items': {'4'}},
            {'start': 1477939605, 'finish': 1477977748, 'set_items': {'4'}},
            {'start': 1477961500, 'finish': 1478006402, 'set_items': {'5'}},
            {'start': 1477961500, 'finish': 1478006402, 'set_items': {'5'}},
            {'start': 1477961500, 'finish': 1478006402, 'set_items': {'5'}}
        ]
    )

    return intervals


@pytest.fixture()
def complex_interval_outputs() -> list:
    """
    This fixture generates a set of correct outputs against the scenarios provided in the output of
    complex_interval_inputs().
    :return: a list of intervals which contains the correct output for all scenarios in complex_interval_inputs().
    """

    # create a list to store the various outputs
    outputs = list()

    # B starts after A, C starts at the same time as B but ends before B
    outputs.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 2, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"3", "2", "1"}},
            {"start": datetime.datetime(2020, 1, 4, 1, 0, 0), "finish": datetime.datetime(2020, 1, 5, 1, 0, 0),
             "set_items": {"3", "2"}},
            {"start": datetime.datetime(2020, 1, 5, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"2"}}
        ]
    )

    # B starts after A, C starts at the same time as B but ends after
    outputs.append(
        [
            {'start': datetime.datetime(2020, 1, 1, 1, 0), 'finish': datetime.datetime(2020, 1, 2, 1, 0),
             'set_items': {'1'}},
            {'start': datetime.datetime(2020, 1, 2, 1, 0), 'finish': datetime.datetime(2020, 1, 4, 1, 0),
             'set_items': {'2', '1', '3'}},
            {'start': datetime.datetime(2020, 1, 4, 1, 0), 'finish': datetime.datetime(2020, 1, 6, 1, 0),
             'set_items': {'2', '3'}},
            {'start': datetime.datetime(2020, 1, 6, 1, 0), 'finish': datetime.datetime(2020, 1, 7, 1, 0),
             'set_items': {'3'}}
        ]
    )

    # B starts after A, C starts at the same time as B and ends at the same time as B
    outputs.append(
        [
            {'start': datetime.datetime(2020, 1, 1, 1, 0), 'finish': datetime.datetime(2020, 1, 2, 1, 0),
             'set_items': {'1'}},
            {'start': datetime.datetime(2020, 1, 2, 1, 0), 'finish': datetime.datetime(2020, 1, 4, 1, 0),
             'set_items': {'2', '1', '3'}},
            {'start': datetime.datetime(2020, 1, 4, 1, 0), 'finish': datetime.datetime(2020, 1, 6, 1, 0),
             'set_items': {'2', '3'}}
        ]
    )

    # B starts after A, C starts at the same time as B and ends at the same time as B, but A contains 2 items
    outputs.append(
        [
            {'start': datetime.datetime(2020, 1, 1, 1, 0), 'finish': datetime.datetime(2020, 1, 2, 1, 0),
             'set_items': {'1', 'A'}},
            {'start': datetime.datetime(2020, 1, 2, 1, 0), 'finish': datetime.datetime(2020, 1, 4, 1, 0),
             'set_items': {'2', '3', '1', 'A'}},
            {'start': datetime.datetime(2020, 1, 4, 1, 0), 'finish': datetime.datetime(2020, 1, 6, 1, 0),
             'set_items': {'2', '3'}}
        ]
    )

    # B starts after A, but C starts at the same time as B and ends before. D starts at the end time of C and ends last.
    outputs.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 2, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1", "2", "3"}},
            {"start": datetime.datetime(2020, 1, 4, 1, 0, 0), "finish": datetime.datetime(2020, 1, 5, 1, 0, 0),
             "set_items": {"2", "3"}},
            {"start": datetime.datetime(2020, 1, 5, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"2", "4"}},
            {"start": datetime.datetime(2020, 1, 6, 1, 0, 0), "finish": datetime.datetime(2020, 1, 8, 1, 0, 0),
             "set_items": {"4"}}
        ]
    )

    # B starts after A, but C starts at the same time as B and ends before. D starts at the end time of C and ends last.
    # now however there is a "dangling" interval in isolation
    outputs.append(
        [
            {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 2, 1, 0, 0),
             "set_items": {"1"}},
            {"start": datetime.datetime(2020, 1, 2, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
             "set_items": {"1", "2", "3"}},
            {"start": datetime.datetime(2020, 1, 4, 1, 0, 0), "finish": datetime.datetime(2020, 1, 5, 1, 0, 0),
             "set_items": {"2", "3"}},
            {"start": datetime.datetime(2020, 1, 5, 1, 0, 0), "finish": datetime.datetime(2020, 1, 6, 1, 0, 0),
             "set_items": {"2", "4"}},
            {"start": datetime.datetime(2020, 1, 6, 1, 0, 0), "finish": datetime.datetime(2020, 1, 8, 1, 0, 0),
             "set_items": {"4"}},
            {"start": datetime.datetime(2020, 1, 11, 1, 0, 0), "finish": datetime.datetime(2020, 1, 12, 1, 0, 0),
             "set_items": {"5"}}
        ]
    )

    # test for the ability to handle more than one duplicate interval in the input data
    outputs.append(
        [
            {'start': 1477875126, 'finish': 1477901090, 'set_items': {'1'}},
            {'start': 1477901090, 'finish': 1477915725, 'set_items': {'1', '2'}},
            {'start': 1477915725, 'finish': 1477920079, 'set_items': {'1', '2', '3'}},
            {'start': 1477920079, 'finish': 1477938541, 'set_items': {'2', '3'}},
            {'start': 1477938541, 'finish': 1477939605, 'set_items': {'3'}},
            {'start': 1477939605, 'finish': 1477961500, 'set_items': {'3', '4'}},
            {'start': 1477961500, 'finish': 1477977748, 'set_items': {'3', '4', '5'}},
            {'start': 1477977748, 'finish': 1477987473, 'set_items': {'3', '5'}},
            {'start': 1477987473, 'finish': 1478006402, 'set_items': {'5'}}
        ]
    )


    return outputs


@pytest.fixture()
def interval_inputs_integers() -> list:
    """
    This fixture generates a set of intervals with integers as indices.
    :return: a list of intervals to use for testing.
    """

    # create a list to store various interval types
    intervals = list()

    # B starts and ends after A
    intervals.append(
        [
            {"start": 1, "finish": 4, "set_items": {"1"}},
            {"start": 2, "finish": 6, "set_items": {"2"}}
        ]
    )

    # B starts after A but ends at the same time as A
    intervals.append(
        [
            {"start": 1, "finish": 4, "set_items": {"1"}},
            {"start": 2, "finish": 4, "set_items": {"2"}}
        ]
    )

    # B starts after A and ends before A
    intervals.append(
        [
            {"start": 1, "finish": 4, "set_items": {"1"}},
            {"start": 2, "finish": 3, "set_items": {"2"}}
        ]
    )

    return intervals


@pytest.fixture()
def interval_outputs_integers() -> list:
    """
    This fixture generates a set of correct outputs against intervals with integers as indices.
    :return: a list of intervals which contains the correct output for the integer-indexed intervals.
    """

    # create a list to store the various outputs
    outputs = list()

    # B starts and ends after A
    outputs.append(
        [
            {'start': 1, 'finish': 2, 'set_items': {'1'}},
            {'start': 2, 'finish': 4, 'set_items': {'1', '2'}},
            {'start': 4, 'finish': 6, 'set_items': {'2'}}
        ]
    )

    # B starts after A but ends at the same time as A
    outputs.append(
        [
            {'start': 1, 'finish': 2, 'set_items': {'1'}},
            {'start': 2, 'finish': 4, 'set_items': {'2', '1'}}
        ]
    )

    # B starts after A and ends before A
    outputs.append(
        [
            {'start': 1, 'finish': 2, 'set_items': {'1'}},
            {'start': 2, 'finish': 3, 'set_items': {'2', '1'}},
            {'start': 3, 'finish': 4, 'set_items': {'1'}}
        ]
    )

    return outputs


@pytest.fixture()
def interval_inputs_strings() -> list:
    """
    This fixture generates a set of intervals with strings as indices.
    :return: a list of intervals to use for testing.
    """

    # create a list to store various interval types
    intervals = list()

    # B starts and ends after A
    intervals.append(
        [
            {"start": "A", "finish": "D", "set_items": {"1"}},
            {"start": "B", "finish": "F", "set_items": {"2"}}
        ]
    )

    # B starts after A but ends at the same time as A
    intervals.append(
        [
            {"start": "A", "finish": "D", "set_items": {"1"}},
            {"start": "B", "finish": "D", "set_items": {"2"}}
        ]
    )

    # B starts after A and ends before A
    intervals.append(
        [
            {"start": "A", "finish": "D", "set_items": {"1"}},
            {"start": "B", "finish": "C", "set_items": {"2"}}
        ]
    )

    return intervals


@pytest.fixture()
def interval_outputs_strings() -> list:
    """
    This fixture generates a set of correct outputs against intervals with strings as indices.
    :return: a list of intervals which contains the correct output for the string-indexed intervals.
    """

    # create a list to store the various outputs
    outputs = list()

    # B starts and ends after A
    outputs.append(
        [
            {'start': "A", 'finish': "B", 'set_items': {'1'}},
            {'start': "B", 'finish': "D", 'set_items': {'1', '2'}},
            {'start': "D", 'finish': "F", 'set_items': {'2'}}
        ]
    )

    # B starts after A but ends at the same time as A
    outputs.append(
        [
            {'start': "A", 'finish': "B", 'set_items': {'1'}},
            {'start': "B", 'finish': "D", 'set_items': {'2', '1'}}
        ]
    )

    # B starts after A and ends before A
    outputs.append(
        [
            {'start': "A", 'finish': "B", 'set_items': {'1'}},
            {'start': "B", 'finish': "C", 'set_items': {'2', '1'}},
            {'start': "C", 'finish': "D", 'set_items': {'1'}}
        ]
    )

    return outputs


# tests
def test_interval_types(interval_inputs, interval_outputs) -> None:
    """
    For each of the available input types, tests whether the output is correct.
    :param interval_inputs: A set of all types of interval overlaps.
    :param interval_outputs: A set of outputs for all types of interval overlaps.
    :return: None
    """

    for output in interval_outputs:
        for interval in output:
            interval["set_items"] = set(sorted(interval["set_items"], reverse=True))

    for i, o in zip(interval_inputs, interval_outputs):
        out = sorted(Merge.union(i), key=itemgetter('start', 'finish'))
        assert out == sorted(o, key=itemgetter('start', 'finish'))


def test_complex_interval_types(complex_interval_inputs, complex_interval_outputs) -> None:
    """
    For each of the available input types, tests whether the output is correct.
    :param complex_interval_inputs: A set of complex interval overlaps.
    :param complex_interval_outputs: A set of outputs for all complex interval overlaps.
    :return: None
    """

    for i, o in zip(complex_interval_inputs, complex_interval_outputs):
        out = sorted(Merge.union(i), key=itemgetter('start', 'finish'))
        assert len(out) == len(o)
        
        o = sorted(o, key=itemgetter('start', 'finish'))
        assert out == o
        for out, expected in zip(out, o):
            assert out == expected


def test_interval_integers(interval_inputs_integers, interval_outputs_integers) -> None:
    """
    For each of the available input types, tests whether the output is correct.
    :param interval_inputs_integers: A set of all types of interval overlaps.
    :param interval_outputs_integers: A set of outputs for all types of interval overlaps.
    :return: None
    """

    for output in interval_outputs_integers:
        for interval in output:
            interval["set_items"] = set(sorted(interval["set_items"], reverse=True))

    for i, o in zip(interval_inputs_integers, interval_outputs_integers):
        out = sorted(Merge.union(i), key=itemgetter('start', 'finish'))
        assert out == sorted(o, key=itemgetter('start', 'finish'))


def test_interval_strings(interval_inputs_strings, interval_outputs_strings) -> None:
    """
    For each of the available input types, tests whether the output is correct.
    :param interval_inputs_strings: A set of all types of interval overlaps.
    :param interval_outputs_strings: A set of outputs for all types of interval overlaps.
    :return: None
    """

    for output in interval_outputs_strings:
        for interval in output:
            interval["set_items"] = set(sorted(interval["set_items"], reverse=True))

    for i, o in zip(interval_inputs_strings, interval_outputs_strings):
        out = sorted(Merge.union(i), key=itemgetter('start', 'finish'))
        assert out == sorted(o, key=itemgetter('start', 'finish'))


# def test_incorrect_format(interval_inputs) -> None:
#     """
#     Ensures that the correct type and number of warnings are issued when the user uses a
#     list of items instead of a set, which is the correct formatting.
#     :param interval_inputs: A set of all types of interval overlaps.
#     :return: None
#     """

#     # convert the set to a list, which is the incorrect input format
#     for i in interval_inputs:

#         for j in i:
#             j["set_items"] = sorted(j["set_items"])

#         with pytest.warns(UserWarning) as record:

#             # try to do a merge with a list
#             Merge.union(i)


def test_alternate_attribute_key(interval_inputs) -> None:
    """
    Ensures that an attribute other than "set_items" can be used as input.
    :param interval_inputs: A set of all types of interval overlaps.
    :return: None
    """

    # first change the attribute from "set_items" to "items"
    for i in interval_inputs:
        for j in i:
            j["items"] = j["set_items"]
            del j["set_items"]

    # ensure there's some output and that the key is correct
    for i in interval_inputs:
        out = Merge.union(i, key="items")
        for j in out:
            assert "items" in j.keys()


# def test_return_graph(interval_inputs) -> None:
#     """
#     Ensures that a netwworkx.DiGraph object is returned with 'return_graph' is
#     set to True.
#     :param interval_inputs: A set of all types of interval overlaps.
#     :return: None
#     """

#     for i in interval_inputs:
#         out = Merge.union(i, return_graph=True)
#         assert type(out).__name__ == "DiGraph"


def test_nx_exception() -> None:

    """
    Tests an exception which may occur in some scenarios such as one in which a "waterfall" of intervals occurs.
    :return: None
    """

    # create a seed interval
    seed_interval = [
        {"start": datetime.datetime(2020, 1, 1, 1, 0, 0), "finish": datetime.datetime(2020, 1, 4, 1, 0, 0),
         "set_items": {"1"}}
    ]

    # let's create 10 intervals
    interval_counts = list(range(0, 100, 10))

    inputs = list()
    intervals = list()

    # create 10 intervals in a sequence with the same overlap
    for i in interval_counts:
        intervals = seed_interval + list()
        for j in range(i):

            # get the last interval
            update_interval = intervals[-1]

            # add 2 hours to the start and end times
            new_interval = update_interval.copy()
            new_interval["start"] = update_interval["start"] + datetime.timedelta(hours=2)
            new_interval["finish"] = update_interval["finish"] + datetime.timedelta(hours=2)

            # update the set items
            new_interval["set_items"] = {str(j)}

            # append the interval(s)
            intervals.append(new_interval)

        inputs.append(intervals)

    # make sure we run without errors and return a result
    out = Merge.union(intervals=intervals)
    assert out is not None
