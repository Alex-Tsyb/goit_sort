import os
import sys
import shutil
import re


def sort_files_recursive(folder_path):
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

        for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
            TRANS[ord(c)] = l
            TRANS[ord(c.upper())] = l.upper()

        # Розділення імені та розширення файлу
        filename, file_extension = os.path.splitext(name)

        # Транслітерація кириличних символів
        translated_name = filename.translate(TRANS)

        # Заміна всіх символів, крім літер латинського алфавіту та цифр, на символ '_'
        normalized_name = re.sub(r"[^a-zA-Z0-9]", "_", translated_name)

        # Збереження розширення файлу
        normalized_name += file_extension

        return normalized_name

    def extract_archive(archive_path, destination_folder):
        # Визначення розширення архіву
        _, archive_extension = os.path.splitext(archive_path)
        archive_extension = archive_extension[1:].upper()

        # Розпакування архіву
        shutil.unpack_archive(archive_path, destination_folder)

    try:
        # Перевірка, чи існує вказана папка
        if not os.path.exists(folder_path):
            print(f"Папка '{folder_path}' не існує.")
            return

        # Перелік груп розширень
        file_groups = {
            "images": ["JPEG", "PNG", "JPG", "SVG"],
            "video": ["AVI", "MP4", "MOV", "MKV"],
            "documents": ["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"],
            "audio": ["MP3", "OGG", "WAV", "AMR"],
            "archives": ["ZIP", "GZ", "TAR"],
        }

        # Переміщення файлів в відповідні групи
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                filepath = os.path.join(root, filename)

                # Ігноруємо папки
                if os.path.isdir(filepath):
                    continue

                # Отримання розширення файлу
                _, file_extension = os.path.splitext(filename)
                file_extension = file_extension[1:].upper()

                # Визначення групи для даного розширення
                file_group = "unknown"
                for group, extensions in file_groups.items():
                    if file_extension in extensions:
                        file_group = group
                        break

                # Створення папки для даної групи, якщо її ще не існує
                destination_folder = os.path.join(folder_path, file_group)
                os.makedirs(destination_folder, exist_ok=True)

                # Формування нового імені файлу
                normalized_name = normalize(filename)
                new_filepath = os.path.join(destination_folder, normalized_name)

                # Переміщення та перейменування файлу
                shutil.move(filepath, new_filepath)

        # Видалення порожніх папок
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for directory in dirs:
                folder_path_to_check = os.path.join(root, directory)
                if not os.listdir(folder_path_to_check):
                    os.rmdir(folder_path_to_check)

        # Обробка архівів
        archives_folder = os.path.join(folder_path, "archives")
        os.makedirs(archives_folder, exist_ok=True)

        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                filepath = os.path.join(root, filename)

                # Ігноруємо папки та архіви
                if os.path.isdir(filepath) or os.path.splitext(filename)[1].upper() in (
                    "ZIP",
                    "GZ",
                    "TAR",
                ):
                    continue

                # Отримання розширення файлу
                _, file_extension = os.path.splitext(filename)
                file_extension = file_extension[1:].upper()

                # Перевірка, чи файл є архівом
                if file_extension in ("ZIP", "GZ", "TAR"):
                    archive_name = os.path.splitext(filename)[0]
                    archive_folder = os.path.join(archives_folder, archive_name)

                    # Створення папки для архіву
                    os.makedirs(archive_folder, exist_ok=True)

                    # Розпакування архіву
                    extract_archive(filepath, archive_folder)

        print(
            "Сортування, видалення порожніх папок, перейменування файлів та обробка архівів завершено."
        )
    except Exception as e:
        print(f"Виникла помилка: {e}")


if __name__ == "__main__":
    # Перевірка, чи передано аргумент при запуску
    if len(sys.argv) != 2:
        print("Потрібно вказати шлях до папки для сортування.")
    else:
        folder_path = sys.argv[1]
        sort_files_recursive(folder_path)
