import os
import shutil

from pathlib import Path

def delete_directory(dir_path: Path):
    shutil.rmtree(dir_path)

def delete_directory_if_not_exists(dir_path: Path):
    if os.path.exists(dir_path):
        delete_directory(dir_path)

def make_dir(dir_path: Path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        raise ValueError(f"Invalid input path={dir_path}, path already exists")

def make_dir_if_not_exists(dir_path: Path):
    if not os.path.exists(dir_path):
        make_dir(dir_path)

def copy_file(source_dir: Path, source_filename: Path, destination_dir: Path):
    source_full_path = os.path.join(source_dir, source_filename)
    destination_full_path = os.path.join(destination_dir, source_filename)

    if os.path.isfile(source_full_path):
        if os.path.exists(destination_dir):
            if not os.path.exists(destination_full_path):
                shutil.copy2(source_full_path, destination_full_path)
            else:
                raise ValueError(f"File already exists at destination path={destination_full_path}")
        else:
            raise ValueError(f"Destination directory ({destination_dir}) does not exist")
    else: 
        raise ValueError(f"Source file is not a file")

def copy_file_if_not_exists(source_dir: Path, source_filename: Path, destination_dir: Path):
    source_full_path = os.path.join(source_dir, source_filename)
    destination_full_path = os.path.join(destination_dir, source_filename)

    if os.path.isfile(source_full_path):
        if os.path.exists(destination_dir):
            if not os.path.exists(destination_full_path):
                copy_file(source_dir, source_filename, destination_dir)
        else:
            make_dir(destination_dir)
            copy_file(source_dir, source_filename, destination_dir)
    else: 
        raise ValueError(f"Source file is not a file")

def get_filename(source_path: Path) -> str:
    return os.path.basename(source_path)

def get_directory(source_path: Path) -> Path:
    if os.path.isfile(source_path):
        filename = get_filename(source_path)
        return os.path.join(source_path.replace(filename, ""))
    else:
        return source_path

def prepare_destination_path(source_path: Path, destination_dir: Path):
    filename = get_filename(source_path)
    destination_path = os.path.join(destination_dir, filename)
    return destination_path
    
def recursive_directory_copy(source_dir: Path, destination_dir: Path):
    delete_directory_if_not_exists(os.path.abspath(destination_dir))
    make_dir_if_not_exists(os.path.abspath(destination_dir))

    stack = [os.path.abspath(os.path.join(os.path.abspath(source_dir), item)) for item in os.listdir(source_dir)]

    while len(stack) > 0:
        item = stack.pop(0)
        
        if os.path.isfile(os.path.abspath(item)):
            item_source_dir = get_directory(item)
            item_filename = get_filename(item)
            item_destination_dir = item_source_dir.replace(os.path.abspath(source_dir), os.path.abspath(destination_dir))

            dest_item_path = prepare_destination_path(item_source_dir, item_destination_dir)
            copy_file_if_not_exists(item_source_dir, item_filename, item_destination_dir)
        else: #directory
            item_source_dir = get_directory(item)
            make_dir_if_not_exists(item_destination_dir)
            new_items = os.listdir(os.path.abspath(item))
            stack.extend([os.path.join(item_source_dir, item) for item in os.listdir(item_source_dir)])