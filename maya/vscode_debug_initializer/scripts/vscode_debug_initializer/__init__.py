"""
vscode_debug_initializer.__init__ provides the initialization logic of the module.
"""

from maya.api import OpenMaya

from . import command, common, mmap_utils


def initialize(mplugin: OpenMaya.MFnPlugin) -> None:
    """
    Initialize the vscode_debug_initializer module.

    Args:
        mplugin (OpenMaya.MFnPlugin): The plugin to initialize with.
    """
    with common.wait_cursor():
        command.initialize(mplugin)


def uninitialize(mplugin: OpenMaya.MFnPlugin) -> None:
    """
    Uninitialize the vscode_debug_initializer module.

    Args:
        mplugin (OpenMaya.MFnPlugin): The plugin to uninitialize.
    """
    command.uninitialize(mplugin)
    mmap_utils.close_mmaps()
