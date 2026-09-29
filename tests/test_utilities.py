"""Tests for miller.utilities."""

from __future__ import annotations

import pathlib

import pytest

from miller import utilities


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        (None, []),
        ('string', ['string']),
        (b'bytes', [b'bytes']),
        (bytearray(b'x'), [bytearray(b'x')]),
        ([1, 2, 3], [1, 2, 3]),
        ((1, 2), (1, 2)),
        ({1, 2}, {1, 2}),
        ({'a': 1}, {'a': 1}),
        (42, [42]),
        (3.14, [3.14]),
        (True, [True]),
    ])
def test_iterify(value, expected):
    assert utilities.iterify(value) == expected


def test_iterify_returns_same_object():
    item = [1, 2]
    assert utilities.iterify(item) is item


def test_namify():
    class Named:
        name = 'named'

    class Other:
        pass

    def function():
        pass

    assert utilities.namify('text') == 'text'
    assert utilities.namify(Named()) == 'named'
    assert utilities.namify(function) == 'function'
    assert utilities.namify(Other) == 'Other'
    assert utilities.namify(Other()) == 'Other'
    assert utilities.namify(3, default = 'fallback') == 'fallback'
    assert utilities.namify(3) == 'int'


def test_namify_ignores_non_str_name():
    class Odd:
        name = 5

    assert utilities.namify(Odd()) == 'Odd'


def test_namify_survives_broken_attribute():
    class Broken:
        @property
        def name(self):
            raise RuntimeError('broken')

    assert utilities.namify(Broken()) == 'Broken'


def test_pathlibify(tmp_path):
    assert utilities.pathlibify('a/b') == pathlib.Path('a/b')
    assert utilities.pathlibify(tmp_path) is tmp_path
    with pytest.raises(TypeError):
        utilities.pathlibify(5)


def test_is_private_name():
    assert utilities.is_private_name('_a')
    assert utilities.is_private_name('__a__')
    assert not utilities.is_private_name('a_')


def test_drop_privates():
    assert utilities.drop_privates(['a', '_b', '__c__', 'd']) == ['a', 'd']
    assert utilities.drop_privates(('a', '_b')) == ['a']
    assert utilities.drop_privates({'a': 1, '_b': 2, 3: 4}) == {'a': 1, 3: 4}
