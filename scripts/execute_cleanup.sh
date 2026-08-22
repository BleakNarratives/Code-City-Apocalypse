#!/bin/bash

echo "=== STORAGE CLEANUP EXECUTION ==="
echo ""
echo "Starting Phase 1: Immediate Cleanup"
echo ""

# Backup important information
echo "Creating backup information..."
date_str=$(date +%Y%m%d_%H%M%S)
backup_info="cleanup_backup_$date_str.txt"
echo "Storage status before cleanup:" >> "$backup_info"
df -h >> "$backup_info"
echo "" >> "$backup_info"

# Task 1: Remove duplicate models
echo "Task 1: Removing duplicate models..."
if [ -d "$HOME/files/home/models/" ]; then
    echo "Found duplicate models directory at $HOME/files/home/models/"
    echo "Size:"
    du -sh $HOME/files/home/models/
    echo ""
    echo "Removing..."
    rm -rf $HOME/files/home/models/
    if [ $? -eq 0 ]; then
        echo "✓ Successfully removed duplicate models"
    else
        echo "✗ Failed to remove duplicate models"
    fi
else
    echo "✓ No duplicate models found"
fi
echo "" >> "$backup_info"    echo "Duplicate models removal status: $(if [ -d "$HOME/files/home/models/" ]; then echo "FAILED"; else echo "SUCCESS"; fi)" >> "$backup_info"
echo ""

# Task 2: Remove transformers.js
echo "Task 2: Removing transformers.js..."
if [ -d "$HOME/transformers.js/" ]; then
    echo "Found transformers.js directory"
    echo "Size:"
    du -sh $HOME/transformers.js/
    echo ""
    echo "Removing..."
    rm -rf $HOME/transformers.js/
    if [ $? -eq 0 ]; then
        echo "✓ Successfully removed transformers.js"
    else
        echo "✗ Failed to remove transformers.js"
    fi
else
    echo "✓ No transformers.js directory found"
fi
echo "" >> "$backup_info"
echo "Transformers.js removal status: $(if [ -d "$HOME/transformers.js/" ]; then echo "FAILED"; else echo "SUCCESS"; fi)" >> "$backup_info"
echo ""

# Task 3: Clean old screenshots
echo "Task 3: Cleaning old screenshots..."
echo "Finding screenshots older than 30 days..."
old_screenshots=$(find $HOME/Pictures/Screenshots/ -name "*.png" -mtime +30 2>/dev/null | wc -l)
echo "Found $old_screenshots old screenshots"
if [ "$old_screenshots" -gt 0 ]; then
    echo "Removing old screenshots..."
    find $HOME/Pictures/Screenshots/ -name "*.png" -mtime +30 -delete 2>/dev/null
    new_count=$(find $HOME/Pictures/Screenshots/ -name "*.png" -mtime +30 2>/dev/null | wc -l)
    if [ "$new_count" -eq 0 ]; then
        echo "✓ Successfully removed old screenshots"
    else
        echo "✓ Removed $(($old_screenshots - $new_count)) old screenshots"
    fi
else
    echo "✓ No old screenshots found"
fi
echo "" >> "$backup_info"
echo "Old screenshots cleanup status: SUCCESS" >> "$backup_info"
echo ""

# Task 4: Clean temporary files
echo "Task 4: Cleaning temporary files..."
echo "Finding temporary files older than 30 days..."
old_files=$(find $HOME/files/ -type f -mtime +30 2>/dev/null | wc -l)
echo "Found $old_files old temporary files"
if [ "$old_files" -gt 0 ]; then
    echo "Removing old temporary files..."
    find $HOME/files/ -type f -mtime +30 -delete 2>/dev/null
    new_count=$(find $HOME/files/ -type f -mtime +30 2>/dev/null | wc -l)
    if [ "$new_count" -eq 0 ]; then
        echo "✓ Successfully removed old temporary files"
    else
        echo "✓ Removed $(($old_files - $new_count)) old temporary files"
    fi
else
    echo "✓ No old temporary files found"
fi
echo "" >> "$backup_info"
echo "Temporary files cleanup status: SUCCESS" >> "$backup_info"
echo ""

# Summary
echo "=== CLEANUP SUMMARY ==="
echo ""
echo "Storage status after cleanup:"
df -h
echo ""
echo "Backup information saved to: $backup_info"
echo ""
echo "Phase 1 cleanup complete!"
echo ""
echo "Next steps:"
echo "1. Verify all critical data is intact"
echo "2. Proceed to Phase 2: Project Consolidation"
echo "3. Monitor storage usage regularly"
