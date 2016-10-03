
import hashlib
from handlers.weixin.utils import msg_type
from config import TOKEN,domain
from handlers.basehandlers.basehandler import BaseRequestHandler

class WeixinHandler(BaseRequestHandler):
    def get(self):
        print('验证Access_Token')
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        print(signature + timestamp + nonce + echostr)
        token = TOKEN
        tmpList = [token, timestamp, nonce]
        tmpList.sort()
        tmpstr = "%s%s%s" % tuple(tmpList)
        tmpstr = tmpstr.encode()
        tmpstr = hashlib.sha1(tmpstr).hexdigest()
        if tmpstr == signature:
            self.write(echostr)
        else:
            self.write('Sorry')

    def post(self):
        rt_msg=msg_type(self.request.body)
        self.write(rt_msg.replace('re_domain',domain))
