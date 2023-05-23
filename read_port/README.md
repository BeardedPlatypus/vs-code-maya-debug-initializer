# `read_port.exe`: utility to obtain the debug port

`read_port.exe` is a simple utility which prints either 0, or the debug port if
it is set. This utility is used by the Visual Studio code extension to find out which
port to connect to.

## Requirements

* Compiling the application:
  * **gcc**: The C compiler used to compile the source code.
* Running the tests:
  * **python**: A recent version of [python][python] is required to run the tests.
  * **tox**: The tests (as well as the compile command) can be run with [`tox`][tox].
       In order to do so, you will need `tox` installed.

## Compiling the application

The [`read_port.c`](src/read_port.c) provides the main function which
can be compiled from the "Developer Command Prompt for VS 2022" with the following
command:

```cmd
cl <repo_root>\read_port\src\read_port.c /DAS_EXECUTABLE
```

It does not provide a default value for the mmap tag, as such one always needs to be
provided.

## Running the application

The utility can be run by calling the executable directly. If no mmap exists, the
application will return 0. If a value has been written to the specified mmap, that
value will be returned:

## Running the tests

Currently there are two tests, one to verify the behavior of no mmap existing, and on
to verify the behavior with an existing memory mapped file. These tests can be run with
the following command:

```console
$ tox -e test
test: commands[0]> pytest <repo_root>\read_port\test\
============================ test session starts =============================
platform win32 -- Python 3.11.1, pytest-7.2.0, pluggy-1.0.0
cachedir: .tox\test\.pytest_cache
rootdir: <repo_root>\read_port
collected 2 items

test\test_read_port.py ..                                               [100%]

============================= 2 passed in 0.04s ============================== 
  test: OK (0.39=setup[0.05]+cmd[0.34] seconds)
  congratulations :) (0.50 seconds)
```

_The timings and versions such might differ._

[tox]: https://tox.wiki/en/latest/index.html
[python]: https://www.python.org/
