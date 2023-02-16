"""
test_miller: tests functions and classes in the miller packae
Corey Rayburn Yung <coreyrayburnyung@gmail.com>
Copyright 2020-2022, Corey Rayburn Yung
License: Apache-2.0

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

ToDo:
    
    
"""
from __future__ import annotations
import dataclasses
import inspect
import pathlib
import types
from typing import Any, ClassVar

import miller


@dataclasses.dataclass
class TestDataclass(object):
    
    a_dict: dict[Any, Any] = dataclasses.field(default_factory = dict)
    a_list: list[Any] = dataclasses.field(default_factory = list)
    a_classvar: ClassVar[Any] = None     

    @property
    def list_something(self) -> str:
        return 'something'
    
    def do_something(self) -> None:
        return
    
    
class TestClass(object):
    
    a_classvar: str = 'tree'
    
    def __init__(self) -> None:
        a_dict = {'tree': 'house'}

    @property
    def list_something(self) -> str:
        return 'something'
    
    def do_something(self) -> None:
        return
   
    
def test_attributes() -> None:
    an_instance = TestClass()
    a_dataclass = TestDataclass()
    assert miller.is_class_attribute(an_instance, attribute = 'a_classvar')
    assert miller.is_class_attribute(
        a_dataclass, 
        attribute = 'a_classvar')   
    assert not miller.is_class_attribute(an_instance, attribute = 'a_dict')
    # assert not miller.is_class_attribute(
    #     a_dataclass, 
    #     attribute = 'a_dict')    
    assert miller.is_method(an_instance, attribute = 'do_something')
    assert miller.is_method(
        a_dataclass, 
        attribute = 'do_something')
    # assert miller.is_property(
    #     an_instance, 
    #     attribute = 'list_something')
    # assert miller.is_property(
    #     a_dataclass, 
    #     attribute = 'list_something')
    # properties = miller.list_properties(an_instance)
    # assert properties == {'list_something': 'something'}
    methods = miller.list_methods(a_dataclass) 
    assert isinstance(methods[0], types.MethodType)
    attributes = miller.name_fields(TestDataclass)
    assert attributes == ['a_dict', 'a_list']
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
    # test_modules()
    # test_attributes()
