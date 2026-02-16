import * as vscode from 'vscode';

interface AnalyzeResponse {
    green_score: number;
    estimated_co2_kg: number;
}


export function activate(context: vscode.ExtensionContext) {

    const disposable = vscode.commands.registerCommand(
        'greenops-analyzer.analyzeCode',
        async () => {

            const editor = vscode.window.activeTextEditor;

            if (!editor) {
                vscode.window.showErrorMessage('No active editor found');
                return;
            }

            const code = editor.document.getText();

            try {
                const response = await fetch('http://127.0.0.1:8000/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ code })
                });

                if (!response.ok) {
                    throw new Error('Server error');
                }

                const data = await response.json() as AnalyzeResponse;

                vscode.window.showInformationMessage(
                    `Green Score: ${data.green_score} | CO₂: ${data.estimated_co2_kg} kg`
                );

            } catch (error: any) {
                 vscode.window.showErrorMessage(`Error: ${error.message}`);
                }
        }
    );

    context.subscriptions.push(disposable);
}

export function deactivate() {}
