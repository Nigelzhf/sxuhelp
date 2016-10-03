RT_txt = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>'''


#成绩查询
RT_score = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>1</ArticleCount>
<Articles>
<item>
<Title><![CDATA[成绩查询结果]]></Title>
<Description><![CDATA[点击查看(具体以教务处为准)\n如果有成绩没出请及时联系教务处]]></Description>
<PicUrl><![CDATA[http://winter1ife.qiniudn.com/weixin/titlebar/score_boy.jpg]]></PicUrl>
<Url><![CDATA[http://re_domain/myscore?openid=%s]]></Url>
</item>
</Articles>
</xml>'''

#成绩查询
RT_register = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>1</ArticleCount>
<Articles>
<item>
<Title><![CDATA[点击进行绑定]]></Title>
<Description><![CDATA[点击进行绑定]]></Description>
<PicUrl><![CDATA[http://winter1ife.qiniudn.com/weixin/titlebar/score_boy.jpg]]></PicUrl>
<Url><![CDATA[http://re_domain/register?openid=%s]]></Url>
</item>
</Articles>
</xml>'''
