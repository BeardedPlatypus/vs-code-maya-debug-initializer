param([string]$module_path="", [string]$debug_port="3000")

$Env:MAYA_MODULE_PATH = $module_path
$Eenv:MDI_DEBUG_PORT = $debug_port
tox -e run_test