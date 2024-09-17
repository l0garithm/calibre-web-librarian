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

# def insert_content(content, new_line, target_line, before=True):
#     lines = content.split('\n')
    
#     for i, line in enumerate(lines):
#         if target_line in line:
#             if before:
#                 lines.insert(i, new_line)
#             else:
#                 lines.insert(i + 1, new_line)
#             break
    
#     result = '\n'.join(lines)
#     return result

def insert_content(content, new_content, target_content, before=True):
    print(f"Inserting new content: {new_content}")
    print(f"Target content: {target_content}")
    print(f"Inserting before: {before}")
    
    if new_content not in content:
        if target_content.strip() in content.strip():
            if before:
                print(f"Inserting before target content")
                content = content.replace(target_content.strip(), new_content + '\n' + target_content)
            else:
                print(f"Inserting after target content")
                content = content.replace(target_content, target_content + '\n' + new_content)
        else:
            print(f"Target content not found in the file")
    else:
        print(f"New content already exists in the file")
    
    print(f"Content after insertion: {content}")
    return content
