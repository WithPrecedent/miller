"""
modules: introspection tools for Python modules
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

Contents:
  

        
ToDo:
    Add support for Kinds once that system is complete.

"""
from __future__ import annotations
from collections.abc import (
    Container, Hashable, Iterable, Mapping, MutableSequence, Sequence, Set)
import dataclasses
import functools
import inspect
import pathlib
import sys
import types
from typing import Any, Optional, Type

import camina
import nagata

    
def list_annotations(
    item: object | types.ModuleType, 
    include_private: bool = False) -> list[Any]:
    """Returns list of type annotations.
    
    Args:
        item (object): instance to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        list[Any]: list of annotations of 'item'.
            
    """
    return list(map_annotations(
        item = item, 
        include_private = include_private).values())
       
def list_classes(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[Type[Any]]:
    """Returns list of classes in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        list[Type[Any]]: list of classes in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    classes = [
        m[1] for m in inspect.getmembers(item, inspect.isclass)
        if m[1].__module__ == item.__label.name__]
    if not include_private:
        classes = camina.drop_privates(classes)
    return classes
              
def list_functions(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[types.FunctionType]:
    """Returns list of functions in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        list[Type[types.FunctionType]]: list of functions in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    functions = [
        m[1] for m in inspect.getmembers(item, inspect.isfunction)
        if m[1].__module__ == item.__label.name__]
    if not include_private:
        functions = camina.drop_privates(functions)
    return functions 
  
def name_classes(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[str]:
    """Returns list of string names of classes in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        list[Type[types.FunctionType]]: list of functions in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    names = [    
        m[0] for m in inspect.getmembers(item, inspect.isclass)
        if m[1].__module__ == item.__name__]
    if not include_private:
        names = camina.drop_privates(names)
    return names
 
def name_functions(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[str]:
    """Returns list of string names of functions in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        list[Type[types.FunctionType]]: list of functions in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    names = [
        m[0] for m in inspect.getmembers(item, inspect.isfunction)
        if m[1].__module__ == item.__name__]
    if not include_private:
        names = camina.drop_privates(names)
    return names

def name_variables(
    item: object | Type[Any], 
    include_private: bool = False) -> list[str]:
    """Returns variable names of 'item'.
    
    Args:
        item (object | Type[Any]): item to examine.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
                        
    Returns:
        list[str]: names of attributes in 'item' that are neither methods nor
            properties.
            
    """
    names = [
        a for a in dir(item) 
        if identify.is_variable(item, attribute = a)]
    if not include_private:
        names = camina.drop_privates(names)
    return names
 