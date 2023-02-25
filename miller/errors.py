"""
errors: custom errors for miller
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
import abc
from collections.abc import Callable, MutableSequence
import dataclasses
import inspect
import types
from typing import Any, Optional, Type

from . import configuration 


class Sabaka(abc.ABC):
    """Mixin for exceptions.
    
    In Belter Creoloe, in the TV show The Expanse (and in the books on which the
    show was based), "Sabaka" means "a general-purpose curse; "Dammit!" or 
    "You bastard!" (https://expanse.fandom.com/wiki/Belter_Creole), a suitable
    name for error messaging.
    
    This mixin provides sources of alternative or default error messages if one
    is not directly passed to a Exception subclass. If a message is passed, the 
    Exception class will operate in the same manner as a normal exception.
    
    This mixin prioritizes how the loggged error message is constructed in the
    following order:
        1) passed message;
        2) message created by other passed arguments using the 'compose' 
            method, if any args or kwargs are passed;
        3) message in the class 'default' attribute;
        4) whatever message is created be the parent or mixed-in Exception 
            subclass's '__init__' method when no message is passed.
   
    Args:
        default (str | configuration.MISSING_TYPE): default error message. 
            Defaults to configuration.MISSING.
        
    """
    default: str | configuration.MISSING_TYPE = configuration.MISSING
    
    def __init__(self, message: str, *args: Any, **kwargs: Any):
        """Calls the mixed-in Exception class with the appropriate message."""
        if message is not None:
            super().__init__(message, *args, **kwargs)
        elif args or kwargs:
            super().__init__(self.compose(*args, **kwargs))
        elif self.default is not configuration.MISSING:
            super().__init__(self.default)
        else:
            super().__init__()
            
    def compose(self, *args, **kwargs) -> str:
        """Returns an error message based on passed arguments.
        
        Subclasses should override this method. But, in the event, this method
        is not overridden, a str is returned with passed args and arguments of
        kwargs.
        
        Return:
            str: created from args and kwargs.
            
        """
        return ', '.join([str(args), str(kwargs.values())])


class ValidationFailed(Sabaka, AttributeError):
    """Error for a failed check by a passed callable.
    
    Args:
        default (str | configuration.MISSING_TYPE): default error message. 
            Defaults to configuration.MISSING, which would result in the 
            'compose' method being called to create an error message if no 
            message is passed.
        
    """
    default: str | configuration.MISSING_TYPE = configuration.MISSING
        
    def compose(
        self, 
        item: Any, 
        checker: Optional[Callable | str] = None) -> str:
        """Returns an error message based on passed arguments."""
        item = item if str else item.__name__
        if checker is None:
            return f'{item} failed a check'
        else:
            checker = checker if str else checker.__name__
            return f'{item} failed a check by {checker}'
    

class NotAttribute(Sabaka, AttributeError):
    """Error for a missing class or instance attribute.
    
    Args:
        default (str | configuration.MISSING_TYPE): default error message. 
            Defaults to configuration.MISSING, which would result in the 
            'compose' method being called to create an error message if no 
            message is passed.
        
    """
    default: str | configuration.MISSING_TYPE = configuration.MISSING
        
    def compose(self, base: Any, attribute: str) -> str:
        """Returns an error message based on passed arguments."""
        base = base if str else base.__name__
        return f'{attribute} is not an attribute of {base}'
    

class NotType(Sabaka, TypeError):
    """Error for a type check failure.
    
    Args:
        default (str | configuration.MISSING_TYPE): default error message. 
            Defaults to configuration.MISSING, which would result in the 
            'compose' method being called to create an error message if no 
            message is passed.
        
    """
    
    def compose(self, item: Any, kind: Any) -> str:
        """Returns an error message based on passed arguments."""
        kind = kind if str else kind.__name__
        item = item if str else item.__name__
        return f'{item} is not a {kind}'
    
     