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
    def get_something(self) -> str:
        return 'something'
    
    def do_something(self) -> None:
        return
    
    
class TestClass(object):
    
    a_classvar: str = 'tree'
    
    def __init__(self) -> None:
        a_dict = {'tree': 'house'}

    @property
    def get_something(self) -> str:
        return 'something'
    
    def do_something(self) -> None:
        return
   
    
def test_all() -> None:
    a_folder = pathlib.Path('.') / 'tests' / 'dummy_folder'
    a_file = pathlib.Path(a_folder) / 'dummy_module.py'
    assert miller.is_folder(item = a_folder)
    assert miller.is_module(item = a_file)
    assert miller.name_modules(item = a_folder) == ['dummy_module']
    all_modules = miller.get_modules(item = a_folder)
    a_module = all_modules[0]
    assert type(a_module) == types.ModuleType
    assert a_module.__name__ == 'dummy_module'
    class_names = miller.name_classes(item = a_module)
    assert class_names == ['DummyClass', 'DummyDataclass']
    function_names = miller.name_functions(item = a_module)
    assert function_names == ['dummy_function']
    classes = miller.get_classes(item = a_module)
    assert inspect.isclass(classes[0])
    functions = miller.get_functions(item = a_module)
    assert type(functions[0]) == types.FunctionType
    a_class = TestClass()
    a_dataclass = TestDataclass()
    assert miller.is_class_attribute(item = a_class, attribute = 'a_classvar')
    assert miller.is_class_attribute(
        item = a_dataclass, 
        attribute = 'a_classvar')   
    assert not miller.is_class_attribute(item = a_class, attribute = 'a_dict')
    assert not miller.is_class_attribute(
        item = a_dataclass, 
        attribute = 'a_dict')    
    assert miller.is_method(item = a_class, attribute = 'do_something')
    assert miller.is_method(
        item = a_dataclass, 
        attribute = 'do_something')
    assert miller.is_property(
        item = a_class, 
        attribute = 'get_something')
    assert miller.is_property(
        item = a_dataclass, 
        attribute = 'get_something')
    properties = miller.get_properties(item = a_class)
    assert properties == {'get_something': 'something'}
    methods = miller.get_methods(item = a_dataclass) 
    assert isinstance(methods[0], types.MethodType)
    attributes = miller.name_fields(item = TestDataclass)
    assert attributes == ['a_dict', 'a_list']
    return

if __name__ == '__main__':
    test_all()

