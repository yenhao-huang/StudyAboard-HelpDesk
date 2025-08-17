import os

def list_all_files(dir_path):
    all_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files
