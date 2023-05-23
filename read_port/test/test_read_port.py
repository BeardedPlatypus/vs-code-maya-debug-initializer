"""
Test the `read_port.exe` utility.
"""
import mmap
import subprocess
from pathlib import Path


EXECUTABLE = Path(__file__).parent.parent / "dist" / "read_port.exe"
MMAP_TAG = "Local\\BEARDEDPLATYPUS_TEST_MMAP"


def _run_read_port():
    p = subprocess.run([EXECUTABLE.resolve(), MMAP_TAG], capture_output=True, shell=True)
    return int(p.stdout)

def _encode_port(value):
    return value.to_bytes(2, byteorder="little", signed=False)


def _construct_mmap_with_value(expected_value):
    debug_mmap = mmap.mmap(-1, 2, tagname=MMAP_TAG)
    debug_mmap.write(_encode_port(expected_value))
    return debug_mmap


def test_with_map():
    # GIVEN: an existing mmap with a value
    expected_value = 3000
    debug_mmap = _construct_mmap_with_value(expected_value)

    # WHEN: attach_mmap_util.exe is run without an active mmap
    val = _run_read_port()

    # THEN: the result is equal to the initial value 
    assert val == expected_value

    debug_mmap.close()


def test_no_map():
    # WHEN: read_.exe is run without an active mmap
    val = _run_read_port()

    # THEN: the result is 0
    assert val == 0