"""Main file for unit tests."""

from __future__ import annotations
import dataclasses
import inspect
import pathlib
import types
from typing import Any, ClassVar

import miller

    
class TestClass(object):
    
    a_classvar: str = 'tree'
    
    def __init__(self) -> None:
        self.a_dict = {'tree': 'house'}
        self.a_list = []
        return

    @property
    def list_something(self) -> str:
        return 'something'
    
    def do_something(self) -> None:
        return

    @classmethod
    def do_something_with_class(cls) -> None:
        pass
   
   
@dataclasses.dataclass
class TestDataclass(object):
    
    a_dict: dict[Any, Any] = dataclasses.field(default_factory = dict)
    a_list: list[Any] = dataclasses.field(default_factory = list)
    a_classvar: ClassVar[str] = 'tree'     

    @property
    def list_something(self) -> str:
        return 'something'
    
    def do_something(self) -> None:
        return

    @classmethod
    def do_something_with_class(cls) -> None:
        pass
           
    
def test_attributes() -> None:
    an_instance = TestClass()
    a_dataclass = TestDataclass()
    for instance in [an_instance, a_dataclass]:
        assert miller.is_attribute(
            instance, 
            'a_dict',
            raise_error = False)  
        assert miller.is_instance_attribute(
            instance, 
            'a_dict',
            raise_error = False)  
        assert miller.is_instance_attribute(
            instance, 
            'a_list',
            raise_error = False)  
        assert miller.is_class_attribute(
            instance, 
            'a_classvar',
            raise_error = False)
        assert not miller.is_class_attribute(
            instance, 
            'a_dict',
            raise_error = False) 
        assert miller.is_variable(
            instance, 
            'a_dict',
            raise_error = False)
        assert miller.is_instance_variable(
            instance, 
            'a_dict',
            raise_error = False)     
        assert not miller.is_class_variable(
            instance, 
            'a_dict',
            raise_error = False)    
        assert miller.is_method(
            instance, 
            'do_something',
            raise_error = False)
        assert miller.is_instance_method(
            instance, 
            'do_something',
            raise_error = False)  
        assert miller.is_class_method(
            instance, 
            'do_something_with_class',
            raise_error = False)
        assert miller.is_property(
            instance, 
            attribute = 'list_something',
            raise_error = False)
        # properties = miller.list_properties(instance)
        # assert properties == {'list_something': 'something'}
        # methods = miller.list_methods(instance) 
        # assert isinstance(methods[0], types.MethodType)
        # attributes = miller.name_fields(TestDataclass)
        # assert attributes == ['a_dict', 'a_list']
    return

def test_modules() -> None:
    a_folder = pathlib.Path('.') / 'tests' / 'dummy_folder'
    all_modules = miller.list_modules(a_folder, import_modules = True)
    a_module = all_modules[0]
    class_names = miller.name_classes(a_module)
    assert class_names == ['DummyClass', 'DummyDataclass']
    function_names = miller.name_functions(a_module)
    assert function_names == ['dummy_function']
    classes = miller.list_classes(a_module)
    assert inspect.isclass(classes[0])
    functions = miller.list_functions(a_module)
    assert type(functions[0]) == types.FunctionType
    return

def test_paths() -> None:
    a_folder = pathlib.Path('.') / 'tests' / 'dummy_folder'
    a_file = pathlib.Path(a_folder) / 'dummy_module.py'
    assert miller.is_folder(a_folder)
    assert miller.is_module(a_file)
    assert miller.name_modules(a_folder) == ['dummy_module']
    all_modules = miller.list_modules(a_folder, import_modules = True)
    a_module = all_modules[0]
    assert type(a_module) == types.ModuleType
    assert a_module.__name__ == 'dummy_module'
    return

if __name__ == '__main__':
    test_paths()
    test_modules()
    test_attributes()
