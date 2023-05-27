<p align='center'><img src="vscode/img/icon.png" align="center" width="50%"></p>

# Maya Debug Initializer

Maya Debug Initializer is a small self-contained plug-in for Visual Studio Code to (more
easily) enable debugging Maya Python plug-ins.

## Motivation

Before venturing into an example set-up, let's quickly go over the motivation of the
"Maya Debug Initializer" and how it works. Maya contains its own Python executable.
This executable will be used to run your Maya python plug-in. Visual Studio Code does
not provide a way to start Maya with a debug server automatically started. This makes
it impossible to automatically connect a debug client as well.

This makes starting a debugger automatically from within Visual Studio Code cumbersome,
especially when used in conjunction with Maya Batch. The "Maya Debug Initializer"
extension provides the functionality to simplify such a set-up significantly. It
contains a Maya plug-in that allows you to start the debug server from within Maya as
well the Visual Studio Code commands to connect to this debug server. Lastly, it
leverages the ability for commands to asynchronously return a value, to only try and
connect to the debug client, once it has been initialized.

This allows you to set-up a debug environment for your Maya Python plugin within Visual
Studio Code with minimum changes to your project.

## Usage

In order to use the Maya Debug Initializer within your project, you will need to slightly
adjust your Maya (test) set-up, and configure Visual Studio Code.

In the following subsections, we will set up a maya plug-in project where unit tests
are run through Maya batch. A similar approach can be taken to start the Maya UI with
a debugger automatically attached.

The example assumes the tests are run with `tox`. If you are using a different
system you will need to adapt the following code to your system of choice.

A complete example of the set-up can be found in [the `example` directory](/example/).

### Configuring Tox

We assume that a tox environment is set up similar to
[the `tox.ini` file in the `example` directory](/example/tox.ini):

```ini
[testenv:run_test]
pass_env =
    MAYA_MODULE_PATH
setenv =
    MAYA_SCRIPT_PATH = {toxinidir}{/}dcc_bootstrap{:}{env:MAYA_SCRIPT_PATH:}
    BEARDEDPLATYPUS_ROOT = {toxinidir}     # Required for the bootstrap to find the setup scripts
allowlist_externals =
    C:\Program Files\Autodesk\Maya2023\bin\mayabatch.exe
commands =
    {[maya]executable} -command bootstrap -noAutoloadPlugins
```

### Configuring Maya

_For more details see [the `maya` README](/maya/)_

The `vscode_debug_initializer` Maya plug-in provides the `mdi_ConfigureDebugServer`
command. This command will start the debug server and if specified will wait for the
debugger to attach.

Assuming we run the tests by calling a `run_tests` method in a bootstrap python script,
we can start the debug server with

```python
def run_tests():
    # Retrieve the debug port, if no port is set we will not start the debug server.
    port = int(os.environ.get("MDI_DEBUG_PORT", -1))
    if port > 0:
        cmds.loadPlugin("vscode_debug_initializer_plugin")
        cmds.mdi_ConfigureDebugServer(port, waitForDebugger=True)
```

This will start the debug server at the port specified in the `"MDI_DEBUG_PORT"`
environment variable. If no variable is set, we will skip the debug server
initialization, thus allowing us to run without it as well.

A full example of the bootstrap logic can be found in [the `dcc_bootstrap` directory](/example/dcc_bootstrap/).

### Configuring Visual Studio Code

_For more details see [the `vscode` README](/vscode/)_

With the Maya tests configured we need to configure Visual Studio Code to start the
debugger. First install the `Maya Debug Initializer` plug-in from the marketplace. This
plugin contains the before mentioned Maya plug-in and any other utilities we need.

First we need to add a PowerShell script to run the tests with, in order for Visual
Studio Code to easily start it. [See `run_tests.ps1`](/example/run_tests.ps1).

```powershell
param([string]$module_path="", [string]$debug_port="3000")

$Env:MAYA_MODULE_PATH = $module_path
$Env:MDI_DEBUG_PORT = $debug_port
tox -e run_test
```

Note that we add `module_path` parameter in order for us to pass the necessary module
path elements to the `tox` environment.

Next we create a launch profile to run the before mentioned `tox` test environment:

```json
{
    "name": "Run Tox Tests",
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

## Development

The development of this plugin can be roughly subdivided in three sections:

* Maya plug-in which starts the debug server within your Maya instance
* The C++ utility to find whether the debug server has been instantiated
* The Visual Studio Code extension used to start the debug client at the correct time

The following subsections detail the requirements to develop, the structure of the
project and how to build the different components.

### Prerequisites

In order to build the complete plug-in you will need the following:

* [tox][tox]: A tool used to manage the different build and test commands.
* [docker][docker]: Used to build the Visual Studio Code extension (alternatively a direct 
   installation of NPM would work as well).
* [gcc][gcc]: C compiler used to compile the memory map utility.

Additionally, in order to manually validate the plug-in you will also need:

* [Visual Studio Code][vscode]: The IDE to run the plug-in in.
* [Maya][maya]: A recent version of Maya (currently 2020, 2022, and 2023 should work).

[tox]: https://tox.wiki/en/latest/
[docker]: https://www.docker.com/
[gcc]: https://gcc.gnu.org/
[vscode]: https://code.visualstudio.com/
[maya]: https://www.autodesk.ca/en/products/maya/features

### Structure of the Project

The plugin can be divided in roughly three sections:

* [`read_port`](/read_port/): The C++ application to retrieve the debug server port
    when it is initialized in Maya.
* [`maya`](/maya/): The Maya Debug Initializer plugin for Maya.
* [`vscode`](/vscode/): The Visual Studio Code extension source code.

Additionally, there is [`example`](/example/) directory which provides a test environment to
validate the behavior of the plug-in.

### Building the Project

In order to build the full Maya Debug Initializer plug-in, you will need to build the
individual components, as discussed in the following sections. This full process is
automated by the Continuous Integration / Continuous Delivery pipeline.

#### `read_port`

The `read_port` can be can be compiled from the "Developer Command Prompt for VS 2022"
with the following command:

```cmd
cl <repo_root>\read_port\src\read_port.c /DAS_EXECUTABLE
```

Which will create a `read_port.exe` at the current location where the command is
executed.

#### `maya`

The source code of the Maya plug-in can be found in
[the `vscode_debug_initializer` directory](/maya/vscode_debug_initializer/). In order
for the plugin to work correctly, you will need to restore the external packages
required by the Maya plug-in, `debugpy` and `ptvsd`. This can be done by calling the
following tox command:

```powershell
tox -e restore-externals
```

Once ran, the plug-in can be used as is.

#### `vscode`

The `vscode` extension is developed in a docker devcontainer, which provides the
necessary environment to compile and package the extension.

First the `maya` plug-in directory [`vscode_debug_initializer`](/maya/vscode_debug_initializer/)
should be copied to a new `maya` directory under the `vscode` directory.

Secondly, the compiled `read_port.exe` should be copied to a new `externals`
directory under the `vscode` directory.

With these files correctly configured, we can build the plugin with the following commands:

```bash
npm run compile
npm run package
```

This will create a `maya-debug-initializer-<version>.vsix` file in the `vscode` directory.
Which can then be used to install the plug-in in Visual Studio Code.

### Testing the environment

With a plug-in build as a `.vsix`, you can install it locally, and test the features.
This can bde done by going to the `Extensions` tab (`Ctrl` `Shift` `X`), clicking
on the `...` in the top right corner of the panel, and selecting "Install from
vsix...".

With the plug-in, as well as Maya installed, you can use the [`example`](/example/) directory
to run the test the plug-in manually.

By adding a breakpoint in [`test_batch.py`](/test/tests/test_batch.py) and running the
"Launch Tests with Debug" configuration, you should hit the breakpoint if all is set up
correctly.

## Additional Recommended Plugins

Several other plug-ins that provide good synergy with the Maya Debug Initializer plug-in.

* [MayaCode][maya_code]: An extension for Visual Studio Code providing MEL
   highlighting, MEL auto-complete and an option to directly run scripts in Maya.

[maya_code]: https://marketplace.visualstudio.com/items?itemName=saviof.mayacode

## Attribution

* <a href="https://www.flaticon.com/free-icons/frog" title="frog icons">Frog icon created by Freepik - Flaticon</a>