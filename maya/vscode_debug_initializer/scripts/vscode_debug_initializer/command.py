"""
vscode_debug_initializer.command provides the command to configure the debug server.
"""
import logging

from maya.api import OpenMaya
from . import common, constants, debug_server, mmap


kWaitForClientShortName = "-wdb"
kWaitForClientLongName = "-waitForDebugger"

kMmapNameShortName = "-mmn"
kMmapNameLongName = "-mmapName"


class ConfigureDebugServerCommand(OpenMaya.MPxCommand):
    """
    ConfigureDebugServerCommand is a **NOT** undoable, **NOT** queryable, and **NOT** editable.

    Configures and starts the Debug Server at the specified port.
    """

    name = constants.CONFIGURE_DEBUG_SERVER_COMMAND_NAME

    def __init__(self):
        """
        Create a new ConfigureDebugServerCommand
        """
        OpenMaya.MPxCommand.__init__(self)
        self._port = None
        self._wait_for_client = False
        self._mmap_name = constants.DEFAULT_TAG_NAME

    @staticmethod
    def cmd_creator():
        """
        cmd_creator provides the factory method to create a 
        ConfigureDebugServerCommand.
        """
        return ConfigureDebugServerCommand()

    @staticmethod
    def syntax_creator():
        """
        syntax_creator provides the factory method to create the syntax
        of the ConfigureDebugServerCommand.
        """
        syntax = OpenMaya.MSyntax()
        syntax.setObjectType(OpenMaya.MSyntax.kStringObjects)
        syntax.addFlag(kWaitForClientShortName, kWaitForClientLongName, OpenMaya.MSyntax.kBoolean)
        syntax.addFlag(kMmapNameShortName, kMmapNameLongName, OpenMaya.MSyntax.kString)
        return syntax

    def doIt(self, args):
        """
        Configure and start the debug server.
        """
        self._parse_arguments(args)

        if self._port is None:
            logging.error("No valid port specified, debug server has not been started.")
            self.setResult(-1)
            return

        with common.wait_cursor():
            debug_server.initialize_debugger(self._port)
            mmap.write(self._mmap_name, self._port)

            if self._wait_for_client:
                debug_server.wait_for_client()

        self.setResult(self._port)

    def _parse_arguments(self, args):
        arg_data = OpenMaya.MArgParser(self.syntax(), args)
        
        self._wait_for_client = (
            arg_data.isFlagSet(kWaitForClientShortName) and
            arg_data.flagArgumentBool(kWaitForClientShortName, 0)
        )
        
        if arg_data.isFlagSet(kMmapNameShortName):
            self._mmap_name = arg_data.flagArgumentString(kMmapNameShortName, 0)
        
        provided_values = arg_data.getObjectStrings()

        try:
            self._port = int(provided_values[0])
        except:
            self._port = None


def initialize(mplugin):
    """
    Initialize the ConfigureDebugServerCommand.

    Args:
        mplugin (OpenMaya.MFnPlugin): The plugin to register the command to.
    """
    try:
        mplugin.registerCommand(
            constants.CONFIGURE_DEBUG_SERVER_COMMAND_NAME,
            ConfigureDebugServerCommand.cmd_creator,
            ConfigureDebugServerCommand.syntax_creator,
        )
    except:
        logging.error(
            "Could not register command %s", 
            constants.CONFIGURE_DEBUG_SERVER_COMMAND_NAME
        )


def uninitialize(mplugin):
    """
    Uninitialize the ConfigureDebugServerCommand.

    Args:
        mplugin (OpenMaya.MFnPlugin): The plugin to deregister the command from.
    """
    try:
        mplugin.deregisterCommand(
            constants.CONFIGURE_DEBUG_SERVER_COMMAND_NAME,
        )
    except:
        logging.error(
            "Could not deregister command %s", 
            constants.CONFIGURE_DEBUG_SERVER_COMMAND_NAME
        )
