"""
vscode_debug_initializer.debug_server provides the logic to initialize a debug server.
"""

import logging
import six
from . import constants, common

logger = logging.getLogger(__name__)


def _initialize_debugger_debugpy(port):
    # type: (int) -> None
    import debugpy

    debugpy.configure(python=common.get_mayapy_path())
    debugpy.listen(address=(constants.HOST, port))
    logging.info("Started debugpy debug server at %s:%s", constants.HOST, str(port))


def _wait_for_client_debugpy():
    import debugpy

    logging.info("Waiting for connection...")
    debugpy.wait_for_client()


def _initialize_debugger_ptvsd(port):
    # type: (int) -> None
    import ptvsd

    ptvsd.enable_attach(address=(constants.HOST, port), redirect_output=True)
    logging.info("Started ptvsd debug server at %s:%s", constants.HOST, str(port))


def _wait_for_client_ptvsd():
    import ptvsd

    logging.info("Waiting for connection...")
    ptvsd.wait_for_attach()


initialize_debugger = _initialize_debugger_debugpy if six.PY3 else _initialize_debugger_ptvsd
"""
Initialize the debugger at the specified port.

Args:
    port (int): The port to initialize the debugger server at.
"""

wait_for_client = _wait_for_client_debugpy if six.PY3 else _wait_for_client_ptvsd
"""
Wait for the client to attach.
"""
