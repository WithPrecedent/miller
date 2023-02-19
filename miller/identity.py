"""
identity: introspection tools that return a bool whether an item is a type
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
    is_class:
    is_class_attribute:
    is_container:
    is_dict:
    is_file:
    is_folder:
    is_function:
    is_iterable:
    is_list:
    is_method:
    is_module:
    is_nested (dispatcher):
        is_nested_dict:
        is_nested_list:
        is_nested_set:
        is_nested_tuple:
    is_object:
    is_path:
    is_property:
    is_sequence:
    is_set:
    is_variable:
   
ToDo:
    

"""
from __future__ import annotations
from collections.abc import (
    Container, Hashable, Iterable, Mapping, MutableMapping, MutableSequence, 
    Sequence, Set)
import functools
import inspect
import pathlib
import types
from typing import Any, Optional, Type

import camina

from . import configuration

     
def is_class(item: Any) -> bool:
    """Returns if 'item' is a class (and not an instance).
    
    Args:
        item (Any): object to examine.
        
    Returns:
        bool: if 'item' is a class (and not an instance).
        
    """  
    return inspect.isclass(item)
 
def is_container(item: Any, include_str: bool = False) -> bool:
    """Returns if 'item' is a container.
    
    If 'exclude_str' is True (the default) and 'item' is a str, False will be
    returned.
    
    Args:
        item (Any): object to examine.
        include_str (bool): whether to return True if 'item' is a str.
                    
    Returns:
        bool: if 'item' is a container.
        
    """  
    if not inspect.isclass(item):
        item = item.__class__
    return (
        issubclass(item, Container)
        and (not issubclass(item, str) or include_str))

def is_dict(item: Any) -> bool:
    """Returns if 'item' is a mutable mapping (generic dict type).
    
    Args:
        item (Any): object to examine.
        
    Returns:
        bool: if 'item' is a mutable mapping.
        
    """  
    if not inspect.isclass(item):
        item = item.__class__
    return isinstance(item, MutableMapping) 
  
def is_file(item: str | pathlib.Path) -> bool:
    """Returns whether 'item' is a file.
    
    Args:
        item (str | pathlib.Path): path to check.
        
    Returns:
        bool: whether 'item' is a file.
        
    """ 
    item = camina.pathlibify(item)
    return item.exists() and item.is_file()

def is_folder(item: str | pathlib.Path) -> bool:
    """Returns whether 'item' is a path to a folder.
    
    Args:
        item (str | pathlib.Path): path to check.
        
    Returns:
        bool: whether 'item' is a path to a folder.
        
    """ 
    item = camina.pathlibify(item)
    return item.exists() and item.is_dir()
 
def is_function(item: Any) -> bool:
    """Returns if 'item' is a function.
    
    Args:
        item (Any): object to examine.
        
    Returns:
        bool: if 'item' is a function.
        
    """  
    return isinstance(item, types.FunctionType)
        
def is_instance(item: Any) -> bool:
    """Returns if 'item' is an instance (and not a class).
    
    To rule out edge cases, this function checks that 'item' is not a class and
    has the attribute '__class__'.
    
    Args:
        item (Any): object to examine.
        
    Returns:
        bool: if 'item' is an instance (and not a class).
        
    """  
    return hasattr(item, '__class__') and not is_class(item)

def is_iterable(item: Any, include_str: bool = False) -> bool:
    """Returns if 'item' is iterable.
    
    If 'exclude_str' is True (the default) and 'item' is a str, False will be
    returned.
        
    Args:
        item (Any): object to examine.
        include_str (bool): whether to return True if 'item' is a str.
        
    Returns:
        bool: if 'item' is iterable.
        
    """ 
    if not inspect.isclass(item):
        item = item.__class__
    return (
        issubclass(item, Iterable) 
        and (not issubclass(item, str) or include_str))

def is_list(item: Any) -> bool:
    """Returns if 'item' is a mutable sequence (generic list type).
    
    Args:
        item (Any): object to examine.
        
    Returns:
        bool: if 'item' is a mutable list.
        
    """
    if not inspect.isclass(item):
        item = item.__class__
    return isinstance(item, MutableSequence)
   
def is_module(item: str | pathlib.Path) -> bool:
    """Returns whether 'item' is a python-module file.
    
    Args:
        item (str | pathlib.Path): path to check.
        
    Returns:
        bool: whether 'item' is a python-module file.
        
    """  
    item = camina.pathlibify(item)
    return (
        item.exists() 
        and item.is_file() 
        and item.suffix in configuration.MODULE_EXTENSIONS)
  
@functools.singledispatch
def is_nested(item: object, /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (object): instance to examine.
        
    Raises:
        TypeError: if 'item' does not match any of the registered types.
        
    Returns:
        bool: if 'item' is a nested mapping.
        
    """ 
    raise TypeError(f'item {item} is not supported by {__name__}')

@is_nested.register(Mapping)   
def is_nested_dict(item: Mapping[Any, Any], /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (Mapping[Any, Any]): object to examine.
        
    Returns:
        bool: if 'item' is a nested mapping.
        
    """ 
    return (
        isinstance(item, Mapping) 
        and any(isinstance(v, Mapping) for v in item.values()))

@is_nested.register(MutableSequence)     
def is_nested_list(item: MutableSequence[Any], /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (MutableSequence[Any]): object to examine.
        
    Returns:
        bool: if 'item' is a nested sequence.
        
    """ 
    return is_sequence(item)and any(is_sequence(item = v) for v in item)

@is_nested.register(Set)         
def is_nested_set(item: Set[Any], /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (item: Set[Any]): object to examine.
        
    Returns:
        bool: if 'item' is a nested set.
        
    """ 
    return is_set(item) and any(is_set(item = v) for v in item)

@is_nested.register(tuple)     
def is_nested_tuple(item: tuple[Any, ...], /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (tuple[Any, ...]): object to examine.
        
    Returns:
        bool: if 'item' is a nested sequence.
        
    """ 
    return is_sequence(item) and any(is_sequence(item = v) for v in item)

def is_object(item: Any) -> bool:
    """Returns if 'item' is an object (and not a class or function).

    Args:
        item (Any): object to examine.

    Returns:
        bool: whether 'item' is an object (and not a class or function).
        
    """ 
    return not is_function(item) and not is_class(item)
  
def is_path(item: str | pathlib.Path) -> bool:
    """Returns whether 'item' is a currently existing path.
    
    Args:
        item (str | pathlib.Path): path to check.
        
    Returns:
        bool: whether 'item' is a currently existing path.
        
    """ 
    item = camina.pathlibify(item)
    return item.exists()
  
def is_sequence(item: Any, include_str: bool = False) -> bool:
    """Returns if 'item' is a sequence.
    
    If 'exclude_str' is True (the default) and 'item' is a str, False will be
    returned.
        
    Args:
        item (Any): object to examine.
        include_str (bool): whether to return True if 'item' is a str.
                    
    Returns:
        bool: if 'item' is a sequence.
        
    """ 
    if not inspect.isclass(item):
        item = item.__class__
    return (
        issubclass(item, Sequence)
        and (not issubclass(item, str) or include_str))
        
def is_set(item: Any) -> bool:
    """Returns if 'item' is a Set (generic type set).
    
    Args:
        item (Any): object to examine.
        
    Returns:
        bool: if 'item' is a set.
        
    """ 
    if not inspect.isclass(item):
        item = item.__class__
    return issubclass(item, Set)
 