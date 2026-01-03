import os

from markdown_blocks import markdown_to_html_node, extract_title
from copystatic import make_dir_if_not_exists, get_filetype, get_filename


def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        file_contents = f.read()
    return file_contents

def write_file(content: str, file_path: str):
    with open(file_path, 'w') as f:
        f.write(content)

def generate_page(from_path: str, dest_path: str, template_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source_file, template_file = read_file(from_path), read_file(template_path)

    source_file_html = markdown_to_html_node(source_file).to_html()

    title = extract_title(source_file)

    prepped_html = template_file.replace("{{ Title }}", title)
    prepped_html = prepped_html.replace("{{ Content }}", source_file_html)
    prepped_html = prepped_html.replace('href="/', f'href="{basepath}')
    prepped_html = prepped_html.replace('src="/', f'src="{basepath}')

    make_dir_if_not_exists(os.path.dirname(dest_path))
    write_file(prepped_html, dest_path)

def generate_pages_recursive(dir_path_content: str, dest_dir_path: str, template_path: str, basepath: str):
    for item in os.listdir(dir_path_content):
        full_item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(full_item_path):
            if get_filetype(full_item_path) == "md":
                filename_no_ext = get_filename(item).split(".")[0]
                new_filename = f"{filename_no_ext}.html"
                generate_page(full_item_path, os.path.join(dest_dir_path, new_filename), template_path, basepath)
        else: #item is a directory
            make_dir_if_not_exists(os.path.join(dest_dir_path, item))
            generate_pages_recursive(full_item_path, os.path.join(dest_dir_path, item), template_path, basepath)