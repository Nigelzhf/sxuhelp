import time
import xml.etree.ElementTree as ET
from utils import logger
from backend.mongo_db.comment import CommentDB
from backend.mysql_model.user import User
from handlers.weixin import weixin_return_template

# 对用户提交的信息(xml)进行拆分，并根据不同类型的消息选择不同方式的回复
def msg_type(request):
    xmlstr = ET.fromstring(request)
    toUserName = xmlstr.find('ToUserName').text
    fromUserName = xmlstr.find('FromUserName').text
    # 获取消息类型
    msgType = xmlstr.find('MsgType').text
    if msgType == 'text':
        return response_msg_text(request)
    elif msgType == 'event':
        eventType = xmlstr.find('Event').text
        logger.debug(eventType+" : "+fromUserName)
        if eventType == 'CLICK':
            return response_msg_click(request)
        # 关注事件
        elif eventType == 'subscribe':
            rt_content= '暂时不能绑定了.'
            return compound_msg_text(toUserName, fromUserName, rt_content)
        # 取消关注事件，清除绑定
        elif eventType == 'unsubscribe':
            return '取消关注'
    returncontent = '很抱歉-暂不支持您的查询'
    return compound_msg_text(toUserName, fromUserName, returncontent)

# 普通文本信息的合成
def compound_msg_text(toUserName, fromUserName, returncontent, msgType='text'):
    out = weixin_return_template.RT_txt % (fromUserName, toUserName, str(int(time.time())), msgType, returncontent)
    return out

# 根据用户提交的普通文本信息，进行判断回复
def response_msg_text(request):
    xmlstr = ET.fromstring(request)
    toUserName = xmlstr.find('ToUserName').text
    fromUserName = xmlstr.find('FromUserName').text
    content = xmlstr.find('Content').text
    inputParams = content.split(' ')
    lenParams = len(inputParams)
    CommentDB.add_comment(fromUserName,content)
    # 进行绑定操作，其他操作都需要绑定
    if inputParams[0] == '@':
        res = '感谢您的留言！'
        return compound_msg_text(toUserName, fromUserName, res)
    elif inputParams[0] in ['成绩','成绩查询']:
        if User.get_by_openid(fromUserName):
            out = weixin_return_template.RT_score % (fromUserName, toUserName, str(int(time.time())), fromUserName)
        else:
            out = weixin_return_template.RT_register % (fromUserName, toUserName, str(int(time.time())), fromUserName)
        return out
    elif inputParams[0] in ['绑定','绑定成绩']:
        out = weixin_return_template.RT_register % (fromUserName, toUserName, str(int(time.time())), fromUserName)
        return out
    res = '感谢您的留言！现在可以回复[绑定]'
    return compound_msg_text(toUserName, fromUserName, res)

# 对于用户点击菜单的时间进行相应
def response_msg_click(request):
    xmlstr = ET.fromstring(request)
    toUserName = xmlstr.find('ToUserName').text
    fromUserName = xmlstr.find('FromUserName').text
    eventKey = xmlstr.find('EventKey').text
    if eventKey == 'mystudy':
        if User.get_by_openid(fromUserName):
            out = weixin_return_template.RT_score % (fromUserName, toUserName, str(int(time.time())), fromUserName)
        else:
            out = weixin_return_template.RT_register % (fromUserName, toUserName, str(int(time.time())), fromUserName)
        return out

    returncontent = '/:heart  其他暂时都不可用.'
    return compound_msg_text(toUserName, fromUserName, returncontent)
