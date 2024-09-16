import os
from constants import (
    import_line,
    main_register_line,
    config_db_file,
    config_db_new_content
)
from cps.plugins.calibre_web_downloader.utils.file_utils import read_file, write_file

def uninstall():
    try:
        remove_from_main_py()
        remove_from_config_db_html()
        print("Plugin uninstalled successfully.")
    except Exception as e:
        print(f"Error during uninstallation: {str(e)}")

def remove_from_main_py():
    main_py_path = os.path.join(os.path.dirname(__file__), '..', '..', 'main.py')
    content = read_file(main_py_path)

    content = content.replace(import_line + '\n', '')
    content = content.replace(main_register_line + '\n', '')

    write_file(main_py_path, content)

def remove_from_config_db_html():
    config_db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', config_db_file)
    content = read_file(config_db_path)
    download_ui = read_file(os.path.join(os.path.dirname(__file__), 'templates', config_db_new_content))

    content = content.replace(download_ui, '')

    write_file(config_db_path, content)

if __name__ == "__main__":
    uninstall()
