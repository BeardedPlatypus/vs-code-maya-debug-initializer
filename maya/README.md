# Maya Debug Initializer - `vscode_debug_initializer` Maya Plug-in

The `vscode_debug_initializer` provides the functionality to start a debug server
inside Maya, with a single Maya command. It provides the necessary dependencies,
`debugpy` for Python 3 and `ptvsd` for Python 2. The port at which the the debug server
should be started, as well as the memory map file name can be customized with flags.

## Usage

The plug-in provides the `mdi_ConfigureDebugServer` command which is a **not** undoable,
**not** queryable, and **not** editable command used to start a debug server inside maya.

### Syntax

```python
mdi_ConfigureDebugServer(
  *args: Sequence[Union[str, int]], 
  waitForDebugger: Boolean=False, 
  mmapName: str="Local\\MDI_MAYA_DEBUG_INFO"
)
```

The first argument provided is interpreted as the port at which the debug server should
be started. If no arguments are provided it defaults to `3000`.

### Return value

`(Optional[int])`: The port at which the debug server was started if successful.

### Flags

| Long Name         | Short Name | Argument Type | Description                            |
| ----------------- | ----- | -------| -------------------------------------------------- |
| `waitForDebugger` | `wdb` | `bool` | Whether to wait for the debugger client to attach. |
| `mmapName`        | `mmn` | `str`  | The name of the mmap in which to store the port.   |

### Examples

```python
# Start the Debug Server at localhost:3000 and continue execution.
cmds.mdi_ConfigureDebugServer()

# Start the Debug Server at localhost:4999 and continue execution.
cmds.mdi_ConfigureDebugServer(4999)

# Start the Debug Server at localhost:3000 and wait for the debugger client to attach.
cmds.mdi_ConfigureDebugServer(waitForDebugger=True)

# Start the Debug Server at localhost:3000 and use the memory map name Local\MY_DEBUG_PORT
cmds.mdi_ConfigureDebugServer(mmapName="Local\\MY_DEBUG_PORT")
```

## Supported Versions

The Maya Debug Initializer plug-in supports Maya 2020, Maya 2022, and Maya 2023. It
works with both Python 2 and Python 3.

## Development

The plug-in follows [the standard Maya plug-in layout][plugin_layout], and is located
in the `vscode_debug_initializer` directory.

### Restoring the externals

The Maya Debug Initializer leverages `debugpy` for Python 3, and `ptvsd` for Python 2.
These dependencies are bundled with the plug-in in the `externals` directory. In order
to restore these dependencies, the following tox command can be called:

```powershell
$ tox -e restore_externals
restore_externals: commands[0]> powershell.exe -Command "Copy-Item -Path \"<path-to-repository>\maya\.tox\restore_externals\Lib\site-packages\debugpy\" -Destination \"<path-to-repository>\maya\vscode_debug_initializer\externals\debugpy\" -Recurse"
restore_externals: commands[1]> powershell.exe -Command "Copy-Item -Path \"<path-to-repository>\maya\.tox\restore_externals\Lib\site-packages\ptvsd\" -Destination \"<path-to-repository>\maya\vscode_debug_initializer\externals\ptvsd\" -Recurse"
  restore_externals: OK (2.55=setup[0.06]+cmd[1.12,1.36] seconds)
  congratulations :) (2.66 seconds)
```

### Running the plug-in in Maya

A Visual Studio Code launch configuration has be provided to start the plug-in within
Maya 2023. When this configuration is started, the `MAYA_MODULE_PATH` is augmented and
the `vscode_debug_initializer_plugin.py` should be available to in the Plug-ins dialog and
through the Script Editor

[plugin_layout]: https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_Distributing_Maya_Plug_ins_DistributingUsingModules_Maya_module_paths_folders_and_html
