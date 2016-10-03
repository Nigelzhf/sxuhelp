#!/usr/bin/env python
# coding:utf-8

import tornado.web
import tornado.ioloop
from os import path
from sys import argv

import config
from handlers.basehandlers.basehandler import ErrorHandler, BaseStaticFileHandler
from handlers.index import IndexHandler, BindHandler, MyScoreHandler_New, MyScoreHandler_Old, MySecondScoreHandler_Old
from handlers.weixin.weixin import WeixinHandler
from handlers.utils import KingoCaptcha



handlers = [
    (r'/', IndexHandler),
    (r'/bind', BindHandler),
    (r'/utils/kingocaptcha', KingoCaptcha),
    ('/myscore', MyScoreHandler_New),
    ('/myscore_old', MyScoreHandler_Old),
    ('/mysecondscore_old', MySecondScoreHandler_Old),
    (r'/weixin', WeixinHandler),

    #(r'/bind_new_weixin', BindNewWeixin),

    #('r/new_score', NewScore),

    #('r/old_second_score', OldSecondScore)
    #('r/new_second_score', NewSecondScore)
    (r'/assets/(.*)', BaseStaticFileHandler, {"path": "frontend"})
]

application = tornado.web.Application(
    handlers=handlers,
    default_handler_class=ErrorHandler,
    debug=config.DEBUG,
    static_path=path.join(path.dirname(path.abspath(__file__)), 'static'),
    template_path="templates",
    bind_url='/',
    cookie_secret=config.COOKIE_SECRET,
)

config.app = application

if __name__ == "__main__":
    if len(argv) > 1 and  argv[1][:6] == '-port=':
        config.PORT = int(argv[1][6:])

    application.listen(config.PORT)
    print('Server started at port %s' % config.PORT)
    tornado.ioloop.IOLoop.instance().start()
