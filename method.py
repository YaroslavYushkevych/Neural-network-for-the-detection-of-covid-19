import os
import shutil

def photo_path_add():
    path = r"E:\Neuro\archive\Eval"
    name_file = os.listdir(path)
    #print(name_file[0])
    for i in range(0, 25):
        shutil.copyfile(rf"E:\Neuro\archive\Eval\{name_file[0]}", rf"E:\Neuro\archive\Predict\Test\photo_{i}.jpeg")
    #os.remove(rf"E:\Neuro\archive\Eval\{name_file[0]}")


def clear_dir():
    path = r"E:\Neuro\archive\Predict\Test"
    for file_name in os.listdir(path):
        #print(file_name)
        file = path + r"\\" + file_name
        if os.path.isfile(file):
            #print('Deleting file:', file)
            os.remove(file)

def clear_eval():
    path = rf"E:\Neuro\archive\Eval"
    name_file = os.listdir(path)
    os.remove(rf"E:\Neuro\archive\Eval\{name_file[0]}")

def create_dir():
    directory = "Test"
    parent_dir = r"E:\Neuro\archive\Predict"
    path_pre = os.path.join(parent_dir, directory)
    os.mkdir(path_pre)
    print("Directory '% s' created" % directory)