# coding=utf-8
import cetdes
from random import randint
from tornado.httpclient import HTTPRequest
from urllib.parse import urlencode
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine


def random_mac():
    return '%.2X-%.2X-%.2X-%.2X-%.2X-%.2X' % (randint(0, 16),
            randint(0, 16), 
            randint(0, 16),
            randint(0, 16), 
            randint(0, 16),
            randint(0, 16)
            )

class CetCipher(object):

    ticket_number_key = '(YesuNRY'
    request_data_key = '?!btwNP^'

    ticket_number_enc_key = ')XdsuORX'
    ticket_number_dec_key = '(YesuNRY'

    DECRYPT = 0
    ENCRYPT = 1

    def decrypt_ticket_number(self, ciphertext):
        ciphertext = ciphertext[2:]
        return cetdes.cetdes(ciphertext, self.ticket_number_key, self.DECRYPT)

    def encrypt_ticket_number(self, ticket_number):
        ciphertext = cetdes.cetdes(ticket_number,
                                       self.ticket_number_key, self.ENCRYPT)
        ciphertext = '\x35\x2c' + ciphertext
        return ciphertext

    def decrypt_request_data(self, ciphertext):
        return cetdes.cetdes(ciphertext, self.request_data_key, self.DECRYPT)

    def encrypt_request_data(self, request_data):
        return cetdes.cetdes(request_data, self.request_data_key, self.ENCRYPT)

    def encrypt_ticket_number(self, ticket_number):
        ciphertext = cetdes.cetdes(ticket_number,
                                       self.ticket_number_enc_key, self.ENCRYPT)
        return ciphertext

    def decrypt_ticket_number(self, ciphertext):
        ciphertext = ciphertext[2:]
        return cetdes.cetdes(ciphertext, self.ticket_number_enc_key, self.DECRYPT)

class CetTicket(object):

    search_url = 'http://find.cet.99sushe.com/search'
    score_url = 'http://cet.99sushe.com/findscore'

    CET4 = 1
    CET6 = 2

    @classmethod
    def find_ticket_number(cls, province, school, name, examroom='', cet_type=1):
        import pdb;pdb.set_trace()
        cipher = CetCipher()
        province=int(province)
        # province_id = CetConfig.PROVINCE[province]
        param_data = 'type=%d&provice=%d&school=%s&name=%s&examroom=%s&m=%s' % (
                cet_type,
                province,
                school,
                name, 
                examroom,
                random_mac()
                )

            param_data = param_data.encode('gb2312')
            encrypted_data = cipher.encrypt_request_data(param_data)
            #print (''.join( [ "%02X:" % x for x in encrypted_data ]).strip())
            httpclient=AsyncHTTPClient()
            headers={'Accept':'*/*','Connection':'keep-alive'}
            resp=yield httpclient.fetch(cls.search_url,method='POST',body=encrypted_data,headers=headers)

            # decrypt
            ticket_number = cipher.decrypt_ticket_number(resp.body)
            if not ticket_number:
                return None
            return ticket_number.decode()

    @classmethod
    def get_score(cls, ticket_number, name):
        name = name.encode('gb2312')
        params_dict = {
            'id': ticket_number,
            'name': name[:4]
        }
        httpclient=AsyncHTTPClient()
        resp=yield httpclient.fetch(cls.score_url,method='POST',body=urlencode(params_dict),headers={'Referer': 'http://cet.99sushe.com/'})

        score_data = resp.body.decode('gb2312')
        if len(score_data) < 10:
            return None
        score_data = score_data.split(',')

        score = {
            'name': score_data[6],
            'ticket': ticket_number,
            'school': score_data[5],
            'listening': score_data[1],
            'reading': score_data[2],
            'writing': score_data[3],
            'total': score_data[4]
        }
        return score

if __name__=='__main__':
    print(CetTicket.find_ticket_number('山西', '山西大学', '许栋武', cet_type=CetTicket.CET6))
    pass
