"""
containers: introspection tools for containers
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
    Container, Hashable, Iterable, Mapping, MutableMapping, MutableSequence, 
    Sequence, Set)
import functools
import inspect
from typing import Any, Optional, Type

from . import configuration

  
@functools.singledispatch
def has_types(
    item: object, /,
    contents: Type[Any] | tuple[Type[Any], ...]) -> bool:
    """Returns whether 'item' contains the type(s) in 'contents'.

    Args:
        item (object): item to examine.
        contents (Type[Any] | tuple[Type[Any], ...]): types to check for in 
            'item' contents.
        
    Raises:
        TypeError: if 'item' does not match any of the registered types.
        
    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    raise TypeError(f'item {item} is not supported by {__name__}')

@has_types.register(Mapping)    
def has_types_dict(
    item: Mapping[Hashable, Any], /, 
    contents: tuple[Type[Any] | tuple[Type[Any], ...],
                    Type[Any] | tuple[Type[Any], ...]]) -> bool:
    """Returns whether dict-like 'item' contains the type(s) in 'contents'.

    In 'contents', the first item in the passed tuple should be the type(s) to
    check against the keys in 'item' and the second item in the passed tuple
    should be the type(s) to check against the values in 'item'.
    
    Args:
        item (Mapping[Hashable, Any]): item to examine.
        contents (tuple[Type[Any] | tuple[Type[Any], ...], Type[Any] | 
            tuple[Type[Any], ...]]): types to check for in 'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return (
        has_types_container(item.keys(), contents = contents[0])
        and has_types_container(item.values(), contents = contents[1]))

@has_types.register(MutableSequence)   
def has_types_list(
    item: MutableSequence[Any], /,
    contents: Type[Any] | tuple[Type[Any], ...]) -> bool:
    """Returns whether list-like 'item' contains the type(s) in 'contents'.

    Args:
        item (MutableSequence[Any]): item to examine.
        contents (Type[Any] | tuple[Type[Any], ...]): types to check for in 
            'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return has_types_container(item, contents = contents)

@has_types.register(Set)   
def has_types_set(
    item: Set[Any], /,
    contents: Type[Any] | tuple[Type[Any], ...]) -> bool:
    """Returns whether set-like 'item' contains the type(s) in 'contents'.

    Args:
        item (Set[Any]): item to examine.
        contents (Type[Any] | tuple[Type[Any], ...]): types to check for in 
            'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return has_types_container(item, contents = contents)

@has_types.register(tuple)   
def has_types_tuple(
    item: tuple[Any, ...], /,
    contents: Type[Any] | tuple[Type[Any], ...]) -> bool:
    """Returns whether tuple 'item' contains the type(s) in 'contents'.

    Args:
        item (tuple[Any, ...]): item to examine.
        contents (Type[Any] | tuple[Type[Any], ...]): types to check for in 
            'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    if isinstance(contents, tuple) and len(item) == len(contents):
        technique = has_types_sequence
    else:
        technique = has_types_container
    return technique(item, contents = contents)

@has_types.register(Sequence)   
def has_types_sequence(
    item: Sequence[Any], /,
    contents: tuple[Type[Any], ...]) -> bool:
    """Returns whether sequence 'item' contains the type(s) in 'contents'.

    Args:
        item (Sequence[Any]): item to examine.
        contents (tuple[Type[Any], ...]): types to check for in 'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return all(isinstance(item[i], contents[i]) for i in enumerate(item))

@has_types.register(Container)       
def has_types_container(
    item: Container[Any], /,
    contents: Type[Any] | tuple[Type[Any], ...]) -> bool:
    """Returns whether container 'item' contains the type(s) in 'contents'.

    Args:
        item (Container[Any]): item to examine.
        contents (Type[Any] | tuple[Type[Any], ...]): types to check for in 
            'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return all(isinstance(i, contents) for i in item)
      

@functools.singledispatch
def list_types(item: object) -> Optional[
    tuple[Type[Any], ...] |
    tuple[tuple[Type[Any], ...], tuple[Type[Any], ...]]]:
    """Returns types contained in 'item'.

    Args:
        item (object): item to examine.
    
    Returns:
        Optional[Union[tuple[Type[Any], ...], tuple[tuple[Type[Any], ...], 
            tuple[Type[Any], ...]]]]:: returns the types of things contained 
            in 'item'. Returns None if 'item' is not a container.
        
    """
    raise TypeError(f'item {item} is not supported by {__name__}')

@list_types.register(Mapping)  
def list_types_dict(
    item: Mapping[Hashable, Any]) -> Optional[
        tuple[tuple[Type[Any], ...], tuple[Type[Any], ...]]]:
    """Returns types contained in 'item'.

    Args:
        item (object): item to examine.
    
    Returns:
        Optional[tuple[Type[Any], ...]]: returns the types of things contained 
            in 'item'. Returns None if 'item' is not a container.
        
    """
    if isinstance(item, Mapping):
        key_types = list_types_sequence(item.keys())
        value_types = list_types_sequence(item.values())
        return tuple(key_types, value_types)
    else:
        return None

@list_types.register(MutableSequence)  
def list_types_list(item: list[Any]) -> Optional[tuple[Type[Any], ...]]:
    """Returns types contained in 'item'.

    Args:
        item (list[Any]): item to examine.
    
    Returns:
        Optional[tuple[Type[Any], ...]]: returns the types of things contained 
            in 'item'. Returns None if 'item' is not a container.
        
    """
    if isinstance(item, list):
        key_types = list_types_sequence(item.keys())
        value_types = list_types_sequence(item.values())
        return tuple(key_types, value_types)
    else:
        return None

@list_types.register(Sequence)    
def list_types_sequence(item: Sequence[Any]) -> Optional[tuple[Type[Any], ...]]:
    """Returns types contained in 'item'.

    Args:
        item (Sequence[Any]): item to examine.
    
    Returns:
        Optional[tuple[Type[Any], ...]]: returns the types of things contained 
            in 'item'. Returns None if 'item' is not a container.
        
    """
    if isinstance(item, Sequence):
        all_types = []
        for thing in item:
            kind = type(thing)
            if not kind in all_types:
                all_types.append(kind)
        return tuple(all_types)
    else:
        return None
