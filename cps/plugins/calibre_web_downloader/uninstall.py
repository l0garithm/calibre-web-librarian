import os
from .constants import (
    main_import_line,
    main_register_line,
    config_db_file,
    config_db_new_content
)
from cps.plugins.plugin_utils import get_file_content, apply_file_changes, insert_content

def uninstall():
    try:
        remove_from_main_py()
        remove_from_config_db_html()
        print("Plugin uninstalled successfully.")
    except Exception as e:
        print(f"Error during uninstallation: {str(e)}")

def remove_from_main_py():
    main_py_path = os.path.join(os.path.dirname(__file__), '..', '..', 'main.py')
    content = get_file_content('.', 'main.py')

    content = content.replace(main_import_line + '\n', '')
    content = content.replace(main_register_line + '\n', '')

    apply_file_changes('.', 'main.py', content)

def remove_from_config_db_html():
    config_db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', config_db_file)
    content = get_file_content('.', config_db_file)
    download_ui = get_file_content('.', config_db_new_content)

    content = content.replace(download_ui, '')

    apply_file_changes('.', config_db_file, content)

if __name__ == "__main__":
    uninstall()
