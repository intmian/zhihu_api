from typing import *
from requests import get, Response, HTTPError
from json import dumps, dump
from info import *
from spider import is_valid_res


def get_user_collection_list(user: str) -> List:
    """
返回单个用户的总收藏列表
    :param user: url_token
    :return: [[id,name]...]
    """
    url = "https://www.zhihu.com/api/v4/people/{}/collections?include=data%5B*%5D.updated_time%2Canswer_count%2Cfollower_count%2Ccreator%2Cdescription%2Cis_following%2Ccomment_count%2Ccreated_time&offset=0&limit=20"
    response = get(
        url.format(user), headers=header
    )
    is_valid_res(response)
    data = response.json()
    re = list()
    for d in data["data"]:
        re.append([d["id"], d["title"]])
    return re


def get_collection(c_list: int) -> List:
    """
返回某一个收藏列表里面所有的回答/文章id
    :param c_list:收藏列表—id
    :return: [[id,type:str]]
    """
    url = "https://www.zhihu.com/api/v4/collections/{}/items?offset=".format(c_list)
    offset = 0
    re = []
    while True:
        response = get(
            url + str(offset) + "&limit=20", headers=header
        )
        data = response.json()
        if len(data["data"]) == 0:
            return re
        else:
            for d in data["data"]:
                re.append([d["content"]["id"], d["content"]["type"]])
        offset += 20


def get_user_collection(user_token: str) -> List:
    """
返回某人所有公开收藏，以以下格式
[
    {
        "name" : "xxx"
        "list" : [[id,type],......]
    }
]
    :param user_token: 此人url中的id
    """
    re = []
    lists = get_user_collection_list(user_token)
    for l in lists:
        re.append({"name": l[1], "list": get_collection(l[0])})
    return re


def dump_collection(user_token: str):
    """
将某人的收藏dump进文件中
以以下格式
[
    {
        "name" : "xxx"
        "list" : [[id,type],......]
    }
]
    :param user_token: 用户token
    """
    with open(user_token + '.json', 'w', encoding='utf-8') as f:
        # ensure ascii避免出现乱码
        dump(get_user_collection(user_token), f, ensure_ascii=False)


# test
if __name__ == '__main__':
    # t = get_hot_json(True)
    # print(t)
    dump_collection("")
