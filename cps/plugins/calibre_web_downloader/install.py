import os
import re
import logging
from .constants import (
    main_import_line,
    main_import_line,
    main_import_current_line,
    main_register_line,
    main_blueprint_registration_current_line,
    config_db_file,
    config_db_new_content,
    config_db_old_content
)
from cps.plugins.plugin_utils import get_file_content, apply_file_changes, insert_content
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def install():
    edit_main_py()
    edit_config_db_html()

def edit_main_py():
    # Modify main.py
    print("Starting to modify main.py")
    content = get_file_content('main', 'main.py')
    print(f"Content of main.py: {content[:100]}...")  # Log first 100 characters

    # Add import
    if main_import_line not in content:
        print(f"Adding import line to main.py")
        content = insert_content(
            content,
            main_import_line,
            main_import_current_line,
            before=False
        )
        apply_file_changes('main', 'main.py', content)
    else:
        print(f"Import line already exists in main.py")

    print(f"Finished modifying main.py")

def edit_config_db_html():
    print("Starting to modify config_db.html")
    content = get_file_content('templates', 'config_db.html')
    print(f"Content of config_db.html: {content[:100]}...")  # Log first 100 characters

    # Add download folder UI portion
    download_ui = (Path(__file__).parent / 'templates' / config_db_new_content).read_text()
    print(f"Download UI content: {download_ui}")
    
    if download_ui not in content:
        print(f"Adding download UI to config_db.html")
        content = insert_content(
            content,
            download_ui,
            config_db_old_content,
            before=True
        )
        apply_file_changes('templates', 'config_db.html', content)
    else:
        print(f"Download UI already exists in config_db.html")

    print(f"Finished modifying config_db.html")
