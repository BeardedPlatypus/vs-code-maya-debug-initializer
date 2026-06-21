"""
vscode_debug_initializer.debug_server provides the logic to initialize a debug server.
"""

import logging
from . import constants, common

logger = logging.getLogger(__name__)


def initialize_debugger(port: int) -> None:
    """
    Initialize the debugger at the specified port.

    Args:
        port (int): The port to initialize the debugger server at.
    """
    import debugpy

    debugpy.configure(python=common.get_mayapy_path())
    debugpy.listen(address=(constants.HOST, port))
    logging.info("Started debugpy debug server at %s:%s", constants.HOST, str(port))


def wait_for_client() -> None:
    """
    Wait for the client to attach.
    """
    import debugpy

    logging.info("Waiting for connection...")
    debugpy.wait_for_client()
