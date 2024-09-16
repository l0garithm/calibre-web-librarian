import os
import re
from constants import (
    import_line,
    main_import_line,
    main_import_current_line,
    main_register_line,
    main_blueprint_registration_current_line,
    config_db_file,
    config_db_new_content,
    config_db_old_content
)
from cps.plugins.calibre_web_downloader.utils.file_utils import insert_content, read_file, write_file

def install():
    try:
        edit_main_py()
        edit_config_db_html()
        print("Plugin installed successfully.")
    except Exception as e:
        print(f"Error during installation: {str(e)}")

def edit_main_py():
    # Modify main.py
    content = read_file('main.py', '..')

    # Add import
    if import_line not in content:
        content = insert_content(
            content,
            main_import_line,
            main_import_current_line,
            before=False
        )

    # Add blueprint registration
    if main_register_line not in content:
        content = insert_content(
            content,
            main_register_line,
            main_blueprint_registration_current_line,
            before=False
        )
    write_file('../../main.py', content)

def edit_config_db_html():
    content = read_file('config_db.html', 'templates')

    # Add download folder UI portion
    download_ui = read_file(config_db_new_content, 'templates')
    if download_ui not in content:
        content = insert_content(
            content,
            download_ui,
            config_db_old_content,
            before=True
        )
    
    write_file('../../templates/config_db.html', content)