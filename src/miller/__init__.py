"""Introspection tools using consistent, accessible syntax"""

from __future__ import annotations

__version__ = '0.2.0'

__author__: str = 'Corey Rayburn Yung'

from . import (
    attributes,
    configuration,
    containers,
    disks,
    examiners,
    framework,
    identity,
    modules,
    utilities,
)
from .attributes import *  # noqa: F403
from .containers import *  # noqa: F403
from .disks import *  # noqa: F403
from .examiners import *  # noqa: F403
from .framework import *  # noqa: F403
from .identity import *  # noqa: F403
from .modules import *  # noqa: F403

__all__: list[str] = sorted({  # noqa: PLE0605
    *attributes.__all__,
    *containers.__all__,
    *disks.__all__,
    *examiners.__all__,
    *framework.__all__,
    *identity.__all__,
    *modules.__all__})

# Submodules available as `miller.configuration` and `miller.utilities`.
_SUBMODULES = (configuration, utilities)
