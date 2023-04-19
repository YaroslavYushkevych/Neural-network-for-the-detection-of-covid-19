import os
import re

#os.chdir(r"E:\Neuro\archive\chest_xray\test\PNEUMONIA")

def get_file_names(folder_path) -> list:
    file_paths = [f.path for f in os.scandir(folder_path) if not f.is_dir()]
    file_names = [f.split('\\')[-1] for f in file_paths]

    return file_names

list_file_names = get_file_names(r"E:\Neuro\archive\chest_xray\val\PNEUMONIA_copy")
print(list_file_names)
print(len(list_file_names))

for i in range(0, len(list_file_names)):
    if "bacteria" in list_file_names[i]:
        os.rename(fr"E:\Neuro\archive\chest_xray\val\PNEUMONIA_copy\{list_file_names[i]}",
                  fr'E:\Neuro\archive\chest_xray_2\val\BACTERIAL\{list_file_names[i]}')
        print(f"goood{i}: {list_file_names[i]}")
    elif "virus" in list_file_names[i]:
        os.rename(fr"E:\Neuro\archive\chest_xray\val\PNEUMONIA_copy\{list_file_names[i]}",
                  fr'E:\Neuro\archive\chest_xray_2\val\VIRAL\{list_file_names[i]}')
        print(f"goood{i}: {list_file_names[i]}")