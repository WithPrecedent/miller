"""Tests for miller.framework, miller.configuration, and miller.base."""

from __future__ import annotations

import pytest

import miller
from miller import base, configuration, framework


@pytest.mark.parametrize(
    ('function', 'setting'),
    [
        (framework.set_include_privates, 'INCLUDE_PRIVATES'),
        (framework.set_include_str, 'INCLUDE_STR'),
        (framework.set_match_all, 'MATCH_ALL'),
        (framework.set_raise_errors, 'RAISE_ERRORS'),
        (framework.set_recursion, 'RECURSIVE'),
    ])
def test_boolean_setters(function, setting):
    function(True)
    assert getattr(configuration, setting) is True
    function(False)
    assert getattr(configuration, setting) is False
    for bad in ('True', 1, None):
        with pytest.raises(TypeError):
            function(bad)


def test_set_keyer():
    def keyer(item):
        return 'key'

    framework.set_keyer(keyer)
    assert configuration.KEYER is keyer
    assert miller.is_dunder('anything') is False
    with pytest.raises(TypeError):
        framework.set_keyer('not callable')


def test_set_module_extensions():
    framework.set_module_extensions(['.py', '.pyw'])
    assert configuration.MODULE_EXTENSIONS == ('.py', '.pyw')
    framework.set_module_extensions(('.py',))
    assert configuration.MODULE_EXTENSIONS == ('.py',)
    for bad in ('.py', 5, ['.py', 5]):
        with pytest.raises(TypeError):
            framework.set_module_extensions(bad)


def test_resolve():
    assert base.resolve(None, True) is True
    assert base.resolve(False, True) is False
    assert base.resolve(0, 5) == 0


def test_verdict():
    assert base.verdict(True, True, 'message') is True
    assert base.verdict(False, False, 'message') is False
    with pytest.raises(TypeError, match = 'message'):
        base.verdict(False, True, 'message')
    with pytest.raises(KeyError):
        base.verdict(False, True, 'message', KeyError)
    configuration.RAISE_ERRORS = True
    with pytest.raises(TypeError):
        base.verdict(False, None, 'message')
    assert base.verdict(False, False, 'message') is False


def test_has_names():
    def checker(item, name, raise_error = False):
        return name in item

    assert base.has_names('abc', ['a', 'b'], checker)
    assert base.has_names('abc', 'a', checker)
    assert not base.has_names('abc', ['a', 'z'], checker)
    assert base.has_names('abc', ['a', 'z'], checker, match_all = False)
    assert not base.has_names('abc', ['y', 'z'], checker, match_all = False)
    with pytest.raises(AttributeError, match = 'Not all'):
        base.has_names('abc', ['a', 'z'], checker, raise_error = True)
    with pytest.raises(AttributeError, match = 'None'):
        base.has_names(
            'abc', ['y', 'z'], checker, raise_error = True, match_all = False)


def test_name_and_catalog_where():
    names = ['a', '_b', 'c']
    assert base.name_where(names, lambda n: n != 'c') == ['a']
    assert base.name_where(
        names, lambda n: n != 'c', include_privates = True) == ['a', '_b']
    assert base.catalog_where(
        names, lambda _: True, str.upper, include_privates = True) == {
        'a': 'A', '_b': '_B', 'c': 'C'}
    configuration.INCLUDE_PRIVATES = True
    assert base.name_where(names, lambda _: True) == names


def test_has_functions_ignore_global_raise_errors_until_the_end(parent=None):
    """Regression: inner `is_*` checks must not raise on their own."""
    class Example:
        present = 1

    miller.set_raise_errors(True)
    assert miller.has_attributes(Example, ['present']) is True
    assert miller.has_attributes(
        Example, ['present', 'absent'], match_all = False) is True
    with pytest.raises(AttributeError):
        miller.has_attributes(Example, ['present', 'absent'])
