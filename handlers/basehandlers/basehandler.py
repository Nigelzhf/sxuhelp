import tornado.web
from backend.mysql_model.user import User
from utils import logger
from utils.util import set_api_header,json_result, RequestArgumentError, get_cleaned_query_data
import json
import config

class BaseRequestHandler(tornado.web.RequestHandler):
    '''
    重写了异常处理
    '''
    def write_error(self, status_code, **kwargs):
        #if 'exc_info' in kwargs:
        #    # 参数缺失异常
        #    if isinstance(kwargs['exc_info'][1],RequestArgumentError):
        #        self.write(json_result(kwargs['exc_info'][1].code,kwargs['exc_info'][1].msg))
        #        return

        self.redirect("/static/500.html")
        if status_code==400:
            self.redirect("/static/404.html")
            return

        if not config.DEBUG:
            self.redirect("/static/500.html")

    def prepare(self):
        pass
        #if 'openid' not in self.request.query_arguments.keys():
        #    self.render('error.html', error="请从微信端登陆")

    def get_current_user(self):
        openid = get_cleaned_query_data(self, ['openid'], blank = True)['openid']
        if openid:
            user = User.get_by_openid(openid)
        else:
            user = None
        return user

#class BaseStaticFileHandler(tornado.web.StaticFileHandler, BaseRequestHandler):
class BaseStaticFileHandler(tornado.web.StaticFileHandler):
    pass

class ErrorHandler(BaseRequestHandler):
    '''
    默认404处理
    '''
    def prepare(self):
        if 'X-Real-IP' in self.request.headers:
            ip=self.request.headers['X-Real-IP']
        else:
            ip=self.request.remote_ip
        logger.error(self.request.uri+"---"+ip)
        self.set_status(404)
        self.finish()
    def write_error(self):
        pass
