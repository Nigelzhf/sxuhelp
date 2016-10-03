# coding:utf-8
import tornado.web
from backend.mysql_model.user import User
from handlers.basehandlers.basehandler import BaseRequestHandler
from utils.util import json_result, bind_required
from utils.util import get_cleaned_post_data,RequestArgumentError

import requests
import re
import base64

class KingoCaptcha(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self.set_header("Content-type",  "image/jpg")
        response = requests.get('http://bkjw.sxu.edu.cn/_data/login.aspx',
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                                )
        viewstate = self.find_viewstate(response.text)
        self.set_cookie('ViewState', viewstate)
        # ASPsessionid是唯一凭证
        ASPsessionid = response.cookies.get('ASP.NET_SessionId')
        response = requests.get("http://bkjw.sxu.edu.cn/sys/ValidateCode.aspx",
                                    cookies = {'ASP.NET_SessionId': ASPsessionid},
                                    headers = {'Referer': 'http://bkjw.sxu.edu.cn/_data/login.aspx', 'Host': 'bkjw.sxu.edu.cn'},
                                    #proxies = {'http': 'http://127.0.0.1:8080'}
                                )
        self.set_cookie('ASP.NET_SessionId', ASPsessionid)
        self.write(response.content)

    def find_viewstate(self,content):
        pattern = re.compile(r'name="__VIEWSTATE" value="(.*?)"')
        v = pattern.search(content)
        return v.group(1)
