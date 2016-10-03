# coding: utf-8
import requests

data = {
    '__VIEWSTATE': 'dDwyMTIyOTQxMzM0Ozs+AI2AQlMGeOYvPjA1fJfST57PPCk=',
    'pcInfo': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0Intel Mac OS X 10.115.0 (Macintosh) SN:NULL',
    'txt_asmcdefsddsd': '201502401037',

    # 密码密文
    'dsdsdsdsdxcxdfgfg': '58FF9D86289172C240A7143CF0A2D2',

    # 验证码
    'fgfggfdgtyuuyyuuckjg': '3A6147FB984F339FD0726319DA0808',
    'Sel_Type': 'STU',
    'typeName': '学生'
}

proxy = {
    'http': 'http://127.0.0.1:8080'
}

headers = {
    'Host': 'bkjw.sxu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Referer': 'http://bkjw.sxu.edu.cn/_data/login.aspx',
    'Cookie': 'ASP.NET_SessionId=5nloy4rryrm3je45ebaqyy45; amlbcookie=02; iPlanetDirectoryPro=AQIC5wM2LY4SfcyLZEfNliCNZptM4WjZMDMr6feDuZ%2BpYgk%3D%40AAJTSQACMDI%3D%23'
}

resp = requests.post('http://bkjw.sxu.edu.cn/_data/login.aspx', data = data, headers = headers,proxies = proxy)
import pdb;pdb.set_trace()

print(resp.text)
