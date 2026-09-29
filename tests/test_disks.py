"""Tests for miller.disks."""

from __future__ import annotations

import pathlib

import pytest

import miller
from miller import disks


def test_paths(tree):
    assert disks.name_paths(tree) == ['a.py', 'b.txt', 'empty', 'sub']
    assert disks.collect_paths(tree) == [
        tree / 'a.py', tree / 'b.txt', tree / 'empty', tree / 'sub']
    assert disks.catalog_paths(tree)['sub'] == tree / 'sub'
    assert disks.name_paths(tree, recursive = True) == [
        'a.py', 'b.txt', 'empty', 'sub', 'sub/c.py', 'sub/d.txt']
    assert disks.name_paths(str(tree), include_privates = True) == [
        '__pycache__', '_hidden.py', 'a.py', 'b.txt', 'empty', 'sub']


def test_file_paths(tree):
    assert disks.name_file_paths(tree) == ['a.py', 'b.txt']
    assert disks.collect_file_paths(tree) == [tree / 'a.py', tree / 'b.txt']
    assert disks.catalog_file_paths(tree) == {
        'a.py': tree / 'a.py', 'b.txt': tree / 'b.txt'}
    assert disks.name_file_paths(tree, recursive = True) == [
        'a.py', 'b.txt', 'sub/c.py', 'sub/d.txt']
    assert disks.name_file_paths(
        tree, recursive = True, include_privates = True) == [
        '__pycache__/a.cpython.pyc',
        '_hidden.py',
        'a.py',
        'b.txt',
        'sub/__init__.py',
        'sub/c.py',
        'sub/d.txt']


def test_folder_paths(tree):
    assert disks.name_folder_paths(tree) == ['empty', 'sub']
    assert disks.collect_folder_paths(tree) == [tree / 'empty', tree / 'sub']
    assert disks.catalog_folder_paths(tree) == {
        'empty': tree / 'empty', 'sub': tree / 'sub'}
    assert disks.name_folder_paths(
        tree, include_privates = True) == ['__pycache__', 'empty', 'sub']


def test_modules(tree):
    assert disks.name_modules(tree) == ['a']
    assert disks.name_modules(tree, recursive = True) == ['a', 'sub.c']
    assert disks.name_modules(
        tree, recursive = True, include_privates = True) == [
        '_hidden', 'a', 'sub.__init__', 'sub.c']
    assert disks.collect_modules(tree) == [tree / 'a.py']
    assert disks.catalog_modules(tree, recursive = True) == {
        'a': tree / 'a.py', 'sub.c': tree / 'sub' / 'c.py'}
    miller.set_module_extensions(['.txt'])
    assert disks.name_modules(tree) == ['b']


def test_global_recursion(tree):
    miller.set_recursion(True)
    assert 'sub/c.py' in disks.name_file_paths(tree)
    assert 'sub/c.py' not in disks.name_file_paths(tree, recursive = False)


def test_has_paths(tree):
    assert disks.has_paths(tree, ['a.py', 'sub'])
    assert disks.has_paths(tree, 'a.py')
    assert disks.has_paths(tree, tree / 'a.py')
    assert disks.has_paths(tree, pathlib.Path('a.py'))
    assert disks.has_paths(tree, '_hidden.py')
    assert not disks.has_paths(tree, ['a.py', 'missing'])
    assert disks.has_paths(tree, ['a.py', 'missing'], match_all = False)
    assert not disks.has_paths(tree, 'sub/c.py')
    assert disks.has_paths(tree, 'sub/c.py', recursive = True)
    with pytest.raises(AttributeError):
        disks.has_paths(tree, 'missing', raise_error = True)


def test_has_file_paths(tree):
    assert disks.has_file_paths(tree, ['a.py', 'b.txt'])
    assert not disks.has_file_paths(tree, ['a.py', 'sub'])
    assert disks.has_file_paths(tree, 'sub/d.txt', recursive = True)


def test_has_folder_paths(tree):
    assert disks.has_folder_paths(tree, ['sub', 'empty'])
    assert not disks.has_folder_paths(tree, 'a.py')


def test_has_modules(tree):
    assert disks.has_modules(tree, 'a')
    assert disks.has_modules(tree, 'a.py')
    assert not disks.has_modules(tree, 'b')
    assert disks.has_modules(tree, 'sub.c', recursive = True)
    assert not disks.has_modules(tree, 'sub.c')


def test_not_a_folder(tree):
    for function in (
            disks.name_paths,
            disks.collect_file_paths,
            disks.catalog_folder_paths,
            disks.name_modules):
        with pytest.raises(NotADirectoryError):
            function(tree / 'a.py')
        with pytest.raises(NotADirectoryError):
            function(tree / 'missing')
