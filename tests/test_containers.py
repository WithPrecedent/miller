"""Tests for miller.containers."""

from __future__ import annotations

import pytest

import miller
from miller import containers


def test_collect_types():
    assert containers.collect_types([1, 'a', 2, 3.0]) == (int, str, float)
    assert containers.collect_types((1, 2)) == (int,)
    assert containers.collect_types({1, 2}) == (int,)
    assert containers.collect_types({'a': 1, 'b': 'c'}) == (int, str)
    assert containers.collect_types([]) == ()
    for bad in (5, 'string', b'bytes'):
        with pytest.raises(TypeError):
            containers.collect_types(bad)


def test_collect_key_types():
    assert containers.collect_key_types({'a': 1, 2: 3}) == (str, int)
    with pytest.raises(TypeError):
        containers.collect_key_types([1])


def test_has_types():
    assert containers.has_types([1, 'a'], [int, str])
    assert containers.has_types([1, 'a'], int)
    assert containers.has_types([True], int)
    assert not containers.has_types([1], [int, str])
    assert containers.has_types([1], [int, str], match_all = False)
    assert not containers.has_types([1], [str, bytes], match_all = False)
    assert containers.has_types({'a': 1}, int)
    assert not containers.has_types([], int)
    with pytest.raises(AttributeError):
        containers.has_types([1], str, raise_error = True)
    miller.set_match_all(False)
    assert containers.has_types([1], [int, str])
    with pytest.raises(TypeError):
        containers.has_types(5, int)
