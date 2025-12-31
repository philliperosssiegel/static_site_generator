from pathlib import Path

def delete_directory(dir_path: Path):
    shutil.rmtree(dir_path)

def make_dir(dir_path: Path):
    if not os.path.exists:
        os.mkdir(dir_path)
    else:
        raise ValueError(f"Invalid input path={dir_path}, path already exists")

def make_dir_if_not_exists(dir_path: Path):
    if not os.path.exists:
        make_dir(dir_path)

def copy_file(source_dir: Path, source_filename: Path, destination_dir: Path):
    source_full_path = os.path.join(source_dir, source_filename)
    destination_full_path = os.path.join(destination_dir, source_filename)

    if os.path.isfile(source_full_path):
        if os.path.exists(destination_dir):
            pass
            if not os.path.exists(destination_full_path):
                pass
            else:
                raise ValueError(f"File already exists at destination path={destination_full_path}")
        else:
            raise ValueError(f"Destination directory ({destination_dir}) does not exist")
    else: 
        raise ValueError(f"Source file is not a file")

def copy_file_if_not_exists(source_dir: Path, source_filename: Path, destination_dir: Path):
    if os.path.isfile(source_full_path):
        if os.path.exists(destination_dir):
            pass
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
    filename = get_filename(source_path)
    return os.path.join(source_path.replace(filename, ""))

def prepare_destination_path(source_path: Path, destination_dir: Path):
    filename = get_filename(source_path)
    destination_path = os.path.join(destination_dir, filename)
    return destination_path
    
def recursive_directory_copy(source_dir: Path, destination_dir: Path):
    delete_directory(destination_dir)

    stack = os.listdir(source_dir)

    while len(stack) > 0:
        item = stack.pop(0)
        if os.path.isfile(item):
            item_source_dir = get_directory(item)
            item_filename = get_filename(item)
            item_destination_dir = item_source_dir.replace(source_dir, destination_dir)

            dest_item_path = prepare_destination_path(item_source_dir, item_destination_dir)
            copy_file_if_not_exists(item_source_dir, item_filename, item_destination_dir)
        else: #directory
            make_dir_if_not_exists(item)
            stack.extend(os.listdir(item))