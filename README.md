# File Organizer

A small command line tool that organizes files into folders by type, finds large files, and finds duplicate files.

## Requirements

- Python 3.11 or newer

## Usage

Run commands from the folder that contains `organizer.py`.

### Organize a folder

    python organizer.py C:\path\to\folder

Moves each file into a folder based on its type:

| Folder       | File types                                  |
|--------------|---------------------------------------------|
| Image        | .jpg .png .gif .webp .svg .psd              |
| Documents    | .txt .doc .docx .pdf .odt .rtf .pages       |
| Spreadsheets | .xls .xlsx .csv .ods .json .xml             |
| Audio        | .mp3 .wav .flac                             |
| Video        | .mp4 .mkv .mov .avi                         |
| Archives     | .zip .rar .7z .tar .gz                      |
| Code         | .html .htm .css .js .py .java .cpp .sqlite .db |
| System       | .exe .dll .sh .bat                          |

Files with other types are left where they are.

### Preview changes first

    python organizer.py --dry-run C:\path\to\folder

Shows which folders will be created and which files will go in each one. You are then asked whether to apply the changes. Type `y` to continue, or any other key to cancel.

### Find large files

    python organizer.py --large C:\path\to\folder 10mb

Lists files bigger than the given size. Use `kb`, `mb` or `gb` with a whole number, for example `500kb` or `2gb`.

### Find duplicate files

    python organizer.py --duplicates C:\path\to\folder

Lists files that have exactly the same content, even if their names are different.

## Notes

- Only one option can be used at a time.
- All options look at the top level of the folder only, not subfolders.
- If a path has spaces, put it in quotes: "C:\My Folder\Demo"
- Sizes use 1 KB = 1024 bytes, the same as Windows File Explorer.
