# -*- coding: utf-8 -*-

import requests

import datetime

import hashlib

import collections



XIAOI_URL = 'http://nlp.xiaoi.com/ask.do?platform=custom&question=%s&userId=%s'

API_KEY = "MuI3aBlK6kooO"

API_SEC = "1nyzMvEAAqMxaIHMXbXXK"



class IBotSignature:

    """

        It's about iBotCloud signature stuff

    """

    def __init__(self, app_key, app_sec, uri, http_method="POST", realm="xiaoi.com"):

        self.app_key = app_key

        self.app_sec = app_sec

        self.uri = uri

        self.http_method = http_method.upper()

        self.realm = realm



    def get_signature(self):

        time_str = str(datetime.datetime.now())

        nonce = hashlib.sha1(time_str).hexdigest()



        HA1 = "{0}:{1}:{2}".format(self.app_key, self.realm, self.app_sec)

        HA1 = hashlib.sha1(HA1).hexdigest()



        HA2 = "{0}:{1}".format(self.http_method, self.uri)

        HA2 = hashlib.sha1(HA2).hexdigest()



        signature = "{0}:{1}:{2}".format(HA1, nonce, HA2)

        signature = hashlib.sha1(signature).hexdigest()



        # print "signature:" + signature

        # print "nonce:" + nonce

        ret = collections.namedtuple("get_signature_reture", "signature nonce")



        ret.signature = signature

        ret.nonce = nonce



        return ret

    def get_http_header_xauth(self):

        ret_vals = self.get_signature()



        ret = {'X-Auth': "app_key=\"{0}\",nonce=\"{1}\",signature=\"{2}\"".format(self.app_key,

                                                                                    ret_vals.nonce,

                                                                                    ret_vals.signature)}



        return ret
def get_answer(question, userid):

    # if isinstance(question,unicode):

    #     print "input %s is unicode" % question

    signature_ask = IBotSignature(app_key=API_KEY,

                                    app_sec=API_SEC,

                                    uri="/ask.do",

                                    http_method="POST")

    xauth = signature_ask.get_http_header_xauth()

    http_headers = {"Content-type": "application/json",

                    "Accept": "text/plain",

                    xauth.keys()[0]: xauth.values()[0]}

    response = requests.post(XIAOI_URL %(question,userid), headers=http_headers)

    if response.status_code == 200:

        return response.text

    else:

        return response.text





if __name__ == '__main__':

    print get_answer(u"你好","aaa")
