"""
1. Скрипт приймає один аргумент при запуску це шлях до папки для сортування.
2. Також за бажанням можна прописати другим аргументом "backup", що вкаже скрипту
перед сортування заархівувати папку яку буде сортовано та помістити його до цієї папки.
3. Результати роботи скрипту виводяться до терміналу, а також створююється два текстові файли 
один з яким містить таку ж інформацію що виведено до терміналу, а також лог* сортування.
Другий містить в собі лог* нормалізації та кількість нормалізованих файлів.
* Мається на увазі список шляхів до сортування/нормалізації та після.
"""

import sys
from updated_sorter.tools import *
from pathlib import Path
from utilities import kb_interrupt_error

def clean_folder(path, backup=False):
    path = Path(path)
    if backup == True: 
        create_backup_copy(path)

    # Main logic. Results of the functions assign to variables for future reporting
    
    files_amount_init = files_amount(path)
    normalized_log, normalized_files = normalize(path)
    sort_log, unpacked_archs_count = sort_dir(path)
    removed_dirs = remove_empty_dirs(path)
    
    # Shows results of the script in terminal

    dirs_info(path)
    print(
f'''
{'Amount of sorted files:':<30} {files_amount_init}
{'Normalized files:':<30} {normalized_files}
{'Unpacked archives:':<30} {unpacked_archs_count}
{'Removed empty directories:':<30} {removed_dirs}
''')

    # Creates two file. First contains results of the script and sorting log. 
    # Second contains log of normalized files.

    make_report(path, backup)
    with open(path / 'report.txt', 'a', encoding="utf-8") as rep:
        rep.write(
f'''
{'Amount of sorted files:':<30} {files_amount_init}
{'Normalized files:':<30} {normalized_files}
{'Unpacked archives:':<30} {unpacked_archs_count}
{'Removed empty directories:':<30} {removed_dirs}
'''
        )
        rep.write("\nSort log:\n")
        for pair in sort_log:
            rep.write(f"{pair[0]} --> {pair[1]}\n")
        
    with open(path / 'normalized_log.txt', 'w', encoding="utf-8") as rep:
        rep.write(f"\nScript normalized {normalized_files} files.\n\n")
        rep.write("Normalize log:\n\n")
        for pair in normalized_log:
            rep.write(f"{pair[0]} --> {pair[1]}\n")

first_lauch = True

@kb_interrupt_error
def main():

    global first_lauch
    if first_lauch:
        greet()
        first_lauch = False
    
    path = validate_correct_path()

    # if len(sys.argv) == 3 and sys.argv[2] == 'backup':
    #     backup_archive = True
    # else:
    #     backup_archive = False
    clean_folder(path)
    # try:
    #     path = rf"{sys.argv[1]}"
    #     try:
    #         # clean_folder(path, backup_archive)
    #         clean_folder(path)
    #     except FileNotFoundError as e:
    #         print(f"Invalid path argument: {e}. Path may contain whitespaces.")
    # except IndexError as err:
    #     print(f"At least 1 argument should be passed: {err}")


if __name__ == '__main__':
   main()