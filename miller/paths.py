"""
paths: inspects paths on disk
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
    catalog_files
    catalog_folders
    catalog_modules
    catalog_paths  
    get_files
    get_folders
    get_modules
    get_paths   
    has_files
    has_folders
    has_modules
    has_paths 
    is_file
    is_folder
    is_module
    is_path 
    name_files
    name_folders
    name_modules
    name_paths  
          
To Do:

    
"""
from __future__ import annotations
import pathlib
import types
from typing import Optional

import camina
import nagata

from . import defaults


def catalog_files(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> dict[str, pathlib.Path]:  
    """Returns dict of python file names and file paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        dict[dict[str, pathlib.Path]: dict with keys being file names and values
            being file paths. 
        
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    kwargs = {'item': item, 'recursive': recursive}
    names = name_files(**kwargs)
    files = get_files(**kwargs)
    return dict(zip(names, files))

def catalog_folders(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> dict[str, pathlib.Path]:  
    """Returns dict of python folder names and folder paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        dict[dict[str, pathlib.Path]: dict with keys being folder names and 
            values being folder paths. 
        
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    kwargs = {'item': item, 'recursive': recursive}
    names = name_folders(**kwargs)
    folders = get_folders(**kwargs)
    return dict(zip(names, folders))

def catalog_modules(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None,
    import_modules: Optional[bool] = False) -> (
        dict[str, types.ModuleType] | dict[str, pathlib.Path]):  
    """Returns dict of python module names and modules in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        import_modules (Optional[bool]): whether the values in the returned dict
            should be imported modules (True) or file paths to modules (False).
        
    Returns:
        dict[str, types.ModuleType] | dict[str, pathlib.Path]: dict with str key 
            names of python modules and values as the paths to corresponding 
            modules or the imported modules (if 'import_modules' is True).
        
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    kwargs = {'item': item, 'recursive': recursive}
    names = name_modules(**kwargs)
    modules = get_modules(**kwargs, import_modules = import_modules)
    return dict(zip(names, modules))

def catalog_paths(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> dict[str, pathlib.Path]:  
    """Returns dict of python path names and paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        dict[dict[str, pathlib.Path]: dict with keys being paht names and values
            being paths. 
        
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    kwargs = {'item': item, 'recursive': recursive}
    names = name_paths(**kwargs)
    paths = get_paths(**kwargs)
    return dict(zip(names, paths))
    
def get_files(
    item: str | pathlib.Path, 
    recursive: Optional[bool] = None,
    suffix: Optional[str] = '*') -> list[pathlib.Path]:  
    """Returns list of non-python module file paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine. 
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        suffix (Optional[str]): file suffix to match. Defaults to '*' (all 
            suffixes).
        
    Returns:
        list[pathlib.Path]: a list of file paths in 'item'.
        
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    paths = get_paths(item = item, recursive = recursive, suffix = suffix)
    return [p for p in paths if is_file(item = p)]

def get_folders(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[pathlib.Path]:  
    """Returns list of folder paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        list[pathlib.Path]: a list of folder paths in 'item'.
        
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    paths = get_paths(item = item, recursive = recursive)
    return [p for p in paths if is_folder(item = p)]

def get_modules(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None,
    import_modules: Optional[bool] = False) -> (
        list[pathlib.Path |types.ModuleType]):  
    """Returns list of python module paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        import_modules (Optional[bool]): whether the values in the returned dict
            should be imported modules (True) or file paths to modules (False).
                    
    Returns:
        list[pathlib.Path |types.ModuleType]: a list of python module paths in 
            'item' or imported modules if 'import_modules' is True.
            
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    paths = get_paths(item = item, recursive = recursive)
    modules = [p for p in paths if is_module(item = p)]
    if import_modules:
        modules = [nagata.from_file_path(path = p) for p in modules]
    return modules
    
def get_paths(
    item: str | pathlib.Path, 
    recursive: Optional[bool] = None,
    suffix: Optional[str] = '*') -> list[pathlib.Path]:  
    """Returns list of all paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine. 
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'defaults.RECURSIVE' is used.
        suffix (Optional[str]): file suffix to match. Defaults to '*' (all 
            suffixes).
        
    Returns:
        list[pathlib.Path]: a list of all paths in 'item'.
        
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    item = camina.pathlibify(item) 
    if recursive:
        return list(item.rglob(f'*.{suffix}'))
    else:
        return list(item.glob(f'*.{suffix}'))
      
def has_files(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path]) -> bool:  
    """Returns whether all 'elements' are in 'item'.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        
    Returns:
        bool: whether all 'elements' are in 'item'.
        
    """ 
    item = camina.pathlibify(item)
    paths = get_paths(item = item, recursive = False)
    elements = [camina.pahlibify(p) for p in elements]
    return all(elements in paths)
          
def has_folders(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path]) -> bool:  
    """Returns whether all 'elements' are in 'item'.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        
    Returns:
        bool: whether all 'elements' are in 'item'.
        
    """ 
    item = camina.pathlibify(item)
    paths = get_paths(item = item, recursive = False)
    elements = [camina.pahlibify(p) for p in elements]
    return all(elements in paths)
      
def has_modules(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path]) -> bool:  
    """Returns whether all 'elements' are in 'item'.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        
    Returns:
        bool: whether all 'elements' are in 'item'.
        
    """ 
    item = camina.pathlibify(item)
    paths = get_paths(item = item, recursive = False)
    elements = [camina.pahlibify(p) for p in elements]
    return all(elements in paths)
      
def has_paths(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path]) -> bool:  
    """Returns whether all 'elements' are in 'item'.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        
    Returns:
        bool: whether all 'elements' are in 'item'.
        
    """ 
    item = camina.pathlibify(item)
    paths = get_paths(item = item, recursive = False)
    elements = [camina.pahlibify(p) for p in elements]
    return all(elements in paths)

def is_file(item: str | pathlib.Path) -> bool:
    """Returns whether 'item' is a non-python-module file.
    
    Args:
        item (str | pathlib.Path): path to check.
        
    Returns:
        bool: whether 'item' is a non-python-module file.
        
    """ 
    item = camina.pathlibify(item)
    return (
        item.exists() 
        and item.is_file() 
        and not item.suffix in defaults.MODULE_SUFFIXES)

def is_folder(item: str | pathlib.Path) -> bool:
    """Returns whether 'item' is a path to a folder.
    
    Args:
        item (str | pathlib.Path): path to check.
        
    Returns:
        bool: whether 'item' is a path to a folder.
        
    """ 
    item = camina.pathlibify(item)
    return item.exists() and item.is_dir()

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
        and item.suffix in defaults.MODULE_SUFFIXES)

def is_path(item: str | pathlib.Path) -> bool:
    """Returns whether 'item' is a currently existing path.
    
    Args:
        item (str | pathlib.Path): path to check.
        
    Returns:
        bool: whether 'item' is a currently existing path.
        
    """ 
    item = camina.pathlibify(item)
    return item.exists()
      
def name_files(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of non-python-module file paths in 'item'.
    
    The 'stem' property of 'pathlib.Path' is used for the names.
        
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of names of non-python-module file paths in 'item'.
        
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    item = camina.pathlibify(item)
    kwargs = {'item': item, 'recursive': recursive}
    return [p.stem for p in get_files(**kwargs)]
          
def name_folders(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of folder paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of folder paths in 'item'.
        
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    item = camina.pathlibify(item)
    kwargs = {'item': item, 'recursive': recursive}
    return [p.name for p in get_folders(**kwargs)]
      
def name_modules(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of paths to python modules in 'item'.
    
    The 'stem' property of 'pathlib.Path' is used for the names.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of names of paths to python modules in 'item'.
        
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    item = camina.pathlibify(item)
    kwargs = {'item': item, 'recursive': recursive}
    return [p.stem for p in get_modules(**kwargs)]
      
def name_paths(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of paths in 'item'.
    
    For folders, the 'name' property of 'pathlib.Path' is used. For files, the
    'stem' property is.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'defaults.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of names of paths in 'item'.
        
    """
    if recursive is None:
        recursive = defaults.RECURSIVE   
    kwargs = {'item': item, 'recursive': recursive}
    return (
        name_files(**kwargs) 
        + name_folders(**kwargs) 
        + name_modules(**kwargs))
