"""Tests for miller.identity."""

from __future__ import annotations

import pathlib
from collections import UserDict, UserList
from collections.abc import MutableSet

import pytest

import miller
from miller import identity


class MyDict(UserDict):
    pass


class MyList(UserList):
    pass


class MySet(MutableSet):
    def __init__(self):
        self._s = set()

    def __contains__(self, x):
        return x in self._s

    def __iter__(self):
        return iter(self._s)

    def __len__(self):
        return len(self._s)

    def add(self, x):
        self._s.add(x)

    def discard(self, x):
        self._s.discard(x)


def function():
    return


class Thing:
    pass


def test_is_class():
    assert identity.is_class(Thing)
    assert not identity.is_class(Thing())
    with pytest.raises(TypeError):
        identity.is_class(Thing(), raise_error = True)


def test_is_container():
    for item in ({'a': 1}, MyDict(), [1], (1,), {1}, frozenset()):
        assert identity.is_container(item)
    assert identity.is_container(list)
    assert identity.is_container('str', include_str = True)
    assert not identity.is_container('str')
    assert not identity.is_container('str', include_str = False)
    assert not identity.is_container(5)
    miller.set_include_str(True)
    assert identity.is_container('str')
    with pytest.raises(TypeError):
        identity.is_container(5, raise_error = True)


def test_is_dict():
    assert identity.is_dict({})
    assert identity.is_dict(dict)
    assert identity.is_dict(MyDict())
    assert not identity.is_dict(MyDict(), include_generic = False)
    assert identity.is_dict({}, include_generic = False)
    assert not identity.is_dict([])
    assert not identity.is_dict({1})


def test_is_dunder():
    assert identity.is_dunder('__init__')
    assert identity.is_dunder(Thing().__init__)
    assert identity.is_dunder(Thing.__str__)
    assert not identity.is_dunder('_private')
    assert not identity.is_dunder('public')
    assert not identity.is_dunder('____')


def test_is_file_and_folder(tmp_path):
    file = tmp_path / 'f.txt'
    file.write_text('x')
    assert identity.is_file(file)
    assert identity.is_file(str(file))
    assert identity.is_file_path(file)
    assert not identity.is_file(tmp_path)
    assert not identity.is_file(tmp_path / 'missing')
    assert not identity.is_file(5)
    assert identity.is_folder(tmp_path)
    assert identity.is_folder_path(str(tmp_path))
    assert not identity.is_folder(file)
    assert not identity.is_folder(None)
    with pytest.raises(TypeError):
        identity.is_file(tmp_path, raise_error = True)
    with pytest.raises(TypeError):
        identity.is_folder(file, raise_error = True)


def test_is_function():
    assert identity.is_function(function)
    assert identity.is_function(lambda: None)
    assert not identity.is_function(Thing)
    assert not identity.is_function(Thing().__init__)


def test_is_instance():
    assert identity.is_instance(Thing())
    assert identity.is_instance(5)
    assert not identity.is_instance(Thing)
    assert identity.is_instance(Thing(), Thing)
    assert not identity.is_instance(5, Thing)
    assert identity.is_instance(5, (int, str))
    with pytest.raises(TypeError):
        identity.is_instance(Thing, raise_error = True)


def test_is_iterable():
    for item in ({}, [], (), set(), MyList(), iter([])):
        assert identity.is_iterable(item)
    assert identity.is_iterable('a', include_str = True)
    assert not identity.is_iterable('a')
    assert not identity.is_iterable(5)


def test_is_list():
    assert identity.is_list([])
    assert identity.is_list(list)
    assert identity.is_list(MyList())
    assert not identity.is_list(MyList(), include_generic = False)
    assert not identity.is_list(())
    assert not identity.is_list({})
    assert not identity.is_list('abc')


def test_is_module(tmp_path):
    module = tmp_path / 'm.py'
    module.write_text('')
    other = tmp_path / 'm.txt'
    other.write_text('')
    assert identity.is_module(module)
    assert identity.is_module(str(module))
    assert identity.is_module(pathlib)
    assert not identity.is_module(other)
    assert not identity.is_module(tmp_path)
    assert not identity.is_module(5)
    miller.set_module_extensions(['.txt'])
    assert identity.is_module(other)
    assert not identity.is_module(module)


def test_is_nested():
    assert identity.is_nested({'a': {'b': 1}})
    assert identity.is_nested([1, [2]])
    assert identity.is_nested((1, (2,)))
    assert identity.is_nested({frozenset({1})})
    assert identity.is_nested([{'a': 1}])
    assert not identity.is_nested({'a': 1})
    assert not identity.is_nested([1, 'abc'])
    assert not identity.is_nested('abc')
    assert not identity.is_nested(5)
    with pytest.raises(TypeError):
        identity.is_nested([1], raise_error = True)


def test_is_nested_types():
    assert identity.is_nested_dict({'a': {}})
    assert not identity.is_nested_dict([[1]])
    assert identity.is_nested_list([[1]])
    assert not identity.is_nested_list(([1],))
    assert identity.is_nested_set({frozenset({1})})
    assert not identity.is_nested_set([[1]])
    assert identity.is_nested_tuple(((1,),))
    assert not identity.is_nested_tuple([(1,)])


def test_is_object():
    assert identity.is_object(Thing())
    assert identity.is_object(5)
    assert not identity.is_object(Thing)
    assert not identity.is_object(function)
    assert not identity.is_object(pathlib)
    assert not identity.is_object(Thing().__init__)


def test_is_path(tmp_path):
    assert identity.is_path(tmp_path)
    assert identity.is_path(str(tmp_path))
    assert not identity.is_path(tmp_path / 'missing')
    assert not identity.is_path(5)


def test_is_private():
    assert identity.is_private('_a')
    assert identity.is_private('__a__')
    assert not identity.is_private('a')
    assert not identity.is_private(function)
    assert identity.is_private(Thing.__init__)


def test_is_sequence():
    assert identity.is_sequence([])
    assert identity.is_sequence(())
    assert identity.is_sequence(list)
    assert identity.is_sequence('a', include_str = True)
    assert not identity.is_sequence('a')
    assert not identity.is_sequence({})
    assert not identity.is_sequence({1})


def test_is_set():
    assert identity.is_set({1})
    assert identity.is_set(frozenset())
    assert identity.is_set(MySet())
    assert not identity.is_set(MySet(), include_generic = False)
    assert identity.is_set(set(), include_generic = False)
    assert not identity.is_set([])
    assert not identity.is_set({})


def test_is_tuple():
    assert identity.is_tuple((1,))
    assert identity.is_tuple(tuple)
    assert not identity.is_tuple([1])
