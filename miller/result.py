"""
value: generic error and return value functions
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
    Any, Callable, Hashable, MutableMapping, MutableSequence)
import inspect
import sys
import types
from typing import Any, Optional, Type

import camina

from . import configuration


def report_has(
    value: bool,
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
         