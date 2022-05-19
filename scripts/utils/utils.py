import os


def get_files(target_dir, end_pattern):
    # input: root path of specific frameworks
    # output: list format: ["file_dir_1", "file_dir_2", ...]
    # function, go through all files in the framework and only find python files
    file_lists = []
    for root, subdirs, files in os.walk(target_dir):
        for file in files:
            if not file.endswith(end_pattern):
                continue
            file_lists.append(os.path.join(root, file))
    return file_lists

