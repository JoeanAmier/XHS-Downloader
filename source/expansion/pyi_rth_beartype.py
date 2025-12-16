"""
PyInstaller runtime hook for beartype compatibility.

This runtime hook runs BEFORE any user code and patches beartype's import hook
system to be compatible with PyInstaller's frozen import mechanism.

The Problem:
-----------
Beartype's `beartype.claw` module installs a custom path hook into
`sys.path_hooks` that uses `SourceFileLoader` to load and transform Python
source files. In PyInstaller's frozen environment:

1. There are no source .py files - only compiled bytecode in a PYZ archive
2. Beartype's hook is prepended to `sys.path_hooks`, taking precedence over
   PyInstaller's `PyiFrozenFinder`
3. Beartype clears `sys.path_importer_cache`, invalidating PyInstaller's
   cached finders

This causes `ModuleNotFoundError` for any module imported AFTER beartype's
hook is installed.

The Fix:
--------
This runtime hook monkey-patches beartype's `add_beartype_pathhook` function
to detect PyInstaller's frozen environment and skip installing the problematic
path hook.

See Also:
---------
- https://github.com/beartype/beartype/issues/599
- https://github.com/pyinstaller/pyinstaller/issues/9324
"""

import sys


def _is_pyinstaller_frozen():
    """Check if running in a PyInstaller frozen environment."""
    return getattr(sys, "frozen", False) or hasattr(sys, "_MEIPASS")


def _patch_beartype_claw():
    """
    Patch beartype's add_beartype_pathhook to skip in frozen environments.

    This patches the function at import time before any user code can call it.
    """
    # Only patch if we're actually frozen
    if not _is_pyinstaller_frozen():
        return

    try:
        # Import the module containing the function to patch
        from beartype.claw._importlib import clawimpmain

        # Store the original function
        _original_add_beartype_pathhook = clawimpmain.add_beartype_pathhook

        def _patched_add_beartype_pathhook():
            """
            Patched version of add_beartype_pathhook that skips in frozen env.
            """
            if _is_pyinstaller_frozen():
                # In frozen environment, skip installing the path hook entirely
                # This prevents breaking PyInstaller's frozen import system
                return
            # Otherwise, call the original
            return _original_add_beartype_pathhook()

        # Replace the function in clawimpmain module
        clawimpmain.add_beartype_pathhook = _patched_add_beartype_pathhook

        # CRITICAL: Also patch clawpkgmain which does `from ... import add_beartype_pathhook`
        # and thus has its own local reference to the original function
        from beartype.claw._package import clawpkgmain

        clawpkgmain.add_beartype_pathhook = _patched_add_beartype_pathhook

    except ImportError:
        # beartype not installed or not using claw module
        pass
    except Exception:
        # Don't crash on patch failure
        pass


# Apply the patch when this runtime hook is loaded
_patch_beartype_claw()
