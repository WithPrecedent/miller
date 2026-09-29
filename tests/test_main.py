"""Tests for the top-level miller package and the examples in its README."""

from __future__ import annotations

import dataclasses
import inspect
import pathlib
import re

import miller

README = pathlib.Path(__file__).parent.parent / 'README.md'


def test_version_matches_pyproject():
    pyproject = README.parent / 'pyproject.toml'
    match = re.search(
        r'^version = "(.+)"', pyproject.read_text(encoding = 'utf-8'), re.M)
    assert match
    assert match.group(1) == miller.__version__


def test_all_exports_exist():
    assert miller.__all__
    assert len(miller.__all__) == len(set(miller.__all__))
    for name in miller.__all__:
        item = getattr(miller, name)
        assert callable(item) or inspect.ismodule(item), name


def test_readme_prefix_suffix_grid():
    """Every prefix/suffix combination promised by the README exists."""
    grid = {
        'annotations': ('catalog', 'collect', 'has', 'name'),
        'attributes': ('catalog', 'collect', 'has', 'name'),
        'classes': ('catalog', 'collect', 'has', 'name'),
        'fields': ('catalog', 'collect', 'has', 'name'),
        'file_paths': ('catalog', 'collect', 'has', 'name'),
        'folder_paths': ('catalog', 'collect', 'has', 'name'),
        'functions': ('catalog', 'collect', 'has', 'name'),
        'methods': ('catalog', 'collect', 'has', 'name'),
        'modules': ('catalog', 'collect', 'has', 'name'),
        'paths': ('catalog', 'collect', 'has', 'name'),
        'properties': ('catalog', 'collect', 'has', 'name'),
        'signatures': ('catalog', 'collect', 'has', 'name'),
        'variables': ('catalog', 'collect', 'has', 'name')}
    for suffix, prefixes in grid.items():
        for prefix in prefixes:
            assert hasattr(miller, f'{prefix}_{suffix}'), (
                f'{prefix}_{suffix}')


def test_readme_singular_is_functions():
    for suffix in (
            'attribute', 'class', 'class_attribute', 'field', 'file_path',
            'folder_path', 'function', 'instance', 'method', 'module', 'path',
            'property', 'variable'):
        assert hasattr(miller, f'is_{suffix}'), suffix


def test_readme_universal_examples():
    """The 'Why use miller?' examples work for functions and dataclasses."""

    @dataclasses.dataclass
    class Example:
        one: int = 1
        two: str = 'two'

        @property
        def prop(self) -> int:
            return 1

    assert miller.name_functions(miller.framework) == [
        'set_include_privates',
        'set_include_str',
        'set_keyer',
        'set_match_all',
        'set_module_extensions',
        'set_raise_errors',
        'set_recursion']
    assert miller.name_properties(Example()) == ['prop']
    assert miller.name_fields(Example()) == ['one', 'two']


def test_readme_privates_parameter():
    class Example:
        def _hidden(self):
            return

        def shown(self):
            return

    assert miller.name_methods(Example) == ['shown']
    assert '_hidden' in miller.name_methods(Example, include_privates = True)
    assert 'shown' in miller.name_methods(Example, include_privates = True)


def test_readme_method_family():
    """The five `*_methods` examples in the README all work."""

    class Example:
        def one(self):
            return 1

        def two(self):
            return 2

        value = 3

    item = Example()
    assert list(miller.catalog_methods(item)) == ['one', 'two']
    assert miller.catalog_methods(item)['one']() == 1
    assert [m() for m in miller.collect_methods(item)] == [1, 2]
    assert miller.has_methods(item, ['one', 'two'])
    assert not miller.has_methods(item, ['one', 'value'])
    assert miller.is_method(item, 'one')
    assert not miller.is_method(item, 'value')
    assert miller.name_methods(item) == ['one', 'two']


def test_readme_usage_example():
    """Runs the README 'Usage' code block and checks its commented results."""
    text = README.read_text(encoding = 'utf-8')
    usage = text.split('### Usage', 1)[1].split('## Contributing', 1)[0]
    blocks = re.findall(r'``` python\n(.*?)```', usage, re.S)
    assert len(blocks) == 2
    namespace: dict = {}
    # Point the folder example at the real source folder.
    code = blocks[0].replace(
        "'src/miller'", repr(str(README.parent / 'src' / 'miller')))
    exec(code, namespace)  # noqa: S102
    miller_ = namespace['miller']
    item = namespace['item']
    for line in code.splitlines():
        if '  # ' not in line or not line.startswith('miller.'):
            continue
        call, expected = line.split('  # ', 1)
        expected = expected.strip()
        if expected.startswith(('[', '{', 'True')):
            assert eval(call.strip(), namespace) == eval(expected), line  # noqa: S307
    assert miller_.name_fields(item) == ['one']
    inspector = miller_.Inspector(item)
    assert list(inspector.methods) == ['add']
    assert inspector.variables == {'one': 1}
    assert list(inspector.fields) == ['one']
