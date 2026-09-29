"""Tests for miller.examiners."""

from __future__ import annotations

import pathlib

import pytest
from conftest import Data, Parent

import miller
from miller import examiners


def test_factory(parent, tree):
    assert isinstance(examiners.Inspector(Parent), examiners.ClassInspector)
    assert isinstance(
        examiners.Inspector(parent), examiners.InstanceInspector)
    assert isinstance(
        examiners.Inspector(miller.utilities), examiners.ModuleInspector)
    assert isinstance(examiners.Inspector(tree), examiners.PackageInspector)
    assert isinstance(
        examiners.Inspector(str(tree)), examiners.PackageInspector)
    assert isinstance(examiners.Inspector(5), examiners.InstanceInspector)
    assert isinstance(examiners.Inspector([1]), examiners.InstanceInspector)


def test_direct_subclass_creation(parent):
    inspector = examiners.ClassInspector(Parent, include_privates = True)
    assert inspector.item is Parent
    assert inspector.include_privates is True


def test_common_properties(parent):
    inspector = examiners.Inspector(parent)
    assert inspector.name == 'Parent'
    assert inspector.type is Parent
    assert 'Parent' in repr(inspector)
    assert examiners.Inspector(Parent).name == 'Parent'


def test_class_inspector(parent):
    inspector = examiners.Inspector(Parent)
    assert list(inspector.methods) == [
        'class_method', 'method', 'static_method']
    assert list(inspector.properties) == ['broken_prop', 'prop']
    assert list(inspector.variables) == ['class_variable']
    assert 'class_variable' in inspector.class_attributes
    assert 'class_variable' in inspector.attributes
    assert 'method' in inspector.signatures
    assert inspector.annotations == {'class_variable': 'int'}
    assert inspector.parameters == ['class_variable']
    assert inspector.fields == {}
    assert inspector.contains is None
    private = examiners.ClassInspector(Parent, include_privates = True)
    assert '_private_method' in private.methods


def test_class_inspector_dataclass(data):
    inspector = examiners.Inspector(Data)
    assert list(inspector.fields) == ['x', 'y']
    assert list(examiners.Inspector(data).fields) == ['x', 'y']


def test_instance_inspector(parent):
    inspector = examiners.Inspector(parent)
    assert inspector.instance_attributes == {'instance_variable': 3}
    assert 'class_variable' in inspector.class_attributes
    assert inspector.variables == {
        'class_variable': 1, 'instance_variable': 3}
    assert inspector.properties['prop'] == 5
    assert examiners.Inspector([1, 'a']).contains == (int, str)
    assert examiners.Inspector({'a': 1}).contains == (int,)


def test_module_inspector():
    inspector = examiners.Inspector(miller.framework)
    assert 'set_recursion' in inspector.functions
    assert inspector.classes == {}
    assert 'set_recursion' in inspector.methods
    assert 'set_recursion' in inspector.signatures
    assert '__version__' not in inspector.variables
    assert 'Any' in inspector.variables
    assert examiners.Inspector(miller.examiners).classes['Inspector'] is (
        examiners.Inspector)


def test_package_inspector(tree):
    inspector = examiners.Inspector(tree)
    assert isinstance(inspector.item, pathlib.Path)
    assert list(inspector.paths) == [
        'a.py', 'b.txt', 'empty', 'sub', 'sub/c.py', 'sub/d.txt']
    assert list(inspector.file_paths) == [
        'a.py', 'b.txt', 'sub/c.py', 'sub/d.txt']
    assert list(inspector.folder_paths) == ['empty', 'sub']
    assert list(inspector.modules) == ['a', 'sub.c']
    shallow = examiners.PackageInspector(tree, recursive = False)
    assert list(shallow.modules) == ['a']
    private = examiners.PackageInspector(tree, include_privates = True)
    assert '_hidden' in private.modules
    assert inspector.name == tree.name


def test_repr_and_types_raise_nothing(parent):
    for item in (parent, Parent, miller, 5, 'text'):
        inspector = examiners.Inspector(item)
        assert isinstance(repr(inspector), str)


def test_package_inspector_bad_path():
    with pytest.raises(TypeError):
        examiners.PackageInspector(5)
