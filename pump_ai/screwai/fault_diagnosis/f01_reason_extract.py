#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 21:24
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: f01_reason_extract.py
# 专业函数
import pandas as pd

from screwai.core.base import *


def fault_map_func(x, fault_dict):
    # 从故障原因中提取，哪些故障，返回故障类型列表
    # 可能有缺失值
    if type(x) != str:
        return []

    _fault_type_list = []
    for word in list(fault_dict):
        if word in x:
            _fault_type_list.append(fault_dict[word])

    #     if len(_fault_type_list) == 0:
    #         return None
    #     elif len(_fault_type_list) == 1:
    #         return _fault_type_list[0]

    return _fault_type_list


def find_fault_id(x, focus_id, mode='common'):
    # 从故障id列表中，判断是否存在指定类型，可选：
    # common: 包含该故障
    # only: 有且只对应该故障
    # first: 多故障，以第一个故障为判断依据

    assert mode in ['only', 'common', 'first'], '未知模式，请选择:only, common, first 模式'
    # mode: 'only', 'common'

    if len(x) == 0:
        return False

    elif mode == 'common':
        res = focus_id in x

    elif mode == 'only':
        res = [focus_id] == x

    elif mode == 'first':
        try:
            res = focus_id == x[0]
        except Exception as e:
            print(x)
            raise e

    else:
        return False

    return res


class FindReason(object):
    """故障原因检索"""

    def __init__(self, data_path):
        """
        data_path: str, 故障映射表路径
        """
        super(FindReason, self).__init__()

        # 故障特征词原因，pd.DataFrame
        fault_mapping_df = yaml_read(data_path, encoding='utf-8')
        self.fault_mapping_df = pd.DataFrame(fault_mapping_df).T

    def get_fault_mapping_df(self):
        # 获取 故障特征词原因
        return self.fault_mapping_df

    def bag_of_words_in_language(self, fault_focus_language):
        """
        返回指定语言
        fault_focus_language: str, 故障特征词语言 in ['CN', 'RU', 'EN']
        """
        assert fault_focus_language in ['CN', 'RU', 'EN'], '选择的语言只能为CN,RU,EN其中一种'

        bag_of_words = []
        for i in self.fault_mapping_df[fault_focus_language]:
            bag_of_words += i

        # 列表去重，保持原始顺序
        bag_of_words = list(dict.fromkeys(bag_of_words))

        return bag_of_words

    def find_reason(self, fault_focus_reason, fault_focus_language):
        """
        fault_focus_reason: str, 故障特征词原因
        fault_focus_language: str, 故障特征词语言 in ['CN', 'RU', 'EN']
        """

        assert fault_focus_language in ['CN', 'RU', 'EN'], '选择的语言只能为CN,RU,EN其中一种'

        # 某个特征词可能出现在多个故障类型中
        fault_reason_focus_idx_list = []
        for idx in range(len(self.fault_mapping_df)):
            if fault_focus_reason in self.fault_mapping_df.loc[idx, fault_focus_language]:
                fault_reason_focus_idx_list.append(idx)

        return fault_reason_focus_idx_list

