#!/usr/bin/env python3
"""
Notebook Fixer - Ensures the Jupyter notebook is properly formatted for GitHub upload
This script fixes common issues that cause notebooks to appear empty on GitHub.
"""

import json
import os
import sys
from pathlib import Path

def fix_notebook_encoding(notebook_path):
    """Fix notebook encoding and formatting issues"""
    
    print(f"🔧 Fixing notebook: {notebook_path}")
    
    try:
        # Read the notebook with UTF-8 encoding
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = f.read()
        
        # Parse as JSON
        notebook_data = json.loads(notebook_content)
        
        # Validate notebook structure
        if 'cells' not in notebook_data:
            print("❌ Invalid notebook structure: missing 'cells' key")
            return False
        
        print(f"✅ Notebook has {len(notebook_data['cells'])} cells")
        
        # Ensure metadata exists
        if 'metadata' not in notebook_data:
            notebook_data['metadata'] = {}
        
        # Ensure nbformat and nbformat_minor exist
        if 'nbformat' not in notebook_data:
            notebook_data['nbformat'] = 4
        if 'nbformat_minor' not in notebook_data:
            notebook_data['nbformat_minor'] = 4
        
        # Clean up cells
        for i, cell in enumerate(notebook_data['cells']):
            # Ensure cell has required fields
            if 'cell_type' not in cell:
                print(f"⚠️  Cell {i} missing cell_type")
                continue
                
            if 'source' not in cell:
                cell['source'] = []
            elif isinstance(cell['source'], str):
                # Convert string to list of lines
                cell['source'] = cell['source'].splitlines(keepends=True)
            
            if 'metadata' not in cell:
                cell['metadata'] = {}
            
            # For code cells, ensure outputs and execution_count exist
            if cell['cell_type'] == 'code':
                if 'outputs' not in cell:
                    cell['outputs'] = []
                if 'execution_count' not in cell:
                    cell['execution_count'] = None
        
        # Write back with proper formatting
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Notebook formatting fixed successfully")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return False
    except UnicodeDecodeError as e:
        print(f"❌ Unicode decode error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def validate_notebook(notebook_path):
    """Validate the notebook file"""
    
    print(f"🔍 Validating notebook: {notebook_path}")
    
    # Check if file exists
    if not os.path.exists(notebook_path):
        print(f"❌ Notebook file not found: {notebook_path}")
        return False
    
    # Check file size
    file_size = os.path.getsize(notebook_path)
    if file_size == 0:
        print("❌ Notebook file is empty")
        return False
    
    print(f"📏 File size: {file_size:,} bytes")
    
    # Try to parse as JSON
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
        
        # Check structure
        if 'cells' not in notebook_data:
            print("❌ Invalid notebook: missing 'cells'")
            return False
        
        cells = notebook_data['cells']
        print(f"✅ Valid notebook with {len(cells)} cells")
        
        # Count cell types
        cell_types = {}
        for cell in cells:
            cell_type = cell.get('cell_type', 'unknown')
            cell_types[cell_type] = cell_types.get(cell_type, 0) + 1
        
        print("📊 Cell types:")
        for cell_type, count in cell_types.items():
            print(f"   {cell_type}: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def create_backup(notebook_path):
    """Create a backup of the notebook"""
    
    backup_path = notebook_path + '.backup'
    
    try:
        import shutil
        shutil.copy2(notebook_path, backup_path)
        print(f"💾 Backup created: {backup_path}")
        return True
    except Exception as e:
        print(f"⚠️  Could not create backup: {e}")
        return False

def main():
    """Main function"""
    
    print("🔧 Notebook Fixer for GitHub Upload")
    print("=" * 40)
    
    # Find notebook file
    notebook_path = "custom_research_assistant.ipynb"
    
    if not os.path.exists(notebook_path):
        print(f"❌ Notebook file not found: {notebook_path}")
        print("Please ensure you're running this script from the project directory")
        sys.exit(1)
    
    # Create backup
    create_backup(notebook_path)
    
    # Validate current notebook
    if not validate_notebook(notebook_path):
        print("❌ Notebook validation failed")
        sys.exit(1)
    
    # Fix encoding and formatting
    if fix_notebook_encoding(notebook_path):
        print("✅ Notebook fixed successfully")
        
        # Validate again
        if validate_notebook(notebook_path):
            print("✅ Final validation passed")
            print("🚀 Notebook is ready for GitHub upload!")
        else:
            print("❌ Final validation failed")
            sys.exit(1)
    else:
        print("❌ Failed to fix notebook")
        sys.exit(1)

if __name__ == "__main__":
    main()
