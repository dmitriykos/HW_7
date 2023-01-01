import json
import sys
import shutil
import os
from pathlib import Path

# створення цільових тек


def create_target_folders(path_folder: Path) -> dict:
    # створення категорій з файла catalog.json
    def create_categories(path_folder: str) -> dict:
        with open(path_folder) as f:
            result = json.load(f)
        return result
# створення тек з назвою ключа в категорії
    CATEGORIES = create_categories("catalog.json")
    for i in CATEGORIES:
        # якщо такої теки немає, то стоворюєио її
        if not path_folder.joinpath(i).exists():
            path_folder.joinpath(i).mkdir()

    return CATEGORIES       # повертає словник з категоріями та розширенням

# нормалізація ім'я


def normalize(name: str) -> str:
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    CYRILLIC = tuple(CYRILLIC_SYMBOLS)
    for c, t in zip(CYRILLIC, TRANSLATION):
        TRANS[ord(c)] = t
        TRANS[ord(c.upper())] = t.upper()
    normalize_name = name.translate(TRANS)
    return normalize_name


def delete_folders(path_folder: Path):    # видалимо порожні папки
    path_folder = Path(path_folder)
    for file in path_folder.glob("**/*"):
        if file.is_dir():
            if len(os.listdir(file)) == 0:
                os.rmdir(file)


count = 0


def sort_files(path_folder: Path) -> str:  # отримаємо список цільових елементів
    work_dir = Path(path_folder)
    # словник з папками та розширенням
    cat = create_target_folders(work_dir)
    # тестова тека

    global count
    for file in work_dir.glob("**/*"):

        normalize_name = normalize(file.name)
        count += 1

        # ітеруємо словник і переносимо файли в нові папки
        for new_folder, list_extension in cat.items():
            try:
                if str(file.suffix) in cat["archives"]:
                    shutil.unpack_archive(
                        file, work_dir / "archives" / file.stem)
                    file.replace(work_dir / "archives" / file.name)
                elif file.suffix in list_extension:
                    try:
                        shutil.move(file, work_dir /
                                    new_folder / normalize_name)
                    except FileExistsError:
                        new_name = f"_{count}.".join(
                            normalize_name.split("."))
                        shutil.move(file, work_dir / new_folder / new_name)
                elif file.suffix not in cat and file.is_file():
                    shutil.move(file, work_dir / "Others")
            except Exception as err:
                print(f"[ERROR]: {err}")
                continue


# головна функція
def sort() -> str:
    try:
        folder = sys.argv[1]
        sort_files(folder)
        delete_folders(folder)
        print(f"File in {folder} were sorted successfully!")
        print(f"All files: {count}")

    except IndexError:
        print("No parameter")


if __name__ == "__main__":
    sort()
