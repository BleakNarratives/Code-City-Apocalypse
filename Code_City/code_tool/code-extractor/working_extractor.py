#!/usr/bin/env python3
import os
import shutil
import json

print("🚀 Starting Working Code Extractor...")

# Read the file list
with open('./logs/targeted_code_files.txt', 'r') as f:
    files = [line.strip() for line in f if line.strip()]

print(f"📁 Found {len(files)} files to process")

# Filter out our own log files and scripts (keep only actual code files)
code_files = [f for f in files if not f.endswith(('target_folders.txt', 'targeted_code_files.txt', 'accessible_files.txt')) and not 'code-extractor' in f]

print(f"📝 Filtered to {len(code_files)} actual code files")

# Create output directory
output_dir = "./extracted_code"
os.makedirs(output_dir, exist_ok=True)

# Process each file
success_count = 0
file_types = {}

for file_path in code_files:
    try:
        # Get file extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in file_types:
            file_types[ext] = 0
        file_types[ext] += 1
        
        # Create destination path
        filename = os.path.basename(file_path)
        dest_path = os.path.join(output_dir, filename)
        
        # Handle duplicate names
        counter = 1
        while os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            dest_path = os.path.join(output_dir, f"{name}_{counter}{ext}")
            counter += 1
        
        # Copy the file
        shutil.copy2(file_path, dest_path)
        print(f"✅ Copied: {filename}")
        success_count += 1
        
    except Exception as e:
        print(f"❌ Failed: {os.path.basename(file_path)} - {e}")

# Save simple report
report = {
    "total_files_found": len(files),
    "code_files_processed": len(code_files),
    "successfully_copied": success_count,
    "file_types": file_types
}

with open(os.path.join(output_dir, "extraction_report.json"), "w") as f:
    json.dump(report, f, indent=2)

print("\n" + "="*50)
print("📊 EXTRACTION COMPLETE!")
print("="*50)
print(f"Total found: {len(files)}")
print(f"Code files: {len(code_files)}")
print(f"Successfully copied: {success_count}")
print(f"File types: {file_types}")
print(f"📍 Output: {output_dir}/")
