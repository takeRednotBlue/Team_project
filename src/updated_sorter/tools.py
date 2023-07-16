import re
import os
import shutil
from pathlib import Path
from datetime import datetime

def translitterate(text: str) -> str:
    TRANS_DICT = {}

    cyrillic = [
        'а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з', 'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 
        'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ю', 'я'
        ]
    
    latin = [
        'a', 'b', 'v', 'h', 'g', 'd', 'e', 'ie', 'zh', 'z', 'y', 'i', 'i', 'i', 'k', 'l', 'm', 'n', 
        'o', 'p', 'r', 's', 't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'iu', 'ia'
        ]

    for cyr, lat in zip(cyrillic, latin):
        TRANS_DICT[cyr] = lat
        TRANS_DICT[cyr.upper()] = lat.capitalize()

    trans_dict = str.maketrans(TRANS_DICT)
    new_text = text.translate(trans_dict)
    return new_text


def normalize(path: str) -> tuple:
    '''Transliterates from cyrillic stem of the file and replace symbols
    other than latin letters and numbeіr with "_". The result is renamed Paths of the files.
    Returns tuple which contain list with pairs of paths before and after normalization and integer
    number of normalized files'''
    log_list = []
    count_normalized_files = 0
    max_attempts = 100
    add_suffix = 1

    path = Path(path)
    files = [file for file in get_all_items(path)]

    for file in files:
        pattern = r"\W"
        new_stem = re.sub(pattern, "_", translitterate(file.stem))
        new_path = file.with_stem(new_stem)
        
        if file.name != new_path.name:
            # Handles cases when file exists in order not to rewrite it
            while new_path.exists() and add_suffix <= max_attempts:
                new_name = f"{new_stem}_{add_suffix}{file.suffix}"
                new_path = file.with_name(new_name)
                add_suffix += 1
                
            if add_suffix > max_attempts:
                raise Exception("Could not move file, maximum number of attempts reached")
                       
            count_normalized_files += 1
            log_list.append((file, new_path))
            file.rename(new_path)

    return log_list, count_normalized_files

            



def new_dir(path: Path, newDirName: str) -> Path:
    '''Makes new directory in the given path. Skips if directory exists.'''
    newDir = path / newDirName
    newDir.mkdir(exist_ok=True)
    return newDir

def get_all_items(path: Path):
        '''Generator that yields files recursively from dirs and subdirs'''
        for item in path.iterdir():
            if item.is_dir():
                yield from get_all_items(item)
            else:
                yield item

count_removed_dirs = 0
def remove_empty_dirs(path: str|Path) -> int:
    """Deletes empty dirs recursively. Returns integer number of removed dirs."""
    global count_removed_dirs

    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            remove_empty_dirs(os.path.join(root, dir))
        if not dirs and not files:
            os.rmdir(root) # os.rmdir() removes only if dir is empty
            count_removed_dirs += 1

    return count_removed_dirs 



def move_to_folder(file: Path, destPath: Path) -> Path:
    """Moves file to the given destination folder.
    If a file with the same name already exists in the destination folder, appends 
    a suffix to the file name until a unique name is found. Returns new path of the file."""
    
    max_attempts = 100
    add_suffix = 1
    
    dest_file_path = destPath / file.name
    # Handles cases when file exist in order not to rewrite it
    while dest_file_path.exists() and add_suffix <= max_attempts:
        add_suffix += 1
        dest_file_path = destPath / f"{file.stem}_{add_suffix}{file.suffix}"
    
    if add_suffix > max_attempts:
        raise Exception("Could not move file, maximum number of attempts reached")
    
    file.rename(dest_file_path)
    return dest_file_path            
    
def sort_dir(path: str|Path, unpackArch=True) -> tuple:
    '''Take files from the given path and move them acording to the suffix into the respective dir. Unpacks
    archives with suffixes ".zip", ".tar", ".gztar", ".bztar", ".xztar" if else not given. Returns tuple 
    which contains list with pairs of paths before and after sorting and integer number of unpacked archives.
    '''
    file_formats = {
    'Audio': [
        '.mp3', '.wav', '.aac', '.wma', '.ogg', '.flac', '.alac', '.aiff', '.ape', '.au', 
        '.m4a', '.m4b', '.m4p', '.m4r', '.mid', '.midi', '.mpa', '.mpc', '.oga', '.opus', 
        '.ra', '.ram', '.tta', '.weba'
        ],
    'Video': [
        '.mp4', '.avi', '.mkv', '.wmv', '.mov', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', 
        '.3gp', '.3g2', '.m2ts', '.mts', '.vob', '.ogv', '.mxf', '.divx', '.f4v', '.h264'
        ],
    'Images': [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.svg', '.webp', '.eps', 
        '.raw', '.cr2', '.nef', '.dng', '.orf', '.arw', '.pef', '.raf', '.sr2', '.kdc', '.mos', 
        '.mrw', '.dcr', '.x3f', '.erf', '.mef', '.pcx'
        ],
    'Documents': [
        '.dot', '.odi', '.sxc', '.sxd', '.doc', '.txt', '.odf', '.sxw', '.odt', '.pdf', '.sxg', 
        '.ott', '.odg', '.stw', '.sxi', '.stc', '.dotm', '.md', '.odc', '.docx', '.dotx', '.rtf'
        ],
    'Spreadsheets': [
        '.xls', '.xlsx', '.csv', '.xlsm', '.xlt', '.xltx', '.xlsb', '.numbers', '.ods'
        ],
    'Presentations': [
        '.ppt', '.pptx', '.key', '.odp', '.pps', '.ppsx', '.pot', '.potx', '.potm'
        ],
    'Archives': [
        '.zip', '.rar', '.tar.gz', '.7z', '.tar', '.tgz', '.bz2', '.dmg', '.iso', '.gz', '.jar', 
        '.cab', '.z', '.tar.bz2', '.xz'
        ],
    'Programs': [
        '.exe', '.apk', '.app', '.msi', '.deb', '.rpm', '.bat', '.sh', '.com', '.gadget', '.vb', 
        '.vbs', '.wsf'
        ],
    'Code': [
        '.py', '.java', '.js', '.html', '.css', '.cpp', '.c', '.php', '.xml', '.rb', '.pl', '.swift', 
        '.h', '.hpp', '.cs', '.m', '.mm', '.kt', '.dart', '.go', '.lua', '.r', '.ps1'
        ],
    'Database': [
        '.sql', '.db', '.mdb', '.accdb', '.sqlitedb', '.dbf', '.dbs', '.myd', '.frm', '.sqlite'
        ],
    'Ebook': [
        '.epub', '.azw', '.azw3', '.fb2', '.ibooks', '.lit', '.mobi', '.pdb'
        ]
    }

    log_list = []
    unpack_counter = 0
    path = Path(path)
    files = [file for file in get_all_items(path)]

    for file in files:
        for categ, formats in file_formats.items():
            if file.suffix.lower() in formats:

                if categ == "Archives" and unpackArch == True and file.suffix in {".zip", ".tar", ".gztar", 
                                                                                  ".bztar", ".xztar"}:
                    # Avoid backup archive if such was made
                    if file.stem == path.name + "_backup":
                        break
                    dest_to_unpack = new_dir(path, categ)
                    unpack_arch_and_remove(file, dest_to_unpack)
                    unpack_counter += 1
                    break
                else:
                    dest_dir = new_dir(path, categ)
                    new_file_path = move_to_folder(file, dest_dir)
                    log_list.append((file, new_file_path))
                    break
        
        else:
            dest_dir = new_dir(path, "Unknown")
            new_file_path = move_to_folder(file, dest_dir)
            log_list.append((file, new_file_path))

    return log_list, unpack_counter
           


def dirs_info(path):
    '''Output result of the script into terminal in table format'''
    path = Path(path)
    files_count = 0
    dirs_count = 0
    suffixes_count = 0

    print("-"*117)
    print("|{:^15}|{:^7}|{:^7}|{:^83}|".format("Dir name", "Files", "Subdirs", "Suffixes"))
    print("-"*117)

    for root, dirs, files in os.walk(path):
        root = Path(root)
        # Display info of only sorted in dirs
        if root.parent == path:
            suffixes = list(set([Path(file).suffix.lower() for file in files]))
            suffixes_str = ", ".join(map(repr, suffixes))
            # Handles display of suffixes when not enough space in one row of the table
            if len(suffixes_str) > 83:
                suffixes_line = suffixes_str[:83]
                print('|{:<15}|{:^7}|{:^7}|{:<83}|'.format(root.name, len(files), len(dirs), suffixes_line))
                n = 83
                while len(suffixes_line) > 82:
                    suffixes_line = suffixes_str[n:n+83]
                    print('|{_:<15}|{_:^7}|{_:^7}|{suf:<83}|'.format(_='', suf=suffixes_line))
                    n += 83
            else:
                print('|{:<15}|{:^7}|{:^7}|{:<83}|'.format(root.name, len(files), len(dirs), suffixes_str))

            files_count += len(files)
            dirs_count += len(dirs)
            suffixes_count += len(suffixes)
        else: 
            continue

    print("-"*117)
    print(f'|{"Total:":<15}|{files_count:^7}|{dirs_count:^7}|{suffixes_count:^83}|')
    print("-"*117)

def files_amount(path):
    
    path = Path(path)
    items = [item for item in path.rglob("*")]
    files_amount = len([file for file in items if file.is_file()])
    return files_amount

def make_report(destPath: str|Path, backup):
    '''Writes report into a file'''
    destPath = Path(destPath)
    files_count = 0
    dirs_count = 0
    suffixes_count = 0

    with open(destPath / "report.txt", 'w') as rep:
        time = datetime.now().isoformat(sep=' ', timespec='seconds')
        rep.write(
f'''\r
Time of sorting: {time}
Backup: {backup}
Path: {destPath}\n\n
''')
        rep.write("-"*117+"\n")
        rep.write("|{:^15}|{:^7}|{:^7}|{:^83}|\n".format("Dir name", "Files", "Subdirs", "Suffixes",))
        rep.write("-"*117+"\n")
        
        for root, dirs, files in os.walk(destPath):
            root = Path(root)
            # Displays info only about dirs in root path
            if root.parent == destPath:
                suffixes = list(set([Path(file).suffix.lower() for file in files]))
                suffixes_str = ", ".join(map(repr, suffixes))
                # Handles display of suffixes when not enough space in one row of the table
                if len(suffixes_str) > 83:
                    suffixes_line = suffixes_str[:83]
                    rep.write('|{:<15}|{:^7}|{:^7}|{:<83}|\n'.format(root.name, len(files), len(dirs), suffixes_line))
                    n = 83
                    while len(suffixes_line) > 82:
                        suffixes_line = suffixes_str[n:n+83]
                        rep.write('|{_:<15}|{_:^7}|{_:^7}|{suf:<83}|\n'.format(_='', suf=suffixes_line))
                        n += 83
                else:
                    rep.write('|{:<15}|{:^7}|{:^7}|{:<83}|\n'.format(root.name, len(files), len(dirs), suffixes_str))

                files_count += len(files)
                dirs_count += len(dirs)
                suffixes_count += len(suffixes)
            else: 
                continue

        rep.write("-"*117+"\n")
        rep.write(f'|{"Total:":<15}|{files_count:^7}|{dirs_count:^7}|{suffixes_count:^83}|\n')
        rep.write("-"*117+"\n")


def unpack_arch_and_remove(file: Path, dest: Path):
    '''Unpacks archive to the given dir and removes it after.'''
    destDir = dest / file.stem
    shutil.unpack_archive(file, destDir)
    file.unlink()

def create_backup_copy(path: str|Path):
    '''Makes achive and moves it inside given path as backup before sorting.'''
    path = Path(path)
    archive_name = path.parent / f"{path.name}_backup"
    shutil.make_archive(archive_name, 'zip', path)
    back_up_path = archive_name.with_suffix(".zip")
    back_up_path.rename(path / f"{archive_name.name}.zip")


