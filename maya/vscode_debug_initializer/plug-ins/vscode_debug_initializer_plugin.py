"""
Entry point of the Maya vscode_debug_initializer plugin.
"""
import logging
from maya import cmds
from maya.api import OpenMaya

logger = logging.getLogger(__name__)


_PLUGIN_NAME = "vscode_debug_initializer"
_VENDOR = "BeardedPlatypus"


def maya_useNewAPI():
    """Indicate this plugin is making use of the Maya Python 2.0 API."""
    pass


def initializePlugin(mobject):
    """
    Initialize the vscode_debug_initializer plugin.

    Args:
        mobject: The maya plugin object provided by the framework.
    """
    plugin_version = cmds.moduleInfo(version=True, moduleName=_PLUGIN_NAME)
    logger.info("Initializing %s %s.", _PLUGIN_NAME, plugin_version)

    mplugin = OpenMaya.MFnPlugin(mobject, vendor=_VENDOR, version=plugin_version)

    # Make sure no importing occurs on the global level which might impact
    # performance if the module is not used.
    import vscode_debug_initializer
    vscode_debug_initializer.initialize(mplugin)


def uninitializePlugin(mobject):
    """
    Uninitialize the vscode_debug_initializer plugin.

    Args:
        mobject: The maya plugin object provided by the framework.
    """
    mplugin = OpenMaya.MFnPlugin(mobject)

    # Make sure no importing occurs on the global level which might impact
    # performance if the module is not used.
    import vscode_debug_initializer
    vscode_debug_initializer.uninitialize(mplugin)
