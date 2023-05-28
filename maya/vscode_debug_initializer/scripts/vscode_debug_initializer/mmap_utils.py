"""
vscode_debug_initializer.mmap provides the logic related to initializing and closing a mmap.
"""
import mmap
import six

DEBUG_MMAPS = {}


if six.PY3:
    def _encode_port(value):
        return value.to_bytes(2, byteorder="little", signed=False)
else:
    def _encode_port(value):
        return ''.join([chr((value >> i) & 0xff) for i in range(0, 16, 8)])


UNINITIALISED_PORT = _encode_port(0)


def _initialize_mmap(tag):
    # The DEBUG_MMAP describes the port, a freshly initialized DEBUG_MMAP will just
    # have zero bits, as such we assume this value to be the uninitialised state. 
    # We can write two bits, as such we are capable of writing an uint16 which will
    # describe our port.
    # We assume this function is only called if the mmap has not been initialized yet.
    DEBUG_MMAPS[tag] = mmap.mmap(-1, 2, tagname=tag)


def write(tag, port):
    """
    Write the specified port value to the specified mmap.

    Args:
        tag (string): The tag of the mmap to write to.
        port (int): The port at which the debugger was configured.
    """
    if tag not in DEBUG_MMAPS:
        _initialize_mmap(tag)

    DEBUG_MMAPS[tag].write(_encode_port(port))


def close_mmaps():
    """
    Close the mmaps.
    """
    for mmap in DEBUG_MMAPS.items():
        mmap.write(UNINITIALISED_PORT)
        mmap.close()

    DEBUG_MMAPS.clear()
