// extension.js - Real VS Code extension
const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

class EquiNexProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
    }

    refresh() {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element) {
        return element;
    }

    async getChildren() {
        const files = await this.scanWorkspace();
        return files.map(file => new FileItem(
            file.name,
            file.complexity,
            file.health,
            vscode.TreeItemCollapsibleState.None
        ));
    }

    async scanWorkspace() {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) return [];
        
        const files = [];
        for (const folder of workspaceFolders) {
            await this.scanDirectory(folder.uri.fsPath, files);
        }
        return files;
    }

    async scanDirectory(dirPath, files) {
        const entries = await fs.promises.readdir(dirPath, { withFileTypes: true });
        
        for (const entry of entries) {
            const fullPath = path.join(dirPath, entry.name);
            
            if (entry.isDirectory()) {
                if (!entry.name.startsWith('.')) {
                    await this.scanDirectory(fullPath, files);
                }
            } else if (this.isCodeFile(entry.name)) {
                const stats = await fs.promises.stat(fullPath);
                const content = await fs.promises.readFile(fullPath, 'utf8');
                
                files.push({
                    name: entry.name,
                    path: fullPath,
                    lines: content.split('\n').length,
                    complexity: this.calculateComplexity(content),
                    health: this.calculateHealth(content)
                });
            }
        }
    }

    isCodeFile(filename) {
        return /\.[jt]sx?$|\.py$|\.java$|\.cpp$|\.c$|\.php$|\.rb$|\.go$|\.rs$/.test(filename);
    }

    calculateComplexity(content) {
        // Real complexity analysis
        const lines = content.split('\n');
        let complexity = 1; // Base complexity
        
        // Simple heuristic-based complexity calculation
        complexity += (content.match(/if\s*\(/g) || []).length;
        complexity += (content.match(/for\s*\(/g) || []).length;
        complexity += (content.match(/while\s*\(/g) || []).length;
        complexity += (content.match(/catch\s*\(/g) || []).length;
        
        return Math.min(10, complexity);
    }

    calculateHealth(content) {
        const lines = content.split('\n');
        let score = 100;
        
        // Deduct for code smells
        if (content.length > 1000) score -= 10;
        if ((content.match(/\n\s*\n\s*\n/g) || []).length > 5) score -= 5;
        if (content.includes('TODO') || content.includes('FIXME')) score -= 5;
        
        return Math.max(0, score);
    }
}

class FileItem extends vscode.TreeItem {
    constructor(name, complexity, health, collapsibleState) {
        super(name, collapsibleState);
        
        this.description = `Complexity: ${complexity}/10 | Health: ${health}%`;
        this.tooltip = `${name} - Code Health Analysis`;
        
        // Color code based on health
        if (health >= 80) {
            this.iconPath = new vscode.ThemeIcon('circle-filled', new vscode.ThemeColor('charts.green'));
        } else if (health >= 60) {
            this.iconPath = new vscode.ThemeIcon('circle-filled', new vscode.ThemeColor('charts.yellow'));
        } else {
            this.iconPath = new vscode.ThemeIcon('circle-filled', new vscode.ThemeColor('charts.red'));
        }
    }
}