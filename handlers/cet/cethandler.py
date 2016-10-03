import sys,os
sys.path.append('/Users/jmpews/Desktop/project/sxuhelp/')
print(sys.path)
import config
from utils import logger
from utils.util import get_cleaned_post_data, get_cleaned_query_data, RequestArgumentError, set_api_header
from tornado.gen import coroutine
from handlers.cet.CetUtils import CetTicket
from handlers.basehandlers.basehandler import BaseRequestHandler
import json
import os

from tornado.web import asynchronous


f=open(os.getcwd()+'/handlers/cet/school.json','r')
schools=json.load(f)

ErrorResult={'error':True,'txt':'没有您的信息'}

#CET首页
class CetHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self.render('cet/cet.html')
#CET学校首页
class SchoolCetHandler(BaseRequestHandler):
    def get(self, province, school, *args, **kwargs):
        school_url="/api/cet_school_ticket/%s/%s/" % (province, school)
        school_info={'schoolname':school,'school_url':school_url}
        self.render('cet/school_cet.html',school_info=school_info)

class get_schools(BaseRequestHandler):
    '''
    返回province对应school的信息
    '''
    def get(self, *args, **kwargs):
        self.write(schools)

# 有准考证查询
class cet_yes_ticket(BaseRequestHandler):
    @asynchronous
    @coroutine
    def post(self, *args, **kwargs):
        post_data=get_cleaned_post_data(self,['username','ticket',])
        #在不破坏逻辑的状况下异步调用函数
        g=CetTicket.get_score(post_data['ticket'],post_data['username'])
        resp=yield next(g)
        try:
            result=g.send(resp)
        except StopIteration as e:
            result=e.value
            if result:
                r=result
        self.write(json.dumps(r))

#无准考证查询
class cet_no_ticket(BaseRequestHandler):
    @asynchronous
    @coroutine
    def post(self, *args, **kwargs):
        post_data=get_cleaned_post_data(self,['username','province','school','cet_type',])
        g=CetTicket.find_ticket_number(int(post_data['province']),post_data['school'],post_data['username'],cet_type=int(post_data['cet_type']))
        resp=yield next(g)
        try:
            g.send(resp)
        except Exception as e:
            ticket=e.value
        if ticket:
            g=CetTicket.get_score(ticket, post_data['username'])
            resp=yield next(g)
            try:
                result=g.send(resp)
            # 触发生成器StopIteration
            except StopIteration as e:
                result=e.value
                if result:
                    r=result
        self.write(json.dumps(r))

#按照学校查找_PRO版
class cet_school_ticket(BaseRequestHandler):
    @asynchronous
    @coroutine
    def post(self, province, school, *args, **kwargs):
        #判断学校是否在授权列表中
        if school not in config.school_pro:
            #self.write("School not in Pro")
            #return
            pass
        post_data=get_cleaned_post_data(self,['username','cet_type',])
        g=CetTicket.find_ticket_number(int(province),school,post_data['username'],cet_type=int(post_data['cet_type']))
        resp=yield next(g)
        try:
            g.send(resp)
        except Exception as e:
            ticket=e.value
        if ticket:
            g=CetTicket.get_score(ticket, post_data['username'])
            resp=yield next(g)
            try:
                g.send(resp)
            # 触发生成器StopIteration
            except StopIteration as e:
                result=e.value
                if result:
                    r = result
        self.write(json.dumps(r))
        return

if __name__=='__main__':
    print(ct.find_ticket_number(u'重庆', u'重庆邮电大学', u'曾盈', cet_type=CetTicket.CET4))

