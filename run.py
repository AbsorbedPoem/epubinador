import tkinter as tk
from tkinter import filedialog
# from lib import vars, chapters, toc, manifest

from lib.vars import output_path, root_path
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
        print(f"Seleccionado: {file_path}")
        if os.path.isdir(root_path):
            shutil.rmtree(root_path)
        shutil.unpack_archive(file_path, './', 'zip')
    else:
        print("No file selected.")

if __name__ == "__main__":

    print(Fore.YELLOW + 'AGMIGRRA EL EPUBINADOOOOR' + Fore.RESET)

    select_file()

    parse_chapters()
    create_table_of_content()
    create_manifest()

    if os.path.isfile('Soul Noise.epub.epub'):
        os.remove('Soul Noise.epub.epub')
    shutil.make_archive('./Soul Noise', 'zip', output_path)
    os.rename('./Soul Noise.zip', 'Soul Noise.epub')
    print('\n' + Fore.GREEN + 'Libro Guardado' + Fore.RESET)
    input()

