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
from collections.abc import Callable, MutableSequence
import inspect
import sys
import types
from typing import Any, Optional, Type

import camina

from . import configuration
from . import result


def has_elements(
    checker: Callable[[Any, Any, bool], bool],
    raise_error: bool,
    match_all: bool,
    item: Any, 
    elements: MutableSequence[Any]) -> bool:
    """Returns error or value.

    Args:
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
        AttributeError: if some  or all 'elements' are not an attribute of 
            'item' and 'raise_error' is True (or if it is None and the global 
            setting is True).
                                 
    Returns:
        bool: whether all 'attributes' exist in 'item'.
    
    """
    raise_error = configuration.RAISE_ERRORS if None else raise_error
    match_all = configuration.MATCH_ALL if None else match_all 
    scope = all if match_all else any
    kwargs = dict(raise_error = False)
    value = scope(checker(item, a, **kwargs) for a in elements)  
    return result.report_has(
        value = value,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        elements = elements)
 
def is_kind(
    checker: Callable[[Any, Type[Any]], bool] | Callable[[Any], bool],
    raise_error: bool,
    item: Any,
    kind: Optional[Type[Any]]) -> bool:
    """Returns error or value.

    Args:
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
        AttributeError: if some  or all 'elements' are not an attribute of 
            'item' and 'raise_error' is True (or if it is None and the global 
            setting is True).
                                 
    Returns:
        bool: whether all 'attributes' exist in 'item'.
    
    """
    raise_error = configuration.RAISE_ERRORS if None else raise_error
    value = checker(item) if kind is None else checker(item, kind)  
    return result.report_is(
        value = value,
        raise_error = raise_error,
        item = item,
        kind = kind)

def map_elements(
    checker: Callable[[Any, Any, bool], bool],
    raise_error: bool,
    match_all: bool,
    item: Any, 
    elements: MutableSequence[Any]) -> bool:
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
    return result.report_map(
        value = value,
        raise_error = raise_error,
        match_all = match_all,
        item = item,
        elements = elements)
            