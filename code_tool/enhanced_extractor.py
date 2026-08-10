# Create the main extraction script
cat > scripts/enhanced_extractor.py << 'EOF'
#!/usr/bin/env python3
import os
import shutil
import json
from pathlib import Path
import re

class CodeExtractor:
    def __init__(self, source_base="/storage/emulated/0", output_base="./output"):
        self.source_base = source_base
        self.output_base = output_base
        self.setup_directories()
        
    def setup_directories(self):
        """Create organized output directory structure"""
        dirs = [
            "github_repos/python",
            "github_repos/shell",
            "github_repos/web",
            "github_repos/config",
            "github_repos/docs",
            "github_repos/unknown",
            "analysis",
            "logs"
        ]
        
        for dir_path in dirs:
            Path(os.path.join(self.output_base, dir_path)).mkdir(parents=True, exist_ok=True)
    
    def categorize_file(self, file_path):
        """Categorize files based on extension and content"""
        ext = file_path.lower().split('.')[-1] if '.' in file_path else ''
        
        # Map extensions to categories
        ext_map = {
            'py': 'python',
            'sh': 'shell', 
            'bash': 'shell',
            'js': 'web',
            'html': 'web',
            'css': 'web',
            'json': 'config',
            'yaml': 'config',
            'yml': 'config',
            'xml': 'config',
            'md': 'docs',
            'txt': 'docs',
            'pdf': 'docs'
        }
        
        return ext_map.get(ext, 'unknown')
    
    def extract_file_info(self, file_path):
        """Extract basic info about a file"""
        try:
            stat = os.stat(file_path)
            return {
                'path': file_path,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'category': self.categorize_file(file_path)
            }
        except Exception as e:
            return {'path': file_path, 'error': str(e)}
    
    def copy_file_organized(self, file_path, file_info):
        """Copy file to organized structure"""
        try:
            rel_path = os.path.relpath(file_path, self.source_base)
            dest_dir = os.path.join(self.output_base, "github_repos", file_info['category'])
            
            # Create relative path structure in destination
            dest_path = os.path.join(dest_dir, rel_path.replace('../', '').replace('./', ''))
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            shutil.copy2(file_path, dest_path)
            return {'success': True, 'destination': dest_path}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_code_file(self, file_path):
        """Basic code analysis for Python files"""
        if not file_path.endswith('.py'):
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            analysis = {
                'file': file_path,
                'lines': len(content.splitlines()),
                'has_functions': bool(re.findall(r'def\s+\w+', content)),
                'has_classes': bool(re.findall(r'class\s+\w+', content)),
                'has_imports': bool(re.findall(r'import\s+\w+', content)),
                'has_comments': bool(re.findall(r'#.*', content))
            }
            return analysis
        except:
            return None
    
    def run_extraction(self, file_list_path):
        """Main extraction process"""
        print("🚀 Starting enhanced code extraction...")
        
        # Read file list
        with open(file_list_path, 'r') as f:
            files = [line.strip() for line in f if line.strip()]
        
        print(f"📁 Found {len(files)} files to process")
        
        results = {
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'analysis': []
        }
        
        # Process each file
        for i, file_path in enumerate(files):
            if i % 100 == 0:
                print(f"📊 Progress: {i}/{len(files)}")
                
            try:
                file_info = self.extract_file_info(file_path)
                copy_result = self.copy_file_organized(file_path, file_info)
                
                # Analyze Python files
                analysis = self.analyze_code_file(file_path)
                if analysis:
                    results['analysis'].append(analysis)
                
                if copy_result['success']:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                    print(f"❌ Failed: {file_path} - {copy_result['error']}")
                    
                results['processed'] += 1
                
            except Exception as e:
                print(f"💥 Error processing {file_path}: {e}")
                results['failed'] += 1
                results['processed'] += 1
        
        # Save results
        self.save_results(results)
        return results
    
    def save_results(self, results):
        """Save extraction results and analysis"""
        # Save basic results
        with open(os.path.join(self.output_base, 'analysis', 'extraction_results.json'), 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save file analysis
        if results['analysis']:
            with open(os.path.join(self.output_base, 'analysis', 'code_analysis.json'), 'w') as f:
                json.dump(results['analysis'], f, indent=2)
        
        # Save summary
        summary = f"""
        📊 EXTRACTION SUMMARY
        ====================
        Total processed: {results['processed']}
        Successful: {results['successful']}
        Failed: {results['failed']}
        Python files analyzed: {len(results['analysis'])}
        """
        
        with open(os.path.join(self.output_base, 'analysis', 'summary.txt'), 'w') as f:
            f.write(summary)
        
        print(summary)

if __name__ == "__main__":
    extractor = CodeExtractor()
    
    # Check if file list exists
    file_list = "./logs/all_code_files.txt"
    if os.path.exists(file_list):
        extractor.run_extraction(file_list)
    else:
        print(f"❌ File list not found: {file_list}")
        print("Please run the find command first to generate the file list.")
EOF