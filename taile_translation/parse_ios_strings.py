import os

import chardet

from ios_string import IOS_String

"""
只获取该项目的英文翻译的字段和中文翻译的字段, 然后基于英文和中文去对比和比较
"""
ios_app_project_path = "D:\\github\\firefox-ios"


def get_all_strings_xml_file(module_name, module_string_path):
    """

    根据模块名和项目路径, 获得该模块的 Localizable.strings 文件
    :param module_name:
    :param module_string_path:
    :return:
    """
    """
        过滤出所有的符合条件的 strings 文件
    :return:
    """
    app_file = os.walk(module_string_path + os.sep + module_name)
    string_file_listA = []
    for path, dir_list, file_list in app_file:
        for dir_name in dir_list:
            file_path = os.path.join(path, dir_name)
            for dir_path in os.listdir(file_path):
                file_full_path = os.path.join(file_path, dir_path)
                if file_full_path.endswith(".strings") and file_full_path.__contains__("zh-CN.lproj"):
                    string_file_listA.append(file_full_path)
    print("the strings file of the project, total " + str(string_file_listA.__len__()))
    return string_file_listA


def get_all_module_name():
    """
    根据目录获取该项目的所有的项目
    :return:
    """
    string_dir = os.listdir(ios_app_project_path)
    list_a = []
    for dir1 in string_dir:
        isDir = os.path.isdir(ios_app_project_path + os.sep + dir1)
        if isDir:
            list_a.append(dir1)
    return list_a


string_file_dict = {}


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']


def read_strings_from_file(module_name: str, file_path):
    ios_string_list = []
    encoding = get_encoding(file_path)
    # print("read_strings_from_file: encoding = " + encoding, " file_path " + file_path)
    """
    这些 Windows-1254 和 EUC-TW 编码统一归为 UTF-8 编码
    """
    if encoding == "Windows-1254" or encoding == "EUC-TW":
        encoding = "utf-8"
    project_file_path = file_path.split(ios_app_project_path)[1]
    with open(file=file_path, encoding=encoding) as f:
        file_string = f.readlines()

        for string in file_string:

            if string.strip().__eq__(""):
                continue
            if not string.startswith("\""):
                continue
            ios_string_id = string.split("\" ")[0].replace("\"", "")
            ios_string_value = string.split("\" ")[1].replace("= ", "").replace(";", "").replace("\"", "")
            ios_string = IOS_String(module_name, ios_string_id, ios_string_value, project_file_path)
            ios_string_list.append(ios_string)
    for ios_string in ios_string_list:
        pass
        # print("ios_string = " + str(ios_string))
    return ios_string_list


def get_ios_project_string_dict():
    module_list = get_all_module_name()
    ios_module_string_dict = {}
    for module in module_list:
        string_file_list = get_all_strings_xml_file(module, ios_app_project_path)
        # print("string_file_list = " + str(string_file_list.__len__()))
        module_string_list = []
        for file in string_file_list:
            list_c = read_strings_from_file(module, file)
            for c in list_c:
                module_string_list.append(c)
        ios_module_string_dict[module] = module_string_list
    return ios_module_string_dict


def strip_null_value_string_dict():
    ios_module_string = get_ios_project_string_dict()
    module_string = {}
    for (module_name, value) in ios_module_string.items():
        list_d = ios_module_string.get(module_name)
        if list_d.__len__() == 0:
            continue
        print("list_d = " + str(list_d.__len__()) + ", module_name = " + module_name)
        module_string[module_name] = list_d
        for d in list_d:
            print("ddddd = " + str(d))
    return module_string


string_dict = strip_null_value_string_dict()
for module_name in string_dict.keys():
    list_d = string_dict.get(module_name)
    for d in list_d:
        print("================= " + str(d))
