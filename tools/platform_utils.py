"""
Cross-platform utility functions for subprocess and file operations.

Provides platform-agnostic wrappers around Windows-specific APIs such as
STARTUPINFO, CREATE_NO_WINDOW, and os.startfile, returning safe defaults
on non-Windows platforms.
"""

import os
import subprocess
import sys


def get_startupinfo():
    """Return subprocess.STARTUPINFO on Windows, None on other platforms.

    On Windows the returned object has its *dwFlags* set to
    ``STARTF_USESHOWWINDOW`` and *wShowWindow* set to ``SW_HIDE`` so that
    spawned processes do not flash a console window.
    """
    if sys.platform == "win32":
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return info
    return None


def get_creationflags():
    """Return ``subprocess.CREATE_NO_WINDOW`` on Windows, ``0`` otherwise.

    ``CREATE_NO_WINDOW`` (0x08000000) prevents the creation of a console
    window for the child process.  On Linux / macOS no flag is needed.
    """
    if sys.platform == "win32":
        return subprocess.CREATE_NO_WINDOW
    return 0


def open_file_manager(path):
    """Open the operating system's file manager at *path*.

    Supported platforms
    -------------------
    * **Windows**  -- ``os.startfile()``
    * **macOS**    -- ``open``
    * **Linux**    -- ``xdg-open``

    Parameters
    ----------
    path : str or os.PathLike
        Directory (or file) to reveal in the file manager.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    """
    resolved = os.fspath(path)

    if not os.path.exists(resolved):
        raise FileNotFoundError(f"Path does not exist: {resolved}")

    if sys.platform == "win32":
        os.startfile(resolved)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", resolved])
    else:
        # Linux / other Unix-likes
        subprocess.Popen(["xdg-open", resolved])


def get_executable_filter(name):
    """Return a platform-appropriate Qt file-dialog filter for executables.

    On Windows the filter targets ``*.exe`` files; on Linux / macOS it
    falls back to ``*`` (any file) because executables do not have a
    predictable extension.

    Parameters
    ----------
    name : str
        Human-readable label for the filter (e.g. ``"FFmpeg"``).

    Returns
    -------
    str
        A filter string suitable for ``QFileDialog.getOpenFileName()``.
    """
    if sys.platform == "win32":
        return f"{name} (*.exe);;All Files (*)"
    return f"{name} (*);;All Files (*)"
