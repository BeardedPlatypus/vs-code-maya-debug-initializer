import * as vscode from 'vscode';
import { exec } from "child_process";
import * as path from 'path'

const msDelay = 500;
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));


const retrieveLocalHostWhenReady = async (): Promise<string> => {
	var o: string = "";
	var result: number = 0;

	const configurationSettings = vscode.workspace.getConfiguration('maya-debug-initializer');
	const tag = configurationSettings.get<string>("mmapTag");

	var extensionPath = vscode.extensions.getExtension('BeardedPlatypus.maya-debug-initializer')?.extensionUri.fsPath;

	if (extensionPath == null) {
		return "";
	}

	var executableDir = path.resolve(extensionPath, "externals");

	while(true) {
		exec(`read_port.exe ${tag}`, { cwd: executableDir }, (error, stdout, stderr) => {
			o = stdout;
			result = parseInt(stdout);
		});		

		if (result > 0) {
			return "localhost";
		}

		await delay(msDelay);
	}
}


const getDebugModFile = async (): Promise<string> => {
	var extensionPath = vscode.extensions.getExtension('BeardedPlatypus.maya-debug-initializer')?.extensionUri.fsPath;
	
	if (extensionPath == null) {
		return "";
	}

	return path.resolve(extensionPath, "maya", "vscode_debug_initializer", "modules");
}


export function activate(context: vscode.ExtensionContext) {
	let retrieveLocalHostWhenReadyDisposable = vscode.commands.registerCommand('maya-debug-initializer.retrieveLocalHostWhenReady', retrieveLocalHostWhenReady);
	context.subscriptions.push(retrieveLocalHostWhenReadyDisposable)

	let getDebugModFileDisposable = vscode.commands.registerCommand('maya-debug-initializer.getDebugModFile', getDebugModFile);
	context.subscriptions.push(getDebugModFileDisposable)
}

export function deactivate() {}
