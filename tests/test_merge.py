# Authors: Valentino Constantinou <vconstan@jpl.caltech.edu>, Asitang Mishra <asitang.mishra@jpl.caltech.edu>
# License: Apache 2.0

from mieda.intervals import Merge

import datetime
import pytest


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


def test_complex_interval_types(complex_interval_inputs, complex_interval_outputs) -> None:
    """
    For each of the available input types, tests whether the output is correct.
    :param complex_interval_inputs: A set of complex interval overlaps.
    :param complex_interval_outputs: A set of outputs for all complex interval overlaps.
    :return: None
    """

    # TODO: the sets ar not guaranteed to come out in the correct order -- need improved test

    for i, o in zip(complex_interval_inputs, complex_interval_outputs):
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
