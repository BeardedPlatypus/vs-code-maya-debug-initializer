# Visual Studio Code - Maya Debug Initializer

The Maya Debug Initializer is a small extension which provides some utilities to attach a
Python debugger in Visual Studio Code when developing a Maya Python plug-in.
It provides a Maya plug-in with a command to start a debug server at a specified port
and provides a Visual Studio Code command which returns `"localhost"` when the debug
server in Maya has started. This allows for a Python attach launch configuration to start
and wait for the debug server to be available and then attach itself, thus allowing
debugging in both Maya's GUI as well as Maya's batch executable.

## Requirements

This extension is currently only supported on Windows, and requires a recent Maya
installation. Currently, Maya 2020, 2022, and 2023 are supported.

It assumes the Maya executable can be started with a (Python) start-up command or
script in which the plug-in can be loaded and called.

Other than these requirements, the extension is self-contained, and does not require
any further dependencies.

## Usage

The extension requires two configuration steps in order for the debug initializer to
work within Maya, the Maya plug-in initialization and the Visual Studio Code
`launch.json` configuration. Once these two parts are configured, you can start the
created launch configuration and put the appropriate breakpoints in your source code.

An example set-up can be found [here](/example/) in the extension repository.
A more thorough description can be found in [the README at the repository](/).

### Maya start-up script customization

The main functionality provided by the Maya plug-in is the `mdi_ConfigureDebugServer`
command. This command will start the debug server, and if set, wait for the debugger to
attach.

Assuming we run the tests by calling a `run_tests` method in a bootstrap python script,
we can start the debug server with

```python
def run_tests():
    # Retrieve the debug port, if no port is set we will not start the debug server.
    # We assume the MDI_DEBUG_PORT variable is only set if vs_code_debug_initializer_plugin
    port = int(os.environ.get("MDI_DEBUG_PORT", -1))
    if port > 0:
        cmds.loadPlugin("vscode_debug_initializer_plugin")
        cmds.mdi_ConfigureDebugServer(port, waitForDebugger=True)
```

This will start the debug server at the port specified in the `"MDI_DEBUG_PORT"`
environment variable. If no variable is set, we will skip the debug server
initialization, thus allowing us to run without it as well.

A full example of the bootstrap logic can be found in [the `dcc_bootstrap` directory at the repository](/example/dcc_bootstrap).

### `launch.json` configuration

With the Maya tests configured we need to configure Visual Studio Code to start the
debugger. First we need to add a PowerShell script to run the tests with, in order for
Visual Studio Code to easily start it:

```powershell
param([string]$module_path="", [string]$debug_port="3000")

$Env:MAYA_MODULE_PATH = $module_path
$Env:DEBUG_PORT = $debug_port

# Note that the tests here are run with tox, but this could be replaced with
# powershell command that runs your Maya tests.
tox -e run_test
```

Note that we add `module_path` parameter in order for us to pass the necessary module
path which can then be found by the Maya instance.

Next we create a launch profile to run the before mentioned test environment:

```json
{
    "name": "Run Tests",
    "type": "PowerShell",
    "request": "launch",
    "script": "${workspaceFolder}\\run_tests.ps1",
    "args": ["-module_path ${command:maya-debug-initializer.getDebugModFile}"]
}
```

The `command:maya-debug-initializer.getDebugModFile` will retrieve the `modules` directory
of the Maya plug-in, which will ensure it can be found with the `loadPlugin` command.

Next we create a launch profile to start the debugger:

```json
{
    "name": "Python: Remote Attach",
    "type": "python",
    "request": "attach",
    "justMyCode": false,
    "host": "${command:maya-debug-initializer.retrieveLocalHostWhenReady}",
    "port": 3000,
    "pathMappings": [
        {
            "localRoot": "${workspaceFolder}",
            "remoteRoot": "${workspaceFolder}"
        }
    ]
},
```

Currently, there does not seem a convenient way to have Visual Studio Code commands
return integer values, as such, we need to make sure we match the `port` field with
the value set in the `ps1` script. We then abuse the fact that the
`maya-debug-initializer.retrieveLocalHostWhenReady` will only return `localhost` once
the debug server has been configured in Maya. Thus ensuring we will not attach before
the debug server has been configured.

Lastly, we create a compound profile to start both profiles at the same time:

```json
{
    "name": "Launch Tests with Debug",
    "configurations": ["Run Tox Tests", "Python: Remote Attach"]
}
```

Now we can place a breakpoint anywhere in our tests and start the tests with a debugger
through the created "Launch Tests with Debug" configuration. Our breakpoint should be
hit once maya batch has started.

## Extension Settings

This extension contributes the following settings:

* `maya-debug-initializer.mmapTag`: The tag used for the memory map to communicate whether
  the debug server has started. By default this will be correctly configured to match
  the Maya plug-in.

## Recommended Complimentary Extensions

Several other plug-ins that provide good synergy with the Maya Debug Initializer plug-in.

* [MayaCode][maya_code]: An extension for Visual Studio Code providing MEL
   highlighting, MEL auto-complete and an option to directly run scripts in Maya.

[maya_code]: https://marketplace.visualstudio.com/items?itemName=saviof.mayacode

## Feature Requests and Bug Reports

Feature requests and bug reports can be made directly on [the repository on github](/).
Such reports are welcomed and I will try and address them as quickly as possible.

## Attribution

* <a href="https://www.flaticon.com/free-icons/frog" title="frog icons">Frog icon created by Freepik - Flaticon</a>