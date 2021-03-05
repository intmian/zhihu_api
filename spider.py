# -*- coding: UTF-8 -*-
"""
AUTHOR:  mian
DATE:     2020/10/8
DESCRIBE: 知乎的一些信息获取
"""
from typing import *
from requests import get, Response, HTTPError
from json import dumps, dump
from info import *

'''
如何使用接口：
try:
    调用spider.py里面的接口
except requests.HTTPError:
    处理因为反爬虫或知乎于2020/10/8后更改了接口而引发的错误
except requests.RequestException:
    处理因为网络错误或别的什么奇怪的错误而引发的异常
'''


def get_hot_json(output: bool) -> str:
    """获得当前热榜所有热搜的前十条回答的前十条评论并进行json化
    :param output: 是否输出正在访问哪个问题以方便调试
    :return: 数据
    :exception: requests.HTTPError,requests.RequestException
    """
    return dumps(get_hot(output))


def get_hot(output: bool) -> List:
    """
    获得当前热榜所有热搜的前十条回答的前十条评论
    :param output: 是否输出正在访问哪个问题以方便调试
    :return: 数据
    :rtype: List[
        Dict["url_token":xxx,"content":xxx,"time":xxx]
        next Dict
        ...]
    :exception: requests.HTTPError,requests.RequestException
    """
    i = 0
    re = []
    questions = get_hot_code()
    for question in questions:
        answers = get_ans_code(question)
        for answer in answers:
            if output:
                i = i + 1
                print(i)
            re = re + get_com(answer)
    return re


def is_valid_res(res: Response):
    """
    若已触发知乎反爬虫、别的异常情况则丢出异常
    :param res: 待检查的
    :exception: requests.HTTPError,requests.RequestException
    """
    if res.status_code != 200:  # 除非没有网一般都是这个
        raise HTTPError


def get_hot_code() -> List:
    """返回热榜的问题
    :return: 热榜上前五十个问题的代码
    :exception: requests.HTTPError,requests.RequestException
    """
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
    res = get(url, headers=header)
    is_valid_res(res)
    data = res.json()
    re = list()
    for temp in data["data"]:
        re.append(temp["target"]["id"])
    return re


def get_ans_code(question: str) -> List:
    """返回ans所对应的问题的前十个回答
    :param question: 问题代码
    :return: 回答的代码，且放在list中
    :exception: requests.HTTPError,requests.RequestException
    """
    url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=%2&offset=0&limit=10&sort_by=default".format(
        question)  # default代表按照推荐度排序
    res = get(url, headers=header)
    is_valid_res(res)
    data = res.json()
    re = list()
    for ans in data["data"]:
        re.append(ans["id"])
    return re


def get_com(answer: str) -> List:
    """返回前十条评论
    :param answer: 回答代码
    :rtype: List[
        Dict["url_token":xxx,"content":xxx,"time":xxx]
        next Dict
        ...]
    :exception: requests.HTTPError,requests.RequestException
    """
    response = get(
        "https://www.zhihu.com/api/v4/answers/{}/root_comments?order=normal&limit=10&offset=0&status=open".format(
            answer), headers=header
    )
    is_valid_res(response)
    data = response.json()
    re = list()
    for com in data["data"]:
        re.append({"url_token": com["author"]["member"]["url_token"],
                   "content": com["content"],
                   "time": com["created_time"]})
    return re


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
