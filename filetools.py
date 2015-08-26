__author__ = 'TheJoker'
import shutil
import sys
import os


# 获取脚本文件的当前路�?
def get_path():
    """get the scripts path"""
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def copy_file(source_file_path_name, target_file__path_name):
    """copy the source file to target file"""
    shutil.copy(source_file_path_name, target_file__path_name)


def file_exist(file_path_name):
    """judge the file exist, return true or false"""
    if os.path.exists(file_path_name):
        return True
    else:
        return False


if __name__ == '__main__':
    print(cal_field(5, 30))
