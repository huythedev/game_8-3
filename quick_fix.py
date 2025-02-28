#!/usr/bin/env python
"""
Quick Fix Script

This script quickly updates all URL references in templates
and route files to fix the most common issues after refactoring.
"""

import os
import re
import sys

def fix_file(file_path):
    """Fix url_for references in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remember original for comparison
        original = content
        
        # Standard replacements for templates
        replacements = [
            ('url_for(\'index\'', 'url_for(\'main.index\''),
            ('url_for("index"', 'url_for("main.index"'),
            ('url_for(\'view_result\'', 'url_for(\'main.view_result\''),
            ('url_for("view_result"', 'url_for("main.view_result"'),
            ('url_for(\'admin_login\'', 'url_for(\'admin.login\''),
            ('url_for("admin_login"', 'url_for("admin.login"'),
            ('url_for(\'admin_dashboard\'', 'url_for(\'admin.dashboard\''),
            ('url_for("admin_dashboard"', 'url_for("admin.dashboard"'),
            ('url_for(\'admin_logout\'', 'url_for(\'admin.logout\''),
            ('url_for("admin_logout"', 'url_for("admin.logout"'),
            ('url_for(\'add_user\'', 'url_for(\'admin.add_user\''),
            ('url_for("add_user"', 'url_for("admin.add_user"'),
            ('url_for(\'delete_user\'', 'url_for(\'admin.delete_user\''),
            ('url_for("delete_user"', 'url_for("admin.delete_user"'),
            ('url_for(\'add_string_pair\'', 'url_for(\'admin.add_string_pair\''),
            ('url_for("add_string_pair"', 'url_for("admin.add_string_pair"'),
            ('url_for(\'delete_string_pair\'', 'url_for(\'admin.delete_string_pair\''),
            ('url_for("delete_string_pair"', 'url_for("admin.delete_string_pair"'),
            ('url_for(\'toggle_reaccess\'', 'url_for(\'admin.toggle_reaccess\''),
            ('url_for("toggle_reaccess"', 'url_for("admin.toggle_reaccess"'),
            ('url_for(\'delete_entry\'', 'url_for(\'admin.delete_entry\''),
            ('url_for("delete_entry"', 'url_for("admin.delete_entry"'),
            ('url_for(\'change_password\'', 'url_for(\'admin.change_password\''),
            ('url_for("change_password"', 'url_for("admin.change_password"'),
        ]
        
        # Apply all replacements
        for old, new in replacements:
            content = content.replace(old, new)
        
        # Only write if something changed
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}", file=sys.stderr)
        return False

def quick_fix():
    """Fix templates and Python files in one go."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fixed_files = []

    # Fix template files
    templates_dir = os.path.join(base_dir, 'templates')
    if os.path.isdir(templates_dir):
        for root, _, files in os.walk(templates_dir):
            for filename in files:
                if filename.endswith(('.html', '.j2', '.jinja')):
                    file_path = os.path.join(root, filename)
                    if fix_file(file_path):
                        fixed_files.append(os.path.relpath(file_path, base_dir))

    # Fix Python route files
    routes_dir = os.path.join(base_dir, 'routes')
    if os.path.isdir(routes_dir):
        for root, _, files in os.walk(routes_dir):
            for filename in files:
                if filename.endswith('.py'):
                    file_path = os.path.join(root, filename)
                    if fix_file(file_path):
                        fixed_files.append(os.path.relpath(file_path, base_dir))
    
    # Fix utils.py
    utils_path = os.path.join(base_dir, 'utils.py')
    if os.path.exists(utils_path) and fix_file(utils_path):
        fixed_files.append('utils.py')
    
    return fixed_files

if __name__ == "__main__":
    print("Starting quick fix for URL references...", file=sys.stderr)
    fixed = quick_fix()
    
    if fixed:
        print("\nFixed the following files:", file=sys.stderr)
        for file in fixed:
            print(f"  - {file}", file=sys.stderr)
        print(f"\nTotal: {len(fixed)} files updated", file=sys.stderr)
        print("\nPlease restart your Flask application now.", file=sys.stderr)
    else:
        print("\nNo files needed fixing or no template files found.", file=sys.stderr)
