"""Tests for miller.modules."""

from __future__ import annotations

import pytest

import miller
from miller import modules


def test_classes(dummy_module):
    assert modules.name_classes(dummy_module) == [
        'DummyClass', 'DummyDataclass']
    assert modules.collect_classes(dummy_module) == [
        dummy_module.DummyClass, dummy_module.DummyDataclass]
    assert modules.catalog_classes(dummy_module) == {
        'DummyClass': dummy_module.DummyClass,
        'DummyDataclass': dummy_module.DummyDataclass}
    assert modules.has_classes(dummy_module, 'DummyClass')
    assert modules.has_classes(dummy_module, ['DummyClass', 'DummyDataclass'])
    assert not modules.has_classes(dummy_module, ['DummyClass', 'missing'])
    assert modules.has_classes(
        dummy_module, ['DummyClass', 'missing'], match_all = False)
    assert not modules.has_classes(dummy_module, 'dummy_function')
    with pytest.raises(AttributeError):
        modules.has_classes(dummy_module, 'missing', raise_error = True)


def test_classes_exclude_imports(dummy_module):
    # The dummy module imports `dataclasses` but not any classes from it.
    assert 'dataclass' not in modules.name_functions(dummy_module)
    assert modules.name_classes(miller.examiners) == [
        'ClassInspector',
        'Inspector',
        'InstanceInspector',
        'ModuleInspector',
        'PackageInspector']
    assert '_AttributeInspector' in modules.name_classes(
        miller.examiners, include_privates = True)


def test_functions(dummy_module):
    assert modules.name_functions(dummy_module) == ['dummy_function']
    assert modules.collect_functions(dummy_module) == [
        dummy_module.dummy_function]
    assert modules.catalog_functions(dummy_module) == {
        'dummy_function': dummy_module.dummy_function}
    assert modules.has_functions(dummy_module, 'dummy_function')
    assert not modules.has_functions(dummy_module, 'DummyClass')
    assert not modules.has_functions(dummy_module, ['dummy_function', 'no'])


def test_private_functions():
    assert '_members' not in modules.name_functions(modules)
    assert '_members' in modules.name_functions(
        modules, include_privates = True)


def test_module_name_string():
    assert 'name_classes' in modules.name_functions('miller.modules')
    assert 'name_classes' in modules.name_functions(
        'miller.modules', include_privates = False)


def test_bad_module():
    with pytest.raises(TypeError):
        modules.name_classes(5)
    with pytest.raises(ModuleNotFoundError):
        modules.name_classes('not_a_real_module_name')
