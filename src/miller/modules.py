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
from collections.abc import Callable, MutableSequence
import inspect
import sys
import types
from typing import Any, Optional, Type

import camina

from . import base
from . import identity


def has_classes(
    item: types.ModuleType | str, 
    classes: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'classes' exist in 'item'.

    Args:
        item (types.ModuleType | str): module or its name to inspect.
        classes (MutableSequence[str]): names of classes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'classes' are not an attribute of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'classes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
                        
    Returns:
        bool: whether some or all (depending on 'match_all') of 'classes' exist 
            in 'item'.
    
    """
    item = sys.modules[item] if isinstance(item, str) else item
    return base.has_elements(
        checker = identity.is_class,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        attributes = classes)

def has_functions(
    item: types.ModuleType | str, 
    functions: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'functions' exist in 'item'.

    Args:
        item (types.ModuleType | str): module or its name to inspect.
        functions (MutableSequence[str]): names of functions to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'functions' are not an attribute of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'functions' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
                        
    Returns:
        bool: whether some or all (depending on 'match_all') of 'functions' 
            exist in 'item'.
    
    """
    item = sys.modules[item] if isinstance(item, str) else item
    return base.has_elements(
        checker = identity.is_function,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        attributes = functions)

def has_objects(
    item: types.ModuleType | str, 
    objects: MutableSequence[str], 
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'objects' exist in 'item'.

    Args:
        item (types.ModuleType | str): module or its name to inspect.
        objects (MutableSequence[str]): names of objects to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'objects' are not an attribute of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'objects' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
                        
    Returns:
        bool: whether some or all (depending on 'match_all') of 'objects' exist 
            in 'item'.
    
    """
    item = sys.modules[item] if isinstance(item, str) else item
    return base.has_elements(
        checker = identity.is_object,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        attributes = objects)
   
def list_classes(
    item: types.ModuleType | str, 
    raise_error: Optional[bool] = None,
    include_private: bool = False) -> list[Type[Any]]:
    """Returns list of classes in 'item'.
    
    Args:
        item (types.ModuleType | str): module or its name to inspect.
        include_private (bool): whether to include items that begin with '_'
            (True) or to exclude them (False). Defauls to False.
        
    Returns:
        list[Type[Any]]: list of classes in 'item'.
        
    """
    kwargs = dict(item = item, include_private = include_private)
    return list(map_classes(**kwargs).values())
              
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
    kwargs = dict(item = item, include_private = include_private)
    return list(map_functions(**kwargs).values())
      
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
    kwargs = dict(item = item, include_private = include_private)
    return list(map_objects(**kwargs).values())
   
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
    return _get_object_mapping(
        item = item, 
        predicate = inspect.isclass, 
        include_private = include_private)
   
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
    return _get_object_mapping(
        item = item, 
        predicate = inspect.isfunction, 
        include_private = include_private)
   
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
    return _get_object_mapping(
        item = item, 
        predicate = None, 
        include_private = include_private)  

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
    kwargs = dict(item = item, include_private = include_private)
    return list(map_classes(**kwargs).keys())
 
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
    kwargs = dict(item = item, include_private = include_private)
    return list(map_functions(**kwargs).keys())

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
    kwargs = dict(item = item, include_private = include_private)
    return list(map_objects(**kwargs).keys())


""" Private Functions """

def _check_trait(
    item: Any,
    attributes: MutableSequence[Any],
    raise_error: bool,
    match_all: bool,
    checker: Callable) -> bool:
    """Returns whether 'attributes' exist in 'item'.

    Args:
        item (object | Type[Any]): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not an attribute of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
        checker (Callable): function to call to determine if an attribute in
            'attributes' qualifies as the desired type.
            
    Raises:
        AttributeError: if some 'attributes' are not an attribute of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether all 'attributes' exist in 'item'.
    
    """
    match_all = configuration.MATCH_ALL if None else match_all 
    scope = all if match_all else any
    kwargs = dict(raise_error = False)
    check = scope(checker(item, a, **kwargs) for a in attributes)  
    if not check and raise_error:
        raise AttributeError(
            f'Some of {attributes} are not attributes of {item}')
    elif not check:
        return False
    else:
        return True

def _get_object_mapping(
    item: types.ModuleType | str, 
    predicate: Optional[Callable] = None,
    include_private: bool = False) -> dict[str, Type[Any]]:
    """_summary_

    Args:
        item (types.ModuleType | str): _description_
        predicate (Callable): _description_
        include_private (bool, optional): _description_. Defaults to False.

    Returns:
        dict[str, Type[Any]]: _description_
        
    """
    if isinstance(item, str):
        item = sys.modules[item]
    if predicate is None:
        objects = {
            m[0]: m[1] for m in inspect.getmembers(item)
            if m[1].__module__ == item.__name__}
    else:
        objects = {
            m[0]: m[1] for m in inspect.getmembers(item, predicate)
            if m[1].__module__ == item.__name__}        
    if not include_private:
        objects = camina.drop_privates(objects)
    return objects