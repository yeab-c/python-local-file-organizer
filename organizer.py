import argparse, sys, os, shutil, re, hashlib
from pathlib import Path





file_categories = (
    (".jpg", ".png", ".gif", ".webp", ".svg", ".psd"),
    (".txt", ".doc", ".docx", ".pdf", ".odt", ".rtf", ".pages"),
    (".xls", ".xlsx", ".csv", ".ods", ".json", ".xml"),
    (".mp3", ".wav", ".flac"),
    (".mp4", ".mkv", ".mov", ".avi"),
    (".zip", ".rar", ".7z", ".tar", ".gz"),
    (".html", ".htm", ".css", ".js", ".py", ".java", ".cpp", ".sqlite", ".db"),
    (".exe", ".dll", ".sh", ".bat")
)

folders = ["Image", "Documents", "Spreadsheets", "Audio", "Video", "Archives", "Code", "System"]

def organize_files(path):
    p = Path(path)   
    list_p = list(p.glob('*'))

    for i in list_p:
        if not i.is_file():
            continue
        ext = i.suffix.lower()
        for idx, j in enumerate(file_categories):
            if ext in j:
                new_folder = create_folder(folders[idx], i.parent)
                shutil.move(str(i), str(new_folder / i.name))
                break
    return "Files Organized"
    
def organization_preview(path):
    p = Path(path)   
    list_p = list(p.glob('*'))
    file_structures = {}

    for file in list_p:
        if not file.is_file():
            continue
        file_extention = file.suffix.lower()
        for idx, extention in enumerate(file_categories):
            if file_extention in extention:
                if not folders[idx] in file_structures.keys():
                    file_structures.setdefault(folders[idx], [])

                file_structures[folders[idx]].append(file.name)
                #new_folder = create_folder(folders[idx], file.parent)
                #shutil.move(str(file), str(new_folder / file.name))
                break

    return file_structures

def create_folder(name, path):
    folder_path = Path(path) / name
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path

# Checks if the argument passed is in path format and exists
def is_valid_path(path):
    valid_path = Path(path).is_dir()

    if valid_path:
        path = Path(path)
        if path.exists():
            return True
        else:
            return False
    else:
        return False

def converter(size):
    value = int(size[:-2])
    unit = size[-2:].lower()

    match unit:
        case "gb":
            return value * 1073741824
        case "mb":
            return value * 1048576
        case "kb":
            return value * 1024

def larger_than(path,byte):
    p = Path(path)
    list_p = list(p.glob('*'))
    big_files = []

    for file in list_p:
        if file.stat().st_size > byte:
            big_files.append(file.name)

    return big_files

def file_hasher(path):
    p = Path(path)
    list_p = list(p.glob('*'))
    files_hashed = {}

    for file in list_p:
        if not file.is_file():
            continue
        with open(file, "rb") as f:
            digest = hashlib.file_digest(f, "sha256")

        file_hash = digest.hexdigest()
        if not file_hash in files_hashed.keys():
            files_hashed.setdefault(file_hash, [file.name])
        else:
            files_hashed[file_hash].append(file.name)

    return files_hashed

# main program
def main():
    parser = argparse.ArgumentParser(description="Helps you organize your file effectively")

    parser.add_argument("path", action="store", nargs="?", help="Organize your file in a given folder")
    parser.add_argument("--dry-run", action="store", help="Shows you what changes it will make in your file structure")
    parser.add_argument("--large", action="store", nargs=2, metavar=("PATH", "SIZE"), help="Shows all files larger than the gives size (takes gb,mb,kb")
    parser.add_argument("--duplicates", action="store", help="Shows files with duplicate content")
    # To be continued
    #parser.add_argument("--history", action="store_true", help="Shows all the path changes made using this program")
    #parser.add_argument("--undo", action="store_true", help="Undo to the previous change")

    args = parser.parse_args()

    arg_values = list(vars(args).items())
    valid = 0

    for i in range(len(arg_values)):
        if arg_values[i][1] != None and arg_values[i][1] != False:
            valid += 1

    if valid > 1:
        print("can only pass one argument")
        sys.exit()


    # Path
    if args.path:
        if not is_valid_path(args.path):
            print("invalid path")
            sys.exit()

        print(organize_files(args.path))

    # --dry-run
    if args.dry_run:
        if not is_valid_path(args.dry_run):
            print("invalid path")
            sys.exit()

        file_structures = organization_preview(args.dry_run)
        if len(file_structures.keys()) == 0:
            print("This folder has no file")
        else:
            print(f"New {len(file_structures.keys())} folders will be created\n")
            for folder in file_structures:
                print(folder)
                for file in file_structures[folder]:
                    print(f"---------{file}")
                print("\n\n")
        
        print("Do you want to make these changes?")

        dry_run_response = input("Enter 'y' to make changes or any other key to abort: ").lower()
        if dry_run_response == "y":
            print(organize_files(args.dry_run))
        else:
            print("No changes made")
    
    # --large
    if args.large:
        path, size = args.large
        if not is_valid_path(path):
            print("invalid path")
            sys.exit()
        size_obj = re.compile(r"(\d+(gb|mb|kb))", re.IGNORECASE)
        is_size = size_obj.findall(size)

        if is_size:
            byte = converter(size)
            big_files = larger_than(path,byte)
        else:
            print("Invalid Size")
            sys.exit()

        if len(big_files) == 0:
            print(f" No files greater than {size} found")
        else:    
            for file in big_files:
                print(file)

    # --duplicates
    if args.duplicates:
        if not is_valid_path(args.duplicates):
            print("invalid path")
            sys.exit()
        
        hashed_dict = file_hasher(args.duplicates)

        num_duplicates = 0

        for names in hashed_dict.values():
            if len(names) > 1:
                print(f"Files {names} are duplicates\n")
                num_duplicates += 1

        if num_duplicates == 0:
            print("No duplicates found")



if __name__ == "__main__":
    main()

