"""
containers: inspects containers
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
       
       
"""
from __future__ import annotations
from collections.abc import (
    Collection, Container, Hashable, Iterable, Mapping, MutableMapping, 
    MutableSequence, Sequence, Set)
import functools
import inspect
import pathlib
import types
from typing import Any, Optional, Type, Union

import camina

from . import objects


@functools.singledispatch
def get_types(item: object) -> Optional[Union[
    tuple[Type[Any], ...], 
    tuple[tuple[Type[Any], ...], tuple[Type[Any], ...]]]]:
    """Returns types contained in 'item'.

    Args:
        item (object): item to examine.
    
    Returns:
        Optional[Union[tuple[Type[Any], ...], tuple[tuple[Type[Any], ...], 
            tuple[Type[Any], ...]]]]:: returns the types of things contained 
            in 'item'. Returns None if 'item' is not a container.
        
    """
    raise TypeError(f'item {item} is not supported by {__name__}')

@get_types.register(Mapping)  
def get_types_dict(
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
        key_types = get_types_sequence(item = item.keys())
        value_types = get_types_sequence(item = item.values())
        return tuple([key_types, value_types])
    else:
        return None

@get_types.register(MutableSequence)  
def get_types_list(item: list[Any]) -> Optional[tuple[Type[Any], ...]]:
    """Returns types contained in 'item'.

    Args:
        item (list[Any]): item to examine.
    
    Returns:
        Optional[tuple[Type[Any], ...]]: returns the types of things contained 
            in 'item'. Returns None if 'item' is not a container.
        
    """
    if isinstance(item, list):
        key_types = get_types_sequence(item = item.keys())
        value_types = get_types_sequence(item = item.values())
        return tuple([key_types, value_types])
    else:
        return None

@get_types.register(Sequence)    
def get_types_sequence(item: Sequence[Any]) -> Optional[tuple[Type[Any], ...]]:
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
  
@functools.singledispatch
def has_contents(
    item: object, /,
    contents: Union[Type[Any], tuple[Type[Any], ...]]) -> bool:
    """Returns whether 'item' contains the type(s) in 'contents'.

    Args:
        item (object): item to examine.
        contents (Union[Type[Any], tuple[Type[Any], ...]]): types to check for
            in 'item' contents.
        
    Raises:
        TypeError: if 'item' does not match any of the registered types.
        
    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    raise TypeError(f'item {item} is not supported by {__name__}')

@has_contents.register(Mapping)    
def has_contents_dict(
    item: Mapping[Hashable, Any], /, 
    contents: tuple[Union[Type[Any], tuple[Type[Any], ...]],
                    Union[Type[Any], tuple[Type[Any], ...]]]) -> bool:
    """Returns whether dict 'item' contains the type(s) in 'contents'.

    Args:
        item (Mapping[Hashable, Any]): item to examine.
        contents (Union[Type[Any], tuple[Type[Any], ...]]): types to check for
            in 'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return (
        has_contents_serial(item = item.keys(), contents = contents[0])
        and has_contents_serial(item = item.values(), contents = contents[1]))

@has_contents.register(MutableSequence)   
def has_contents_list(
    item: MutableSequence[Any], /,
    contents: Union[Type[Any], tuple[Type[Any], ...]]) -> bool:
    """Returns whether list 'item' contains the type(s) in 'contents'.

    Args:
        item (MutableSequence[Any]): item to examine.
        contents (Union[Type[Any], tuple[Type[Any], ...]]): types to check for
            in 'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return has_contents_serial(item = item, contents = contents)

@has_contents.register(Set)   
def has_contents_set(
    item: Set[Any], /,
    contents: Union[Type[Any], tuple[Type[Any], ...]]) -> bool:
    """Returns whether list 'item' contains the type(s) in 'contents'.

    Args:
        item (Set[Any]): item to examine.
        contents (Union[Type[Any], tuple[Type[Any], ...]]): types to check for
            in 'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return has_contents_serial(item = item, contents = contents)

@has_contents.register(tuple)   
def has_contents_tuple(
    item: tuple[Any, ...], /,
    contents: Union[Type[Any], tuple[Type[Any], ...]]) -> bool:
    """Returns whether tuple 'item' contains the type(s) in 'contents'.

    Args:
        item (tuple[Any, ...]): item to examine.
        contents (Union[Type[Any], tuple[Type[Any], ...]]): types to check for
            in 'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    if isinstance(contents, tuple) and len(item) == len(contents):
        technique = has_contents_parallel
    else:
        technique = has_contents_serial
    return technique(item = item, contents = contents)

@has_contents.register(Sequence)   
def has_contents_parallel(
    item: Sequence[Any], /,
    contents: tuple[Type[Any], ...]) -> bool:
    """Returns whether parallel 'item' contains the type(s) in 'contents'.

    Args:
        item (Sequence[Any]): item to examine.
        contents (Union[Type[Any], tuple[Type[Any], ...]]): types to check for
            in 'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return all(isinstance(item[i], contents[i]) for i in enumerate(item))

@has_contents.register(Container)       
def has_contents_serial(
    item: Container[Any], /,
    contents: Union[Type[Any], tuple[Type[Any], ...]]) -> bool:
    """Returns whether serial 'item' contains the type(s) in 'contents'.

    Args:
        item (Container[Any]): item to examine.
        contents (Union[Type[Any], tuple[Type[Any], ...]]): types to check for
            in 'item' contents.

    Returns:
        bool: whether 'item' holds the types in 'contents'.
        
    """
    return all(isinstance(i, contents) for i in item)

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
        item (Mapping[Any, Any]): class or instance to examine.
        
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
        item (MutableSequence[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a nested sequence.
        
    """ 
    return (
        objects.is_sequence(item = item)
        and any(objects.is_sequence(item = v) for v in item))

@is_nested.register(Set)         
def is_nested_set(item: Set[Any], /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (item: Set[Any]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a nested set.
        
    """ 
    return (
        objects.is_set(item = item)
        and any(objects.is_set(item = v) for v in item))

@is_nested.register(tuple)     
def is_nested_tuple(item: tuple[Any, ...], /) -> bool:
    """Returns if 'item' is nested at least one-level.
    
    Args:
        item (tuple[Any, ...]): class or instance to examine.
        
    Returns:
        bool: if 'item' is a nested sequence.
        
    """ 
    return (
        objects.is_sequence(item = item)
        and any(objects.is_sequence(item = v) for v in item))
    