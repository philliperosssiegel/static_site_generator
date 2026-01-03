from markdown_blocks import markdown_to_html_node, extract_title

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        file_contents = f.read()
    return file_contents

def write_file(content: str, file_path: str):
    with open(file_path, 'w') as f:
        f.write(content)

def generate_page(from_path: str, dest_path: str, template_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source_file, template_file = read_file(from_path), read_file(template_path)

    source_file_html = markdown_to_html_node(source_file).to_html()

    title = extract_title(source_file)

    prepped_html = template_file.replace("{{ Title }}", title).replace("{{ Content }}", source_file_html)

    write_file(prepped_html, dest_path)