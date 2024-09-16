import os


def read_file(file_name, folder):
    file_path = os.path.join(os.path.dirname(__file__), '..', folder, file_name)
    with open(file_path, 'r') as file:
        return file.read().strip()


def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def insert_content(content, new_content, search_string, before=False):
    if before:
        updated_content = content.replace(search_string, f"{new_content}\n{search_string}")
    else:
        updated_content = content.replace(search_string, f"{search_string}\n{new_content}")
    return(updated_content)