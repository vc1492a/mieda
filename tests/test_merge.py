# Authors: Valentino Constantinou <vconstan@jpl.caltech.edu>, Asitang Mishra <asitang.mishra@jpl.caltech.edu>
# License: Apache 2.0

from mieda.intervals import Merge

import datetime
import pytest


# TODO: unit test for uneven ordering - add param to input and output fixtures?
# TODO: test to ensure proper result when input format is incorrect
# TODO: add unit test for complex patterns

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

    return outputs


# tests
def test_interval_types(interval_inputs, interval_outputs) -> None:
    """
    For each of the available input types, tests whether the output is correct.
    :param interval_inputs: A set of all types of interval overlaps.
    :param interval_outputs: A set of outputs for all types of interval overlaps.
    :return: None
    """

    for i, o in zip(interval_inputs, interval_outputs):
        out = Merge.union(i)
        assert out == o


def test_incorrect_format(interval_inputs) -> None:
    """
    Ensures that the correct type and number of warnings are issued when the user uses a
    list of items instead of a set, which is the correct formatting.
    :param interval_inputs: A set of all types of interval overlaps.
    :return: None
    """

    # convert the set to a list, which is the incorrect input format
    for i in interval_inputs:

        for j in i:
            j["set_items"] = sorted(j["set_items"])

        with pytest.warns(UserWarning) as record:

            # try to do a merge with a list
            Merge.union(i)

            # check that only one warning was raised
            assert len(record) == 1
            # check that the message matches
            assert record[0].message.args[
                       0] == "The correct input format is a set - converted lists to sets."

