#!/usr/bin/env python3
"""
Bulk File Renamer for Ministry of Jerseys - NBA Jerseys Batch 1
This script renames NBA Jerseys images according to the mapping CSV file.
"""

import os
import sys
import csv
import shutil
from pathlib import Path

def rename_files(csv_path, image_directory):
    """
    Rename files based on CSV mapping.
    
    Args:
        csv_path: Path to the CSV file containing old_filename,new_filename
        image_directory: Directory containing the images to rename
    """
    
    # Verify CSV file exists
    if not os.path.exists(csv_path):
        print(f"❌ ERROR: CSV file not found at {csv_path}")
        return False
    
    # Verify image directory exists
    if not os.path.exists(image_directory):
        print(f"❌ ERROR: Image directory not found at {image_directory}")
        return False
    
    print("=" * 60)
    print("MINISTRY OF JERSEYS - BATCH 1 NBA JERSEYS RENAMER")
    print("=" * 60)
    print(f"📂 CSV File: {csv_path}")
    print(f"📂 Image Directory: {image_directory}")
    print()
    
    # Read the CSV mapping
    rename_map = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rename_map.append({
                    'old': row['old_filename'],
                    'new': row['new_filename']
                })
    except Exception as e:
        print(f"❌ ERROR reading CSV: {e}")
        return False
    
    print(f"📋 Found {len(rename_map)} files to rename\n")
    
    # Perform renaming
    success_count = 0
    error_count = 0
    
    for item in rename_map:
        old_path = os.path.join(image_directory, item['old'])
        new_path = os.path.join(image_directory, item['new'])
        
        # Check if old file exists
        if not os.path.exists(old_path):
            print(f"⚠️  SKIP: {item['old']} (file not found)")
            error_count += 1
            continue
        
        # Check if new filename already exists
        if os.path.exists(new_path):
            print(f"⚠️  SKIP: {item['new']} (already exists)")
            error_count += 1
            continue
        
        # Rename the file
        try:
            os.rename(old_path, new_path)
            print(f"✅ {item['old']} → {item['new']}")
            success_count += 1
        except Exception as e:
            print(f"❌ ERROR: {item['old']} - {e}")
            error_count += 1
    
    print()
    print("=" * 60)
    print("RENAMING COMPLETE")
    print("=" * 60)
    print(f"✅ Successfully renamed: {success_count} files")
    print(f"❌ Errors/Skipped: {error_count} files")
    print()
    
    return success_count > 0


if __name__ == "__main__":
    # Default paths (you can modify these)
    default_csv = "nbajerseys_batch1_rename_mapping.csv"
    default_image_dir = "./nba-jerseys-images"
    
    # Check if arguments provided
    if len(sys.argv) == 3:
        csv_file = sys.argv[1]
        image_dir = sys.argv[2]
    elif len(sys.argv) == 1:
        csv_file = default_csv
        image_dir = default_image_dir
        print("ℹ️  Using default paths. To specify custom paths:")
        print(f"   python3 {sys.argv[0]} <csv_file> <image_directory>")
        print()
    else:
        print("Usage:")
        print(f"  python3 {sys.argv[0]} <csv_file> <image_directory>")
        print()
        print("Example:")
        print(f'  python3 {sys.argv[0]} nbajerseys_batch1_rename_mapping.csv "C:/Users/Prashant/Google Drive Data/Final Images/NBA"')
        sys.exit(1)
    
    # Run the renaming
    success = rename_files(csv_file, image_dir)
    
    if success:
        print("🎉 All files renamed successfully!")
        print("Next steps:")
        print("  1. Verify renamed files in your directory")
        print("  2. Upload to GitHub: Ministryofjerseys/moj-images/images/nba-jerseys/")
        print("  3. Generate CSV for website upload")
    else:
        print("⚠️  Renaming completed with errors. Please check the output above.")
        sys.exit(1)
