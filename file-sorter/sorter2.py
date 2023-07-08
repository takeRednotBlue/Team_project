import os
import sys
import shutil
from colorama import init
from colorama import Fore, Back

init()


def list_all_files_in_rootdir(rootdir, lst_all_files):
    for it in os.scandir(rootdir):
        if it.is_file():
            lst_all_files.append(it)
        elif it.is_dir():
            list_all_files_in_rootdir(it, lst_all_files)
    return lst_all_files


def create_new_folders_in_rootdir(rootdir, dir_category_dict):
    for key in dir_category_dict.keys():
        os.makedirs(os.path.join(rootdir, key), exist_ok=True)
    os.makedirs(os.path.join(rootdir, "uknown_extension"), exist_ok=True)


def normalize(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a",
        "b",
        "v",
        "g",
        "d",
        "e",
        "e",
        "j",
        "z",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "r",
        "s",
        "t",
        "u",
        "f",
        "h",
        "ts",
        "ch",
        "sh",
        "sch",
        "",
        "y",
        "",
        "e",
        "yu",
        "ya",
        "je",
        "i",
        "ji",
        "g",
    )
    TRANS = {}
    new_name = ""
    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c.lower())] = t.lower()
        TRANS[ord(c.upper())] = t.upper()
    for i in name[: name.rfind(".")]:
        if ord(i) in TRANS.keys():
            new_i = i.translate(TRANS)
        elif i.isdigit() or i.isalpha():
            new_i = i
        else:
            new_i = "_"
        new_name = new_name + new_i
    new_name = new_name + name[name.rfind(".") :]
    return new_name


def normalize(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a",
        "b",
        "v",
        "g",
        "d",
        "e",
        "e",
        "j",
        "z",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "r",
        "s",
        "t",
        "u",
        "f",
        "h",
        "ts",
        "ch",
        "sh",
        "sch",
        "",
        "y",
        "",
        "e",
        "yu",
        "ya",
        "je",
        "i",
        "ji",
        "g",
    )
    TRANS = {}
    new_name = ""
    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c.lower())] = t.lower()
        TRANS[ord(c.upper())] = t.upper()
    for i in name[: name.rfind(".")]:
        if ord(i) in TRANS.keys():
            new_i = i.translate(TRANS)
        elif i.isdigit() or i.isalpha():
            new_i = i
        else:
            new_i = "_"
        new_name = new_name + new_i
    new_name = new_name + name[name.rfind(".") :]
    return new_name


def normalize_all_files_and_folders_in_archieve(rootdir):
    for it in os.scandir(rootdir):
        if it.is_file():
            os.rename(it, os.path.join(rootdir, normalize(it.name)))
        elif it.is_dir():
            normalize_all_files_and_folders_in_archieve(it)
            os.rename(it, os.path.join(rootdir, normalize(os.path.basename(it))))


def move_and_normalize_and_unarchieve_files_into_correct_folders(
    rootdir, dict_extentions, lst_all_files, dict_fact_files
):
    for file in lst_all_files:
        is_moved = False
        for key, value in dict_extentions.items():
            if (
                file.name[(file.name).rfind(".") + 1 :].upper() in value
                and key != "archives"
            ):
                shutil.move(file, os.path.join(rootdir, key, normalize(file.name)))
                is_moved = True
                dict_fact_files[key].append(normalize(file.name))
            elif (
                file.name[(file.name).rfind(".") + 1 :].upper() in value
                and key == "archives"
            ):
                shutil.unpack_archive(
                    file,
                    os.path.join(
                        rootdir, key, normalize(file.name[: (file.name).rfind(".")])
                    ),
                )
                is_moved = True
                dict_fact_files[key].append(normalize(file.name))
        if is_moved == False:
            shutil.move(
                file, os.path.join(rootdir, "uknown_extension", normalize(file.name))
            )
            dict_fact_files["uknown_extension"].append(normalize(file.name))


def remove_all_unnecessary_folders(rootdir, dict_extentions):
    count_remove_all_unnecessary_folders = 0
    for it in os.scandir(rootdir):
        if (
            it.is_dir()
            and it.name not in dict_extentions.keys()
            and it.name != "uknown_extension"
        ):
            count_remove_all_unnecessary_folders += 1
            print('count_remove_all_unnecessary_folders')
            shutil.rmtree(it, ignore_errors=True)




def print_out_in_console(dict_fact_files, dict_known_unknown_extentions):
    for key, value in dict_fact_files.items():
        print( f"назва папки '{key}': {', '.join(value)}")
        if key == "uknown_extension":
            dict_known_unknown_extentions["unknown extensions"].update(
                i[(i).rfind(".") :].lower() for i in value
            )
        else:
            dict_known_unknown_extentions["known extensions"].update(
                i[(i).rfind(".") :].lower() for i in value

            )
    for key, value in dict_known_unknown_extentions.items():
        print(f"{key}: {', '.join(value)}")


def validate_correct_path():
    rootdir = None
    while True:
        rootdir = input(
            ">   Введіть шлях до каталогу, який потрібно відсортувати:"  
            
        ).strip()
        if not os.path.exists(rootdir) and rootdir.lower() != "exit":
            print(
                Fore.RED
                # + Back.RED
                + f"    Шлях не існує. Вкажіть шлях та каталог!"
            )
                       
            print(Fore.WHITE +  "Якщо ви хочете вийти - введіть 'exit")
        else:
            break
    return rootdir


def main():
    dict_extentions = {
        "archives": ["ZIP", "GZ", "TAR", 'RAR', '7Z', 'TGZ', 'ISO', 'JAR', 'BZ2'],
        "video": ["AVI", "MP4", "MOV", "MKV", 'FLV', 'MPEG', '3GP', 'WEBM', 'VOB', 'DIVX'],
        "audio": ["MP3", "OGG", "WAV", "AMR"],
        "documents": ["DOC", "DOCX", "TXT", "PDF", "XLSX", "XLS", "PPTX","DOT","CAD", "DWG", "ODG", "ODT"],
        "images": ["JPEG", "PNG", "JPG", "SVG"]
    }

    dict_fact_files = {
        "archives": [],
        "video": [],
        "audio": [],
        "documents": [],
        "images": [],
        "uknown_extension": [],
    }
    

    dict_known_unknown_extentions = {
        "known extensions": set(),
        "unknown extensions": set(),
    }

    while True:
        rootdir = validate_correct_path()
        if rootdir.lower() == "exit":
            print(Fore.BLUE +   "Вихід з сортувальника")
            print (Fore.YELLOW +   "Слава Україні!")
            break
        lst_all_files = []
        lst_all_files = list_all_files_in_rootdir(rootdir, lst_all_files)
        create_new_folders_in_rootdir(rootdir, dict_extentions)
        move_and_normalize_and_unarchieve_files_into_correct_folders(
            rootdir, dict_extentions, lst_all_files, dict_fact_files
        )
        normalize_all_files_and_folders_in_archieve(os.path.join(rootdir, "archives"))
        remove_all_unnecessary_folders(rootdir, dict_extentions)
        print_out_in_console(dict_fact_files, dict_known_unknown_extentions)


if __name__ == "__main__":
    main()