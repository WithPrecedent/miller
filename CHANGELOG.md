# Changelog

All notable changes to this project will be documented in this file.

<!-- insertion marker -->

## 0.2.1

* Updated README
* Fixed CI pre-commit and Python 3.10 failures
* Replaced star imports in `__init__.py` with explicit imports

## 0.2.0

* Updated repository to snickerdoodle 0.3.3 (`uv`, `hatchling`, new GitHub Actions)
* Removed dependencies on `camina` and `nagata`; miller now has no dependencies
* Renamed the `map` and `get`/`list` prefixes to `catalog` and `collect` to match the README
* Renamed the `include_private` parameter to `include_privates` to match the README
* Added `miller.utilities`, `miller.framework` setters for all global settings, and the `is_*` functions for tuples, dunders, and privates
* Rewrote `attributes`, `identity`, `containers`, `disks`, `modules`, and `examiners`, fixing many bugs (for example, `has_*` functions that ignored `match_all`, undefined names in `base`, and broken `Inspector` classes)
* Changed the default of `RAISE_ERRORS` to `False`, so `has_*` and `is_*` functions return `False` unless told to raise
* Added a full unit test suite
* Dropped support for Python 3.10 (Python 3.11 or later is now required)

## 0.1.0

* Initial Commit
