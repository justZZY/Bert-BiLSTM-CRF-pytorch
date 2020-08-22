# 用于抓取和生成站点与设备文本
import requests
import json


def getSiteNames():
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
    print(token_request)
    token_result = json.loads(token_request.content)
    print(token_result)
    authorization = token_result['token_type'] + ' ' + token_result['access_token']
    # 取站点信息
    group_request = requests.get(site_url, headers={'Authorization': authorization, 'X-FBox-ClientId': 'test123456'})
    print(group_request)
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
            items = equips['items']
            for item in items:
                equip_set.add(item['name'])
    equip_name_list = list(equip_set)
    print('===================equip name list======================')
    print(equip_name_list)
    # 目前我们取到了站点列表[{name: a, id: b}|...]以及设备命名列表[equip_name|...]
    # 写到文件里
    site_file = 'equip_data/origin_data.txt'
    with open(site_file, 'w', encoding='utf-8') as file_obj:
        for site in site_list:
            file_obj.write(site['name'] + '\n')
        for equip_name in equip_name_list:
            file_obj.write(equip_name + '\n')


if __name__ == '__main__':
    getSiteNames()
