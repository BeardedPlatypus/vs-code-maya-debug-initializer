"""
vscode_debug_initializer.common provides the common code used within the
vscode_debug_initializer module.
"""

import os
import os.path
import sys

from contextlib import contextmanager
from maya import cmds


def get_mayapy_path():
    """
    Get the mayapy path for the current version of Maya being used.

    Returns:
        (str): The path to the mayapy executable.
    """
    maya_version = int(cmds.about(q=True, majorVersion=True))
    mayapy_name = "mayapy.exe" if maya_version != 2022 or sys.version_info.major == 3 else "mayapy2.exe"
    return os.path.join(os.environ['MAYA_LOCATION'], 'bin', mayapy_name)


@contextmanager
def wait_cursor():
    """
    Context manager for the cmds.waitCursor operation of Maya
    """
    cmds.waitCursor(state=True)

    try:
        yield
    finally:
        cmds.waitCursor(state=False)
