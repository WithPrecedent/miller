"""Shared fixtures for miller's unit tests."""

from __future__ import annotations

import dataclasses
import importlib.util
import pathlib
import types

import pytest

import miller

DUMMY_FOLDER = pathlib.Path(__file__).parent / 'dummy_folder'


@pytest.fixture(autouse = True)
def restore_configuration():
    """Restores all global settings after every test."""
    names = [n for n in dir(miller.configuration) if n.isupper()]
    saved = {n: getattr(miller.configuration, n) for n in names}
    yield
    for name, value in saved.items():
        setattr(miller.configuration, name, value)


@pytest.fixture
def dummy_module() -> types.ModuleType:
    """Returns the module in `dummy_folder`."""
    path = DUMMY_FOLDER / 'dummy_module.py'
    spec = importlib.util.spec_from_file_location('dummy_module', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Parent:
    """Class used to test attribute introspection."""

    class_variable: int = 1
    _private_variable: int = 2

    def __init__(self) -> None:
        self.instance_variable = 3
        self._private_instance = 4

    def method(self, value: int) -> int:
        return value

    def _private_method(self) -> None:
        return

    @classmethod
    def class_method(cls) -> None:
        return

    @staticmethod
    def static_method() -> None:
        return

    @property
    def prop(self) -> int:
        return 5

    @property
    def broken_prop(self) -> int:
        raise RuntimeError('broken')


class Child(Parent):
    """Subclass of `Parent`."""

    child_variable: str = 'child'


class Slotted:
    """Class with slots."""

    __slots__ = ('a', 'b')

    def __init__(self) -> None:
        self.a = 1


@dataclasses.dataclass
class Data:
    """Dataclass used to test field introspection."""

    x: int = 1
    y: str = 'y'
    _z: float = 0.5

    def total(self) -> int:
        return self.x


@pytest.fixture
def parent() -> Parent:
    return Parent()


@pytest.fixture
def child() -> Child:
    return Child()


@pytest.fixture
def data() -> Data:
    return Data()


@pytest.fixture
def tree(tmp_path: pathlib.Path) -> pathlib.Path:
    """Returns a folder tree for testing disk introspection.

    root/
        a.py
        b.txt
        _hidden.py
        sub/
            c.py
            d.txt
            __init__.py
        __pycache__/
            a.cpython.pyc
        empty/
    """
    (tmp_path / 'a.py').write_text('x = 1\n')
    (tmp_path / 'b.txt').write_text('b')
    (tmp_path / '_hidden.py').write_text('')
    (tmp_path / 'sub').mkdir()
    (tmp_path / 'sub' / 'c.py').write_text('')
    (tmp_path / 'sub' / 'd.txt').write_text('')
    (tmp_path / 'sub' / '__init__.py').write_text('')
    (tmp_path / '__pycache__').mkdir()
    (tmp_path / '__pycache__' / 'a.cpython.pyc').write_bytes(b'')
    (tmp_path / 'empty').mkdir()
    return tmp_path
