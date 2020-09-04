# 用于抓取和生成站点与设备文本
import requests
import json


def get_site_names():
    # 相关token参数
    token_url = 'https://account.flexem.com/core/connect/token'
    site_url = 'http://fbox360.com/api/client/box/grouped'
    api_url = 'http://fbcs101.fbox360.com/api/'
    post_data = {'username': 'ynzmhj', 'password': 'zmhj123456', 'client_id': 'kmbq',
                 'client_secret': 'a89f97dc2ed2457aa0c6e58eb40142b2',
                 'scope': 'openid offline_access fbox email profile',
                 'grant_type': 'password'}
    # 取token信息
    token_request = requests.post(token_url, data=post_data)
    token_result = json.loads(token_request.content)
    print(token_result)
    authorization = token_result['token_type'] + ' ' + token_result['access_token']
    # 取站点信息
    group_request = requests.get(site_url, headers={'Authorization': authorization, 'X-FBox-ClientId': 'test123456'})
    group_result = json.loads(group_request.content)
    print(group_result)
    site_list = []
    for group in group_result:
        box = group['boxRegs']
        for item in box:
            site = {'name': item['alias'], 'boxNo': item['box']['boxNo']}
            site_list.append(site)
    print('==============site list==================')
    print(site_list)
    # 取各个站点的设备信息
    equip_set = set()
    for site in site_list:
        boxNo = site['boxNo']
        url = api_url + 'v2/box/dmon/grouped?boxNo=' + boxNo
        equip_request = requests.get(url, headers={'Authorization': authorization})
        equip_json_list = json.loads(equip_request.content)
        for equips in equip_json_list:
            if equips['name'] != '传感':
                items = equips['items']
                for item in items:
                    equip_set.add(item['name'])
    equip_name_list = list(equip_set)
    # 设备名存在不规则数据 需要删掉
    equip_name_list = [i for i in equip_name_list if '_' in i]
    equip_name_list, equip_prop_list = equip_name_filter(equip_name_list)
    print('===================equip name list======================')
    print(equip_name_list)
    print('===================equip prop list======================')
    print(equip_prop_list)
    # # 目前我们取到了站点列表[{name: a, id: b}|...]以及设备命名列表[equip_name|...]
    # # 写到文件里
    # site_file = 'equip_data/origin_data.txt'
    # with open(site_file, 'w', encoding='utf-8') as file_obj:
    #     for site in site_list:
    #         file_obj.write(site['name'] + '\n')
    #     file_obj.write('|||\n')
    #     for equip_name in equip_name_list:
    #         file_obj.write(equip_name + '\n')
    #     file_obj.write('|||\n')
    #     for equip_prop in equip_prop_list:
    #         file_obj.write(equip_prop + '\n')
    return site_list, equip_name_list, equip_prop_list


def equip_name_filter(equip_name_list):
    equip_result = set()
    property_result = set()
    for name in equip_name_list:
        names = name.split('_')
        # 分割index 0:类型 1:名称 2:属性
        equip_result.add(names[1])
        property_result.add(names[2])
    equip_list = list(equip_result)
    property_list = list(property_result)
    return equip_list, property_list


def is_chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def add_equip_name_tag(word):
    equip_tag_dic = {'start': 'B-EQUIP', 'mid': 'I-EQUIP', 'end': 'E-EQUIP'}
    result = ''
    i = 0
    word_len = len(word)
    for _ in word:
        if i == 0:
            result += equip_tag_dic['start'] + ' '
        elif i == word_len - 1:
            result += equip_tag_dic['end']
        else:
            result += equip_tag_dic['mid'] + ' '
        i += 1
    return result


# 暂时用不到属性
def add_prop_tag(word):
    property_tag_dic = {'start': 'B-PROP', 'mid': 'I-PROP', 'end': 'E-PROP'}
    result = ''
    i = 0
    word_len = len(word)
    for _ in word:
        if i == 0:
            result += property_tag_dic['start'] + ' '
        elif i == word_len - 1:
            result += property_tag_dic['end']
        else:
            result += property_tag_dic['mid'] + ' '
        i += 1
    return result


def add_type_tag(word):
    type_dic = {'启动': 'B-TAG E-TAG ', '停止': 'B-TAG E-TAG ', '添加': 'B-TAG E-TAG ', '删除': 'B-TAG E-TAG '}
    return type_dic[word]


def add_space_c(word):
    i = 0
    ans = ''
    for c in word:
        if i == len(word) - 1:
            ans += c
        else:
            ans += c + ' '
        i += 1
    return ans


def generate_train_sentence_list(equip_name_list, equip_prop_list, type_list):
    """
    生成中文训练文本
    :param equip_name_list: 设备名称列表
    :param equip_prop_list: 设备属性列表
    :param type_list: 预设动作列表
    :return train_sentence_list: 生成的中文训练集
    """
    # 加两个停词吧
    pre_word = [{'name': '', 'code': ''}, {'name': '帮我', 'code': 'O O '}, {'name': '我想', 'code': 'O O '}]
    ans_list = []
    for equip_name in equip_name_list:
        for pre in pre_word:
            for item in type_list:
                train_word = pre['name'] + item + equip_name
                train_word = add_space_c(train_word)
                test_word = pre['code'] + add_type_tag(item) + add_equip_name_tag(equip_name)
                temp = train_word + '|||' + test_word
                ans_list.append(temp)
    return ans_list


if __name__ == '__main__':
    # 通过网络请求抽取到站点和设备名称 以及设备属性名
    site_list, equip_name_list, equip_prop_list = get_site_names()
    # 根据设备名与设备属性名以及预设动作生成自然语言文本
    type_list = ['启动', '停止', '添加', '删除']  # 预设动作
    train_sentence_list = generate_train_sentence_list(equip_name_list, equip_prop_list, type_list)
    # 将生成的预训练数据写入文本
    site_file = 'equip_data/train_data.txt'
    with open(site_file, 'w', encoding='utf-8') as file_obj:
        for train_sentence in train_sentence_list:
            file_obj.write(train_sentence + '\n')
