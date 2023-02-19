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
    has_classes:
    has_functions:
    has_objects:
    list_classes:
    list_functions:
    list_objects:
    map_classes:
    map_functions:
    map_objects:
    name_classes:
    name_functions:
    name_objects:  
      
ToDo:


"""
from __future__ import annotations
from collections.abc import MutableSequence
import inspect
import sys
import types
from typing import Any, Type

import camina


def has_classes(
    item: types.ModuleType | str, 
    classes: MutableSequence[str]) -> bool:
    """Returns whether 'classes' exist in 'item'.

    Args:
        item (types.ModuleType | str): module or its name to inspect.
        classes (MutableSequence[str]): names of classes to check to see if they
            exist in 'item'.
            
    Returns:
        bool: whether all 'classes' exist in 'item'.
    
    """
    if isinstance(item, str):
        item = sys.modules[item]
    module_classes = list_classes(item = item, include_private = True)
    return all(c in module_classes for c in classes)

def has_functions(
    item: types.ModuleType | str, 
    functions: MutableSequence[str]) -> bool:
    """Returns whether 'functions' exist in 'item'.

    Args:
        item (types.ModuleType | str): module or its name to inspect.
        functions (MutableSequence[str]): names of functions to check to see if 
            they exist in 'item'.
            
    Returns:
        bool: whether all 'functions' exist in 'item'.
    
    """
    if isinstance(item, str):
        item = sys.modules[item]
    module_functions = list_functions(item = item, include_private = True)
    return all(c in module_functions for c in functions)

def has_objects(
    item: types.ModuleType | str, 
    objects: MutableSequence[str]) -> bool:
    """Returns whether 'objects' exist in 'item'.

    Args:
        item (types.ModuleType | str): module or its name to inspect.
        objects (MutableSequence[str]): names of objects to check to see if 
            they exist in 'item'.
            
    Returns:
        bool: whether all 'objects' exist in 'item'.
    
    """
    if isinstance(item, str):
        item = sys.modules[item]
    module_objects = list_objects(item = item, include_private = True)
    return all(c in module_objects for c in objects)
   
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
        if m[1].__module__ == item.__name__]
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
        list[types.FunctionType]: list of functions in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    functions = [
        m[1] for m in inspect.getmembers(item, inspect.isfunction)
        if m[1].__module__ == item.__name__]
    if not include_private:
        functions = camina.drop_privates(functions)
    return functions 
      
def list_objects(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[Any]:
    """Returns list of objects in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        Any: list of objects in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    all_items = [
        m[1] for m in inspect.getmembers()
        if m[1].__module__ == item.__name__]
    classes = list_classes(item, include_private = include_private)
    functions = list_functions(item, include_private = include_private)
    objects = [i for i in all_items if i not in classes]
    return [i for i in objects if i not in functions]
   
def map_classes(
    item: types.ModuleType | str, 
    include_private: bool = False) -> dict[str, Type[Any]]:
    """Returns dict of classes in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        dict[str, Type[Any]]: dict with keys being class names and values
            being classes. 
        
    """
    kwargs = dict(item = item, include_private = include_private)
    names = name_classes(**kwargs)
    classes = list_classes(**kwargs)
    return dict(zip(names, classes))
   
def map_functions(
    item: types.ModuleType | str, 
    include_private: bool = False) -> dict[str, Type[Any]]:
    """Returns dict of functions in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        dict[str, Type[Any]]: dict with keys being function names and values
            being functions. 
        
    """
    kwargs = dict(item = item, include_private = include_private)
    names = name_functions(**kwargs)
    functions = list_functions(**kwargs)
    return dict(zip(names, functions))
   
def map_objects(
    item: types.ModuleType | str, 
    include_private: bool = False) -> dict[str, Type[Any]]:
    """Returns dict of objects in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        dict[str, Type[Any]]: dict with keys being object names and values
            being objects. 
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    objects = {
        m[0]: m[1] for m in inspect.getmembers()
        if m[1].__module__ == item.__name__}
    if not include_private:
        objects = camina.drop_privates(objects)
    return objects
    # kwargs = dict(item = item, include_private = include_private)
    # names = name_objects(**kwargs)
    # objects = list_objects(**kwargs)
    # return dict(zip(names, objects))   

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

def name_objects(
    item: types.ModuleType | str, 
    include_private: bool = False) -> list[Any]:
    """Returns list of names of objects in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        Any: list of names of objects in 'item'.
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    all_items = [
        m[0] for m in inspect.getmembers()
        if m[1].__module__ == item.__name__]
    classes = name_classes(item, include_private = include_private)
    functions = name_functions(item, include_private = include_private)
    objects = [i for i in all_items if i not in classes]
    return [i for i in objects if i not in functions]
 