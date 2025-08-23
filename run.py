import tkinter as tk
from tkinter import filedialog

from lib.vars import output_path, root_path, setMeta
from lib.chapters import parse_chapters
from lib.toc import create_table_of_content
from lib.manifest import create_manifest

import shutil
import os
from colorama import Fore


def select_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("ZIP files", "*.zip")]
    )

    if file_path:
        print(f"Seleccionado: {file_path}\n")
        if os.path.isdir(root_path):
            shutil.rmtree(root_path)
        shutil.unpack_archive(file_path, './', 'zip')
    else:
        print("No file selected.")
        q = input(Fore.YELLOW + "Usar el ultimo archivo cargado? (S/N)" + Fore.RESET)
        if q != 's' and q != 'S':
            input("Pulsa cualquier tecla para salir")
            exit()


if __name__ == "__main__":


    print(Fore.YELLOW + 'AGMIGRRA EL EPUBINADOOOOR' + Fore.RESET)


    select_file()

    setMeta()
    from lib.vars import book_name

    parse_chapters()
    create_table_of_content()
    create_manifest()
    book_name = book_name.upper()

    if os.path.isfile(f'{book_name}.epub'):
        os.remove(f'{book_name}.epub')
    shutil.make_archive(f'./{book_name}', 'zip', output_path)
    os.rename(f'./{book_name}.zip', f'{book_name}.epub')
    print('\n' + Fore.GREEN + 'Libro Guardado' + Fore.RESET)
    input()

