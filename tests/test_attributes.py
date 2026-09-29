"""Tests for miller.attributes."""

from __future__ import annotations

import dataclasses
import inspect

import pytest
from conftest import Child, Data, Parent, Slotted

import miller
from miller import attributes


def test_is_attribute(parent):
    assert attributes.is_attribute(parent, 'method')
    assert attributes.is_attribute(parent, 'instance_variable')
    assert attributes.is_attribute(Parent, 'class_variable')
    assert not attributes.is_attribute(Parent, 'instance_variable')
    assert not attributes.is_attribute(parent, 'missing')
    with pytest.raises(AttributeError):
        attributes.is_attribute(parent, 'missing', raise_error = True)


def test_is_class_attribute(parent):
    assert attributes.is_class_attribute(parent, 'class_variable')
    assert attributes.is_class_attribute(Parent, 'class_variable')
    assert attributes.is_class_attribute(Child(), 'class_variable')
    assert not attributes.is_class_attribute(parent, 'instance_variable')


def test_is_field(data):
    assert attributes.is_field(data, 'x')
    assert attributes.is_field(Data, 'y')
    assert not attributes.is_field(data, 'total')
    assert not attributes.is_field(Parent(), 'class_variable')


def test_is_instance_attribute(parent):
    assert attributes.is_instance_attribute(parent, 'instance_variable')
    assert not attributes.is_instance_attribute(parent, 'class_variable')
    assert not attributes.is_instance_attribute(Parent, 'instance_variable')
    slotted = Slotted()
    assert attributes.is_instance_attribute(slotted, 'a')
    assert not attributes.is_instance_attribute(slotted, 'b')


def test_is_method(parent):
    for name in ('method', 'class_method', 'static_method'):
        assert attributes.is_method(parent, name)
        assert attributes.is_method(Parent, name)
    assert attributes.is_method(list, 'append')
    assert not attributes.is_method(parent, 'prop')
    assert not attributes.is_method(parent, 'class_variable')
    assert not attributes.is_method(parent, 'missing')
    parent.stored = lambda: None
    assert not attributes.is_method(parent, 'stored')
    assert attributes.is_method(attributes, 'is_method')


def test_is_property(parent):
    assert attributes.is_property(parent, 'prop')
    assert attributes.is_property(Parent, 'prop')
    assert not attributes.is_property(parent, 'method')
    assert not attributes.is_property(parent, 'missing')


def test_is_variable(parent):
    assert attributes.is_variable(parent, 'class_variable')
    assert attributes.is_variable(parent, 'instance_variable')
    assert not attributes.is_variable(parent, 'method')
    assert not attributes.is_variable(parent, 'prop')
    assert not attributes.is_variable(parent, 'missing')
    with pytest.raises(AttributeError):
        attributes.is_variable(parent, 'method', raise_error = True)


def test_attributes_functions(parent):
    names = attributes.name_attributes(parent)
    assert 'method' in names
    assert 'instance_variable' in names
    assert '_private_method' not in names
    assert '__init__' not in names
    assert '_private_method' in attributes.name_attributes(
        parent, include_privates = True)
    catalog = attributes.catalog_attributes(Parent)
    assert catalog['class_variable'] == 1
    assert attributes.collect_attributes(Parent)
    assert attributes.has_attributes(parent, ['method', 'prop'])
    assert not attributes.has_attributes(parent, ['method', 'missing'])
    assert attributes.has_attributes(
        parent, ['method', 'missing'], match_all = False)
    assert attributes.has_attributes(parent, 'method')
    with pytest.raises(AttributeError):
        attributes.has_attributes(parent, 'missing', raise_error = True)
    miller.set_raise_errors(True)
    with pytest.raises(AttributeError):
        attributes.has_attributes(parent, 'missing')
    assert attributes.has_attributes(
        parent, 'missing', raise_error = False) is False


def test_global_include_privates(parent):
    miller.set_include_privates(True)
    assert '_private_method' in attributes.name_methods(parent)
    assert '_private_method' not in attributes.name_methods(
        parent, include_privates = False)


def test_class_attributes_functions(parent):
    names = attributes.name_class_attributes(Parent)
    assert 'class_variable' in names
    assert 'instance_variable' not in names
    catalog = attributes.catalog_class_attributes(parent)
    assert catalog['class_variable'] == 1
    assert 1 in attributes.collect_class_attributes(parent)
    assert attributes.has_class_attributes(parent, 'class_variable')
    assert not attributes.has_class_attributes(parent, 'instance_variable')


def test_fields_functions(data):
    assert attributes.name_fields(data) == ['x', 'y']
    assert attributes.name_fields(Data, include_privates = True) == [
        'x', 'y', '_z']
    catalog = attributes.catalog_fields(data)
    assert list(catalog) == ['x', 'y']
    assert all(isinstance(f, dataclasses.Field) for f in catalog.values())
    assert len(attributes.collect_fields(data)) == 2
    assert attributes.has_fields(data, ['x', 'y'])
    assert not attributes.has_fields(data, ['x', 'total'])
    for function in (
            attributes.name_fields,
            attributes.catalog_fields,
            attributes.collect_fields):
        with pytest.raises(TypeError):
            function(Parent())
    with pytest.raises(TypeError):
        attributes.has_fields(Parent(), 'x')


def test_instance_attributes_functions(parent):
    assert attributes.name_instance_attributes(parent) == [
        'instance_variable']
    assert attributes.name_instance_attributes(
        parent, include_privates = True) == [
        '_private_instance', 'instance_variable']
    assert attributes.catalog_instance_attributes(parent) == {
        'instance_variable': 3}
    assert attributes.collect_instance_attributes(parent) == [3]
    assert attributes.has_instance_attributes(parent, 'instance_variable')
    assert not attributes.has_instance_attributes(parent, 'class_variable')
    assert attributes.name_instance_attributes(Parent) == []


def test_methods_functions(parent):
    assert attributes.name_methods(parent) == [
        'class_method', 'method', 'static_method']
    assert '_private_method' in attributes.name_methods(
        Parent, include_privates = True)
    assert attributes.catalog_methods(parent)['method'](5) == 5
    assert len(attributes.collect_methods(parent)) == 3
    assert attributes.has_methods(parent, ['method', 'class_method'])
    assert not attributes.has_methods(parent, ['method', 'prop'])


def test_properties_functions(parent):
    assert attributes.name_properties(parent) == ['broken_prop', 'prop']
    catalog = attributes.catalog_properties(parent)
    assert catalog['prop'] == 5
    # Properties that raise errors fall back to the raw property object.
    assert isinstance(catalog['broken_prop'], property)
    assert isinstance(attributes.catalog_properties(Parent)['prop'], property)
    assert len(attributes.collect_properties(parent)) == 2
    assert attributes.has_properties(parent, 'prop')
    assert not attributes.has_properties(parent, 'method')


def test_variables_functions(parent):
    assert attributes.name_variables(parent) == [
        'class_variable', 'instance_variable']
    assert attributes.catalog_variables(parent) == {
        'class_variable': 1, 'instance_variable': 3}
    assert sorted(attributes.collect_variables(parent)) == [1, 3]
    assert attributes.has_variables(parent, ['class_variable'])
    assert not attributes.has_variables(parent, ['method'])


def test_signatures_functions(parent):
    catalog = attributes.catalog_signatures(parent)
    assert set(catalog) == {'class_method', 'method', 'static_method'}
    assert all(isinstance(s, inspect.Signature) for s in catalog.values())
    assert list(catalog['method'].parameters) == ['value']
    assert attributes.name_signatures(parent) == list(catalog)
    assert len(attributes.collect_signatures(parent)) == 3
    assert attributes.has_signatures(parent, 'method')
    assert not attributes.has_signatures(parent, 'prop')
    assert 'is_method' in attributes.catalog_signatures(attributes)


def test_annotations_functions(child, data):
    names = attributes.name_annotations(Child)
    assert names == ['class_variable', 'child_variable']
    assert attributes.name_annotations(child) == names
    assert attributes.name_annotations(
        Parent, include_privates = True) == [
        'class_variable', '_private_variable']
    assert attributes.name_annotations(data) == ['x', 'y']
    assert len(attributes.collect_annotations(Data)) == 2
    assert attributes.has_annotations(Child, ['class_variable'])
    assert not attributes.has_annotations(Child, 'method')
    assert attributes.name_annotations(Parent.method) == ['value', 'return']
    assert attributes.catalog_annotations(
        attributes, include_privates = True)['_MISSING'] == 'Any'
