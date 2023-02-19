"""
disks: introspection tools for files and folders
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
    has_files
    has_folders
    has_modules
    has_paths
    list_files
    list_folders
    list_modules
    list_paths
    map_files
    map_folders
    map_modules
    map_paths
    name_files
    name_folders
    name_modules
    name_paths   
    
ToDo:
    

"""
from __future__ import annotations
import pathlib
import types
from typing import Optional

import camina
import nagata

from . import configuration
from . import identity


def has_files(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path],
    recursive: Optional[bool] = None) -> bool:  
    """Returns whether all 'elements' are in 'item' and are files.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'miller.RECURSIVE' is used.
                    
    Returns:
        bool: whether all 'elements' are in 'item' and are files.
        
    """ 
    return (
        has_paths(item, elements = elements, recursive = recursive)
        and all(identity.is_file(path) for path in item))
          
def has_folders(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path],
    recursive: Optional[bool] = None) -> bool:  
    """Returns whether all 'elements' are in 'item' and are folders.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'miller.RECURSIVE' is used.
                    
    Returns:
        bool: whether all 'elements' are in 'item' and are folders.
        
    """ 
    return (
        has_paths(item, elements = elements, recursive = recursive)
        and all(identity.is_folder(path) for path in item))
  
def has_modules(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path],
    recursive: Optional[bool] = None) -> bool:  
    """Returns whether all 'elements' are in 'item' and are modules.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'miller.RECURSIVE' is used.
                    
    Returns:
        bool: whether all 'elements' are in 'item' and are modules.
        
    """ 
    return (
        has_paths(item, elements = elements, recursive = recursive)
        and all(identity.is_module(path) for path in item))
   
def has_paths(
    item: str | pathlib.Path,
    elements: list[str | pathlib.Path],
    recursive: Optional[bool] = None) -> bool:  
    """Returns whether all 'elements' are in 'item' and are paths.
  
    Args:
        item (str | pathlib.Path): path of folder to examine.
        elements (list[str | pathlib.Path]): list of paths to test whether they 
            are in 'item'.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'miller.RECURSIVE' is used.
                    
    Returns:
        bool: whether all 'elements' are in 'item' and are paths.
        
    """ 
    paths = list_paths(item, recursive = recursive)
    elements = [camina.pahlibify(p) for p in elements]
    return all(elements in paths) and all(identity.is_path(path) for path in item)

def list_files(
    item: str | pathlib.Path, 
    recursive: Optional[bool] = None,
    suffix: Optional[str] = '*') -> list[pathlib.Path]:  
    """Returns list of non-python module file paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine. 
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'miller.RECURSIVE' is used.
        suffix (Optional[str]): file suffix to match. Defaults to '*' (all 
            suffixes).
        
    Returns:
        list[pathlib.Path]: a list of file paths in 'item'.
        
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    paths = list_paths(item, recursive = recursive, suffix = suffix)
    return [p for p in paths if identity.is_file(item = p)]

def list_folders(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[pathlib.Path]:  
    """Returns list of folder paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'miller.RECURSIVE' is used.
        
    Returns:
        list[pathlib.Path]: a list of folder paths in 'item'.
        
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    paths = list_paths(item, recursive = recursive)
    return [p for p in paths if identity.is_folder(item = p)]

def list_modules(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None,
    import_modules: Optional[bool] = False) -> (
        list[pathlib.Path |types.ModuleType]):  
    """Returns list of python module paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'miller.RECURSIVE' is used.
        import_modules (Optional[bool]): whether the values in the returned dict
            should be imported modules (True) or file paths to modules (False).
                    
    Returns:
        list[pathlib.Path |types.ModuleType]: a list of python module paths in 
            'item' or imported modules if 'import_modules' is True.
            
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    paths = list_paths(item, recursive = recursive)
    modules = [p for p in paths if identity.is_module(item = p)]
    if import_modules:
        modules = [nagata.from_file_path(path = p) for p in modules]
    return modules
    
def list_paths(
    item: str | pathlib.Path, 
    recursive: Optional[bool] = None,
    suffix: Optional[str] = '*') -> list[pathlib.Path]:  
    """Returns list of all paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine. 
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'miller.RECURSIVE' is used.
        suffix (Optional[str]): file suffix to match. Defaults to '*' (all 
            suffixes).
        
    Returns:
        list[pathlib.Path]: a list of all paths in 'item'.
        
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    item = camina.pathlibify(item) 
    if recursive:
        return list(item.rglob(f'*.{suffix}'))
    else:
        return list(item.glob(f'*.{suffix}'))
 
def map_files(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> dict[str, pathlib.Path]:  
    """Returns dict of python file names and file paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'miller.RECURSIVE' is used.
        
    Returns:
        dict[str, pathlib.Path]: dict with keys being file names and values
            being file paths. 
        
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    kwargs = dict(item = item, recursive = recursive)
    names = name_files(**kwargs)
    files = list_files(**kwargs)
    return dict(zip(names, files))

def map_folders(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> dict[str, pathlib.Path]:  
    """Returns dict of python folder names and folder paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'miller.RECURSIVE' is used.
        
    Returns:
        dict[str, pathlib.Path]: dict with keys being folder names and values 
            being folder paths. 
        
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    kwargs = dict(item = item, recursive = recursive)
    names = name_folders(**kwargs)
    folders = list_folders(**kwargs)
    return dict(zip(names, folders))
 
def map_modules(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None,
    import_modules: Optional[bool] = False) -> (
        dict[str, types.ModuleType] | dict[str, pathlib.Path]):  
    """Returns dict of python module names and modules in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'miller.RECURSIVE' is used.
        import_modules (Optional[bool]): whether the values in the returned dict
            should be imported modules (True) or file paths to modules (False).
        
    Returns:
        dict[str, types.ModuleType] | dict[str, pathlib.Path]: dict with str key 
            names of python modules and values as the paths to corresponding 
            modules or the imported modules (if 'import_modules' is True).
        
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    kwargs = dict(item = item, recursive = recursive)
    names = name_modules(**kwargs)
    modules = list_modules(**kwargs, import_modules = import_modules)
    return dict(zip(names, modules))

def map_paths(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> dict[str, pathlib.Path]:  
    """Returns dict of python path names and paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (Optional[bool]): whether to include subfolders. Defaults to 
            None. If 'recursive' is None, 'miller.RECURSIVE' is used.
        
    Returns:
        dict[str, pathlib.Path]: dict with keys being paht names and values
            being paths. 
        
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    kwargs = dict(item = item, recursive = recursive)
    names = name_paths(**kwargs)
    paths = list_paths(**kwargs)
    return dict(zip(names, paths))

def name_files(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of file paths in 'item'.
    
    The 'stem' property of 'pathlib.Path' is used for the names.
        
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'miller.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of names of file paths in 'item'.
        
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    item = camina.pathlibify(item)
    kwargs = dict(item = item, recursive = recursive)
    return [p.stem for p in list_files(**kwargs)]
          
def name_folders(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of folder paths in 'item'.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'miller.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of folder paths in 'item'.
        
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    item = camina.pathlibify(item)
    kwargs = dict(item = item, recursive = recursive)
    return [p.name for p in list_folders(**kwargs)]
 
def name_modules(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of paths to python modules in 'item'.
    
    The 'stem' property of 'pathlib.Path' is used for the names.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'miller.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of names of paths to python modules in 'item'.
        
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    item = camina.pathlibify(item)
    kwargs = dict(item = item, recursive = recursive)
    return [p.stem for p in list_modules(**kwargs)]
 
def name_paths(
    item: str | pathlib.Path,
    recursive: Optional[bool] = None) -> list[str]:  
    """Returns list of names of paths in 'item'.
    
    For folders, the 'name' property of 'pathlib.Path' is used. For files, the
    'stem' property is.
    
    Args:
        item (str | pathlib.Path): path of folder to examine.
        recursive (bool): whether to include subfolders. Defaults to None. If
            'recursive' is None, 'miller.RECURSIVE' is used.
        
    Returns:
        list[str]: a list of names of paths in 'item'.
        
    """
    if recursive is None:
        recursive = configuration.RECURSIVE   
    kwargs = dict(item = item, recursive = recursive)
    return name_files(**kwargs) + name_folders(**kwargs)
