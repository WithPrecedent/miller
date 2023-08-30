"""Fake module for module introspection tests."""

import dataclasses


@dataclasses.dataclass
class DummyDataclass(object):
    
    pass
    
    
class DummyClass(object):
    
    pass
 
    
def dummy_function() -> None:
    return
