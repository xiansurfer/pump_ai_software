import os
import pickle

def makedirs(path):
    """
    保证path这个文件或文件夹路径存在，如果没有则创建该路径
    path 可以为文件或文件夹
    """
    # 通过是否有.xxx后缀判断是文件或文件夹
    # 如果是文件则去除文件名
    # 如果是文件夹则直接判断该文件夹是否存在并创建
    if os.path.splitext(path)[1] != '':
        # 这个是文件
        path = os.path.split(path)[0]

    if not os.path.isdir(path):
        os.makedirs(path)

def pickle_save(path, content):
    """
    保存py变量
    """
    # 如果不存在该路径，则创建文件夹
    makedirs(path)
    with open(path, 'transformer') as f:
        pickle.dump(content, f)


def pickle_load(path):
    """
    读取py变量
    """
    with open(path, 'rb') as f:
        content = pickle.load(f)
    return content
