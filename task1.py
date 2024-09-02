import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor


def process_file(src_path, dest_dir):
    ext = os.path.splitext(src_path)[1][1:].lower()

    if not ext:
        return

    ext_dir = os.path.join(dest_dir, ext)
    os.makedirs(ext_dir, exist_ok=True)

    dest_path = os.path.join(ext_dir, os.path.basename(src_path))
    shutil.copy2(src_path, dest_path)
    print(f"Копіювання файлу {src_path} -> {dest_path}")


def process_directory(src_dir, dest_dir):
    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(src_dir):
            for file_name in files:
                src_path = os.path.join(root, file_name)
                executor.submit(process_file, src_path, dest_dir)

            for dir_name in dirs:
                sub_dir = os.path.join(root, dir_name)
                executor.submit(process_directory, sub_dir, dest_dir)


def main():

    if len(sys.argv) < 2:
        print("Використання: python script.py <source_dir> [destination_dir]")
        sys.exit(1)

    src_dir = sys.argv[1]
    dest_dir = sys.argv[2] if len(sys.argv) > 2 else 'dist'

    os.makedirs(dest_dir, exist_ok=True)

    process_directory(src_dir, dest_dir)
    print("Готово!")


if __name__ == "__main__":
    main()
