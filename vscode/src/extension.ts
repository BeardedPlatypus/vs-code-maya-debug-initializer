import * as vscode from 'vscode';
import { exec } from "child_process";
import * as path from 'path'
import * as net from 'net';

const msDelay = 500;
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));


const retrieveLocalHostWhenReady = async (): Promise<string> => {
	const configurationSettings = vscode.workspace.getConfiguration('maya-debug-initializer');
	const tag = configurationSettings.get<string>("mmapTag");

	var extensionPath = vscode.extensions.getExtension('BeardedPlatypus.maya-debug-initializer')?.extensionUri.fsPath;

	if (extensionPath == null) {
		return "";
	}

	var executableDir = path.resolve(extensionPath, "externals");

	await new Promise<void>((resolve) => {
        exec(`reset_port.exe ${tag}`, { cwd: executableDir }, () => resolve());
    });

	while(true) {
		const result = await new Promise<number>((resolve) => {
			exec(`read_port.exe ${tag}`, { cwd: executableDir }, (error, stdout, stderr) => {
				resolve(parseInt(stdout) || 0);
			});		
		});

		if (result > 0) {
			await delay(msDelay);
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
