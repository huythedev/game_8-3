#!/usr/bin/env python
"""
Fix URL Routes Script

This script fixes url_for references in templates and Python files
to work with the blueprint structure after refactoring.
"""

import os
import re
import sys

def print_status(message):
    """Print a status message with formatting."""
    print(f"[+] {message}")

def print_error(message):
    """Print an error message with formatting."""
    print(f"[!] {message}", file=sys.stderr)

def fix_template_file(file_path):
    """Fix url_for references in template files."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Track if we made changes
    original_content = content
    
    # Fix main routes
    content = re.sub(r'url_for\([\'"]index[\'"](.*?)\)', r'url_for(\'main.index\'\1)', content)
    content = re.sub(r'url_for\([\'"]view_result[\'"](.*?)\)', r'url_for(\'main.view_result\'\1)', content)
    
    # Fix admin routes
    content = re.sub(r'url_for\([\'"]admin_login[\'"](.*?)\)', r'url_for(\'admin.login\'\1)', content)
    content = re.sub(r'url_for\([\'"]admin_dashboard[\'"](.*?)\)', r'url_for(\'admin.dashboard\'\1)', content)
    content = re.sub(r'url_for\([\'"]admin_logout[\'"](.*?)\)', r'url_for(\'admin.logout\'\1)', content)
    content = re.sub(r'url_for\([\'"]add_user[\'"](.*?)\)', r'url_for(\'admin.add_user\'\1)', content)
    content = re.sub(r'url_for\([\'"]delete_user[\'"](.*?)\)', r'url_for(\'admin.delete_user\'\1)', content)
    content = re.sub(r'url_for\([\'"]add_string_pair[\'"](.*?)\)', r'url_for(\'admin.add_string_pair\'\1)', content)
    content = re.sub(r'url_for\([\'"]delete_string_pair[\'"](.*?)\)', r'url_for(\'admin.delete_string_pair\'\1)', content)
    content = re.sub(r'url_for\([\'"]toggle_reaccess[\'"](.*?)\)', r'url_for(\'admin.toggle_reaccess\'\1)', content)
    content = re.sub(r'url_for\([\'"]delete_entry[\'"](.*?)\)', r'url_for(\'admin.delete_entry\'\1)', content)
    content = re.sub(r'url_for\([\'"]change_password[\'"](.*?)\)', r'url_for(\'admin.change_password\'\1)', content)
    
    # Write back only if we changed something
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    
    return False

def fix_route_file(file_path):
    """Fix url_for references in route files."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    original_content = content
    
    # Basic patterns
    content = re.sub(r'url_for\([\'"]index[\'"](.*?)\)', r'url_for(\'main.index\'\1)', content)
    content = re.sub(r'url_for\([\'"]view_result[\'"](.*?)\)', r'url_for(\'main.view_result\'\1)', content)
    content = re.sub(r'url_for\([\'"]admin_login[\'"](.*?)\)', r'url_for(\'admin.login\'\1)', content)
    content = re.sub(r'url_for\([\'"]admin_dashboard[\'"](.*?)\)', r'url_for(\'admin.dashboard\'\1)', content)
    
    # Write back if changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    
    return False

def fix_templates():
    """Fix all template files."""
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    if not os.path.isdir(templates_dir):
        print_error(f"Templates directory not found: {templates_dir}")
        return 0
    
    count = 0
    for root, _, files in os.walk(templates_dir):
        for filename in files:
            if filename.endswith(('.html', '.htm', '.j2', '.jinja', '.jinja2')):
                file_path = os.path.join(root, filename)
                if fix_template_file(file_path):
                    relative_path = os.path.relpath(file_path)
                    count += 1
                    print_status(f"Fixed template: {relative_path}")
    
    return count

def fix_python_files():
    """Fix Python route files."""
    count = 0
    
    # Fix routes in main.py
    main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'routes', 'main.py')
    if os.path.exists(main_path) and fix_route_file(main_path):
        print_status("Fixed routes in main.py")
        count += 1
    
    # Fix routes in admin.py
    admin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'routes', 'admin.py')
    if os.path.exists(admin_path) and fix_route_file(admin_path):
        print_status("Fixed routes in admin.py")
        count += 1
    
    # Fix routes in utils.py
    utils_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils.py')
    if os.path.exists(utils_path) and fix_route_file(utils_path):
        print_status("Fixed routes in utils.py")
        count += 1
    
    return count

def main():
    """Main function"""
    print_status("Starting route fixing script")
    print_status("============================")
    
    # Fix templates
    template_count = fix_templates()
    print_status(f"Fixed {template_count} template files")
    
    # Fix Python files
    py_count = fix_python_files()
    print_status(f"Fixed {py_count} Python files")
    
    if template_count == 0 and py_count == 0:
        print_status("No files needed fixing")
    else:
        total = template_count + py_count
        print_status(f"Successfully updated {total} files")
    
    print_status("Route fixing complete!")
    print_status("You can now restart your application")

if __name__ == "__main__":
    main()
