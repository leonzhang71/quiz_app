from importlib import import_module, sys as _sys

_mod = import_module("quiz_project.quiz_project.settings")

# re-export everything
globals().update(_mod.__dict__)

# keep reference to avoid garbage collection
_sys.modules[__name__] = _mod 