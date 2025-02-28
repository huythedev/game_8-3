#!/usr/bin/env python
"""
Fix Critical Templates Script

This script directly updates the most critical templates that would cause errors
with the Flask application after the blueprint refactoring.
"""

import os

def update_template(file_path, old_content, new_content):
    """Update a template file with new content if it exists."""
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        updated_content = content.replace(old_content, new_content)
        
        if content != updated_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print(f"[+] Updated: {file_path}")
            return True
        else:
            print(f"[*] No changes needed: {file_path}")
            return False
    except Exception as e:
        print(f"[!] Error updating {file_path}: {str(e)}")
        return False

def main():
    """Main function to fix critical templates."""
    print("[+] Starting critical template fix")
    
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    if not os.path.isdir(templates_dir):
        print("[!] Templates directory not found")
        return
    
    # Fix index.html
    index_path = os.path.join(templates_dir, 'index.html')
    update_template(
        index_path,
        'action="{{ url_for(\'index\') }}"',
        'action="{{ url_for(\'main.index\') }}"'
    )
    
    # Fix error.html
    error_path = os.path.join(templates_dir, 'error.html') 
    update_template(
        error_path,
        'href="{{ url_for(\'index\') }}"',
        'href="{{ url_for(\'main.index\') }}"'
    )
    
    # Fix admin_login.html
    login_path = os.path.join(templates_dir, 'admin_login.html')
    update_template(
        login_path,
        'action="{{ url_for(\'admin_login\') }}"',
        'action="{{ url_for(\'admin.login\') }}"'
    )
    update_template(
        login_path,
        'href="{{ url_for(\'index\') }}"',
        'href="{{ url_for(\'main.index\') }}"'
    )
    
    # Fix admin_dashboard.html (just the critical parts that would cause errors)
    dashboard_path = os.path.join(templates_dir, 'admin_dashboard.html')
    update_template(
        dashboard_path,
        'href="{{ url_for(\'admin_logout\') }}"',
        'href="{{ url_for(\'admin.logout\') }}"'
    )
    update_template(
        dashboard_path,
        'action="{{ url_for(\'change_password\') }}"',
        'action="{{ url_for(\'admin.change_password\') }}"'
    )
    
    # Fix no_match.html if it exists
    no_match_path = os.path.join(templates_dir, 'no_match.html')
    if os.path.exists(no_match_path):
        update_template(
            no_match_path,
            'href="{{ url_for(\'index\') }}"',
            'href="{{ url_for(\'main.index\') }}"'
        )
    
    # Fix result.html
    result_path = os.path.join(templates_dir, 'result.html')
    update_template(
        result_path,
        'href="{{ url_for(\'index\') }}"',
        'href="{{ url_for(\'main.index\') }}"'
    )
    
    print("[+] Critical template fixing complete!")

if __name__ == "__main__":
    main()
