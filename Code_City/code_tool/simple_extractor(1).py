cat > simple_extractor.py << 'EOF'
#!/usr/bin/env python3
import os
import shutil
import json
from pathlib import Path

def main():
    print("🚀 Starting Simple Code Extractor...")
    
    # Read the file list
    with open('./logs/targeted_code_files.txt', 'r') as f:
        files = [line.strip() for line in f if line.strip()]
    
    print(f"📁 Found {len(files)} files to organize")
    
    # Create main output structure
    output_base = "./output"
    os.makedirs(output_base, exist_ok=True)
    
    results = {
        'processed': 0,
        'copied': 0,
        'failed': 0,
        'file_types': {}
    }
    
    for file_path in files:
        try:
            # Get file info
            filename = os.path.basename(file_path)
            file_ext = filename.split('.')[-1] if '.' in filename else 'no_ext'
            
            # Count file types
            if file_ext not in results['file_types']:
                results['file_types'][file_ext] = 0
            results['file_types'][file_ext] += 1
            
            # Create organized copy
            # Preserve original folder structure but in organized output
            rel_path = os.path.relpath(file_path, '/storage/emulated/0')
            dest_path = os.path.join(output_base, "organized", rel_path)
            
            # Create destination directory
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Copy file
            shutil.copy2(file_path, dest_path)
            results['copied'] += 1
            
            if results['processed'] % 50 == 0:
                print(f"📊 Progress: {results['processed']}/{len(files)}")
                
        except Exception as e:
            print(f"❌ Failed to copy {file_path}: {e}")
            results['failed'] += 1
            
        results['processed'] += 1
    
    # Save results
    with open(os.path.join(output_base, 'extraction_report.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*50)
    print("📊 EXTRACTION COMPLETE!")
    print("="*50)
    print(f"Total processed: {results['processed']}")
    print(f"Successfully copied: {results['copied']}")
    print(f"Failed: {results['failed']}")
    print("\n📁 File types found:")
    for ext, count in results['file_types'].items():
        print(f"  .{ext}: {count} files")
    
    print(f"\n📁 Output location: {output_base}/organized/")

if __name__ == "__main__":
    main()
EOF