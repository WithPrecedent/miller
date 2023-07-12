"""
base: generic introspection functions
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
from collections.abc import Callable, MutableMapping, MutableSequence
from typing import Any, Optional, Type

from . import configuration


def has_elements(
    item: Any,
    attributes: MutableSequence[str],
    checker: Callable[[Any, Any, bool], bool],
    raise_error: Optional[bool] = None,
    match_all: Optional[bool] = None) -> bool:
    """Returns whether 'item' has 'elements' or an error.

    Args:
        item (Any): class or instance to examine.
        attributes (MutableSequence[str]): names of attributes to check.
        checker (Callable[[Any, Any, bool], bool]): function to call to 
            determine if an attribute in 'attributes' qualifies as the 
            appropriate type.
        raise_error (Optional[bool]): whether to raise an error if any 
            'attributes' are not attributes of 'item' (True) or to simply 
            return False in such situations. Defaults to None, which means the 
            global 'miller.RAISE_ERRORS' setting will be used.
        match_all (Optional[bool]): whether all items in 'attributes' must match
            (True) or any of the items must match (False). Defaults to None,
            which means the global 'miller.MATCH_ALL' will be used.
 
    Raises:
        AttributeError: if 'attributes' are not attributes of 'item' and 
            'raise_error' is True (or if it is None and the global setting is
            True).
                                 
    Returns:
        bool: whether some or all (depending on 'match_all') of 'attributes' 
            exist in 'item' and are the appropriate type.
    
    """
    raise_error = configuration.RAISE_ERRORS if None else raise_error
    match_all = configuration.MATCH_ALL if None else match_all 
    scope = all if match_all else any
    kwargs = dict(raise_error = False)
    value = scope(checker(item, a, **kwargs) for a in attributes)  
    return report_has(
        value = value,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        attributes = attributes)

def is_kind(
    item: Any,
    checker: Callable[[Any, Type[Any]], bool] | Callable[[Any], bool],
    raise_error: Optional[bool] = None,
    kind: Optional[Type[Any] | str] = None) -> bool:
    """Returns whether 'item' is 'kind' or an error.

    Args:
        item (Any): class or instance to examine.
        checker (Callable[[Any, Type[Any]], bool] | Callable[[Any], bool],): 
            function to call to determine if 'item' is the appropriate type.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
        kind (Type[Any]): type to check if 'item' is.
            
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                                 
    Returns:
        bool: whether 'item' is a 'kind'.
    
    """
    raise_error = configuration.RAISE_ERRORS if None else raise_error
    value = checker(item) if kind is None else checker(item, kind)  
    return report_is(
        value = value,
        raise_error = raise_error,
        item = item,
        kind = kind) 

def is_kind_class(
    item: Any,
    checker: Callable[[Any, Type[Any]], bool] | Callable[[Any], bool],
    raise_error: bool,
    kind: Type[Any]) -> bool:
    """Returns whether 'item' is 'kind' or an error.

    Args:
        checker (Callable[[Any, Type[Any]], bool] | Callable[[Any], bool],): 
            function to call to determine if 'item' is the appropriate type.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
        item (Any): class or instance to examine.
        kind (Type[Any]): type to check if 'item' is.
            
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                                 
    Returns:
        bool: whether 'item' is a 'kind'.
    
    """
    raise_error = configuration.RAISE_ERRORS if None else raise_error
    value = checker(item) if kind is None else checker(item, kind)  
    return report_is(
        value = value,
        raise_error = raise_error,
        item = item,
        kind = kind)

def is_kind_container(
    item: Any,
    checker: Callable[[Any, Type[Any]], bool] | Callable[[Any], bool],
    raise_error: Optional[bool] = None,
    include_str: Optional[bool] = None,
    kind: Optional[Type[Any] | str] = None) -> bool:
    """Returns whether 'item' is 'kind' or an error.

    Args:
        item (Any): class or instance to examine.
        checker (Callable[[Any, Type[Any]], bool] | Callable[[Any], bool],): 
            function to call to determine if 'item' is the appropriate type.
        raise_error (Optional[bool]): whether to raise an error if 'attribute' 
            is not an attribute of 'item' (True) or to simply return False in
            such situations. Defaults to None, which means the global 
            'miller.RAISE_ERRORS' setting will be used.
        kind (Type[Any]): type to check if 'item' is.
            
    Raises:
        TypeError: if 'item' is not the appropriate type and 'raise_error' is 
            True (or if it is None and the global setting is True).
                                 
    Returns:
        bool: whether 'item' is a 'kind'.
    
    """
    raise_error = configuration.RAISE_ERRORS if None else raise_error
    include_str = configuration.INCLUDE_STR if None else include_str
    value = checker(item) if kind is None else checker(item, kind)  
    if not include_str and isinstance(item, str):
        value = False
    return report_is(
        value = value,
        raise_error = raise_error,
        item = item,
        kind = kind) 

def list_elements(
    checker: Callable[[Any, Any, bool], bool],
    raise_error: bool,
    match_all: bool,
    item: Any) -> MutableSequence[Any]:
    """_summary_

    Args:
        checker (Callable[[Any, Any, bool], bool]): _description_
        raise_error (bool): _description_
        match_all (bool): _description_
        item (Any): _description_
        elements (MutableSequence[Any]): _description_

    Returns:
        bool: _description_
        
    """
    match_all = configuration.MATCH_ALL if None else match_all 
    scope = all if match_all else any
    kwargs = dict(raise_error = False)
    value = scope(checker(item, a, **kwargs) for a in elements)  
    return report_map(
        value = value,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        elements = elements)
    
def map_elements(
    item: Any,
    mapper: Callable[[Any, Any, bool], bool],
    checker: Optional[Callable[[Any, Type[Any]], bool] | 
                      Callable[[Any], bool]] = None,
    raise_error: Optional[bool] = None,
    include_private: Optional[bool] = None) -> MutableMapping[str, Any]:
    """_summary_

    """
    raise_error = configuration.RAISE_ERRORS if None else raise_error
    include_private = configuration.INCLUDE_PRIVATE if None else include_private 
    return report_map(
        value = value,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        elements = elements)

def name_elements(
    checker: Callable[[Any, Any, bool], bool],
    raise_error: bool,
    match_all: bool,
    item: Any) -> MutableSequence[str]:
    """_summary_

    Args:
        checker (Callable[[Any, Any, bool], bool]): _description_
        raise_error (bool): _description_
        match_all (bool): _description_
        item (Any): _description_
        elements (MutableSequence[Any]): _description_

    Returns:
        bool: _description_
    """
    match_all = configuration.MATCH_ALL if None else match_all 
    scope = all if match_all else any
    kwargs = dict(raise_error = False)
    value = scope(checker(item, a, **kwargs) for a in elements)  
    return report_map(
        value = value,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        elements = elements)    

def report_has(
    value: bool,
    raise_error: bool,
    match_all: bool,
    item: Any, 
    attributes: MutableSequence[Any]) -> bool:
    """_summary_

    Args:
        value (bool): _description_
        raise_error (bool): _description_
        match_all (bool): _description_
        item (Any): _description_
        elements (MutableSequence[Any]): _description_

    Returns:
        bool: _description_
        
    """
    if not value and raise_error and match_all:
        raise AttributeError(
            f'At least one of {attributes} is not in {item}')
    elif not value and raise_error:
        raise AttributeError(
            f'Some of {attributes} are not in {item}')
    elif not value:
        return configuration.DEFAULT_HAS
    else:
        return value
    
def report_is(
    value: bool,
    raise_error: bool,
    item: Any, 
    kind: Optional[Type[Any]]) -> bool:
    """_summary_

    Args:
 

    Returns:
        bool: _description_
        
    """
    if not value and raise_error and kind is None:
        raise TypeError(f'{item} failed the type check')
    elif not value and raise_error:
        raise TypeError(f'{item} is not {kind} type')
    elif not value:
        return configuration.DEFAULT_IS
    else:
        return value

def report_list(
    value: MutableSequence[Any],
    raise_error: bool,
    match_all: bool,
    item: Any, 
    elements: MutableSequence[Any]) -> bool:
    """_summary_

    Args:
        value (bool): _description_
        raise_error (bool): _description_
        match_all (bool): _description_
        item (Any): _description_
        elements (MutableSequence[Any]): _description_

    Returns:
        bool: _description_
    """
    if not value and raise_error and match_all:
        raise AttributeError(
            f'At least one of {elements} is not in {item}')
    elif not value and raise_error:
        raise AttributeError(
            f'Some of {elements} are not in {item}')
    elif not value:
        return configuration.DEFAULT_LIST
    else:
        return value

def report_map(
    value: MutableMapping[Hashable, Any],
    raise_error: bool,
    match_all: bool,
    item: Any, 
    elements: MutableSequence[Any]) -> bool:
    """_summary_

    Args:
        value (bool): _description_
        raise_error (bool): _description_
        match_all (bool): _description_
        item (Any): _description_
        elements (MutableSequence[Any]): _description_

    Returns:
        bool: _description_
    """
    if not value and raise_error and match_all:
        raise AttributeError(
            f'At least one of {elements} is not in {item}')
    elif not value and raise_error:
        raise AttributeError(
            f'Some of {elements} are not in {item}')
    elif not value:
        return configuration.DEFAULT_MAP
    else:
        return value

def report_name(
    value: MutableSequence[str],
    raise_error: bool,
    match_all: bool,
    item: Any, 
    elements: MutableSequence[Any]) -> bool:
    """_summary_

    Args:
        value (bool): _description_
        raise_error (bool): _description_
        match_all (bool): _description_
        item (Any): _description_
        elements (MutableSequence[Any]): _description_

    Returns:
        bool: _description_
    """
    if not value and raise_error and match_all:
        raise AttributeError(
            f'At least one of {elements} is not in {item}')
    elif not value and raise_error:
        raise AttributeError(
            f'Some of {elements} are not in {item}')
    elif not value:
        return configuration.DEFAULT_NAME
    else:
        return value
            