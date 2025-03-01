#!/usr/bin/env python3
"""
Maintenance script for the String Transformer application.
Provides a menu-based interface for various maintenance tasks.
"""

import os
import sys
from utils import show_maintenance_menu

def main():
    """Run the maintenance menu"""
    print("String Transformer Application - Maintenance Utility")
    
    # Import app here to avoid circular imports
    try:
        from app import create_app
        app = create_app()
        show_maintenance_menu(app)
    except ImportError as e:
        print(f"Error: Could not import application. {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
