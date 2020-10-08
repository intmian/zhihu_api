# -*- coding: UTF-8 -*-
"""
AUTHOR:   方家彦
DATE:     2020/10/8
DESCRIBE: 一些配置
"""
# 请求头
# 知乎默认的encode是gzip，为了避免麻烦应指定utf-8
header = {"authority": "www.zhihu.com",
          "method": "GET",
          "path": "/api/v4/answers/1065342258/voters?include=data%5B%2A%5D",
          "scheme": "https",
          "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
          "accept-encoding": "utf-8",
          "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
          "cache-control": "max-age=0",
          "sec-fetch-mode": "navigate",
          "sec-fetch-site": "none",
          "sec-fetch-user": "?1",
          "upgrade-insecure-requests": ":",
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
          }