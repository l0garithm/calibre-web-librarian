from pathlib import Path

allowed_categories = {
    'main': Path(__file__).parent.parent.parent,
    'templates': Path(__file__).parent.parent.parent / 'templates',
    # Add other allowed directories as needed
}

def get_file_content(file_dir, filename):
    file_path = allowed_categories[file_dir] / filename
    
    if not file_path.is_file():
        raise FileNotFoundError(f"File {filename} not found in {file_dir}")
    
    return file_path.read_text()

def apply_file_changes(file_category, filename, new_content):
    if file_category not in allowed_categories:
        raise ValueError(f"Access to {file_category} is not allowed")
    
    file_path = allowed_categories[file_category] / filename
    file_path.write_text(new_content)

def insert_content(content, new_line, target_line, before=True):
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if target_line in line:
            if before:
                lines.insert(i, new_line)
            else:
                lines.insert(i + 1, new_line)
            break
    
    return '\n'.join(lines)