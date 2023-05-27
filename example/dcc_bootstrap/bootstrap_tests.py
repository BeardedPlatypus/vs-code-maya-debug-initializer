import io
import logging
import os
from pathlib import Path

import maya.cmds as cmds

logger = logging.getLogger(__name__)


def run_tests():
    exit_code = 1

    # Initialise debug plugin:
    port = int(os.environ.get("MDI_DEBUG_PORT", -1))

    if port > 0:
        cmds.loadPlugin("vscode_debug_initializer_plugin")
        cmds.mdi_ConfigureDebugServer(port, waitForDebugger=True)

    try:
        root_directory = Path(os.environ["BEARDEDPLATYPUS_ROOT"])
        test_dir = root_directory / "tests"
        os.environ["PATH"] = os.environ["PATH"] + os.pathsep + str(test_dir)

        logger.warning("--- Starting Tests ---")
        logger.warning(f"Test directory: {test_dir}")
        
        import unittest

        suite = unittest.TestLoader().discover(test_dir)
        stream = io.StringIO()

        result = unittest.TextTestRunner(verbosity=2, stream=stream).run(suite)

        print(stream.getvalue())

        if not (result.errors or result.failures):
            exit_code = 0

    except Exception as e:
        logger.error("An error occurred %s. See the stack trace below", str(e))
        logger.exception(e)
        # Value is printed in order for it to show up correctly in the (CI) terminal.
        print(e)

    cmds.evalDeferred("cmds.quit(exitCode=" + str(exit_code) + ", force=True)")

run_tests()