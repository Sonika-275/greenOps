import * as vscode from 'vscode';

interface Issue {
    rule_id: string;
    title: string;
    suggestion: string;
    line: number;
    weight: number;
    severity: string;
}

interface AnalyzeResponse {
    green_score: number;
    estimated_co2_kg: number;
    issues: Issue[];
}

const inefficiencyDecorationType = vscode.window.createTextEditorDecorationType({
    backgroundColor: 'rgba(255, 0, 0, 0.12)',
    border: '1px solid rgba(255, 0, 0, 0.5)',
    isWholeLine: true
});

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

                // ✅ Show Green Score + CO2
                vscode.window.showInformationMessage(
                    `Green Score: ${data.green_score} | CO₂: ${data.estimated_co2_kg} kg`
                );

                // ✅ Clear old highlights
                editor.setDecorations(inefficiencyDecorationType, []);

                const decorations: vscode.DecorationOptions[] = [];

                for (const issue of data.issues) {

                    const lineIndex = issue.line - 1;

                    if (lineIndex < 0 || lineIndex >= editor.document.lineCount) {
                        continue;
                    }

                    const lineText = editor.document.lineAt(lineIndex).text;

                    const range = new vscode.Range(
                        lineIndex,
                        0,
                        lineIndex,
                        lineText.length
                    );

                    const hoverMessage = new vscode.MarkdownString(
`### 🚨 ${issue.title}

**Severity:** ${issue.severity}  
**Weight:** ${issue.weight}  

💡 **Optimization:** ${issue.suggestion}`
);

                    hoverMessage.isTrusted = true;

                    decorations.push({
                        range,
                        hoverMessage
                    });
                }

                // ✅ Apply highlights
                editor.setDecorations(inefficiencyDecorationType, decorations);

            } catch (error: any) {
                vscode.window.showErrorMessage(`Error: ${error.message}`);
            }
        }
    );

    context.subscriptions.push(disposable);
}

export function deactivate() {}
