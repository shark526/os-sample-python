#coding:utf-8
import traceback
import json
import urllib2
from flask import Flask,request
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")
import hashlib, time
import xml.etree.ElementTree as ET
import aqiAPI
import xiaoi
import time_convert

application = Flask(__name__)
#from flask.ext.jsonpify import jsonify
wechat_token='ttookkeenn'

def check_signature(signature, timestamp, nonce):
    token = wechat_token
    tmp_arr = [token, timestamp, nonce]
    tmp_arr.sort()
    tmp_str = tmp_arr[0] + tmp_arr[1] + tmp_arr[2]
    sha1_tmp_str = hashlib.sha1(tmp_str).hexdigest()
    if (sha1_tmp_str == signature) :
        return True
    else :
        return False


@application.route('/wechat/', methods=['GET', 'POST'])
def respond():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')

    if request.method == 'GET':
        if check_signature(signature, timestamp, nonce) :
            return echostr
        else :
            return 'Not Valid!'
    else :
        # if check_signature(signature, timestamp, nonce) :
        xml_recv = ET.fromstring(request.data)
        #text,image,voice,location ...
        MsgType = xml_recv.find("MsgType").text
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        replyContent = ""
        if(MsgType=="text"):
            input_content = xml_recv.find("Content").text.lower()
            
            if "kq" == input_content:
                replyContent = aqiAPI.getRecentAqi(FromUserName)
            elif "#time" in input_content:
                replyContent = time_convert.convert_date(input_content)
            elif u"空气" in input_content:
                replyContent = aqiAPI.getAQIByCityName(FromUserName,input_content)
            else:
		#return ""
                replyContent = xiaoi.get_answer(input_content,FromUserName )

        elif MsgType=="location":
            LocationX = xml_recv.find("Location_X").text
            LocationY = xml_recv.find("Location_Y").text
            location_lable = xml_recv.find("Label").text
            replyContent = aqiAPI.getAQIByLocation(FromUserName,LocationX + ";" + LocationY,location_lable)
	else:
	    return ""

        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        re_msg = (reply % (FromUserName, ToUserName, str(int(time.time())), replyContent))
        return re_msg

@application.route("/v5/weather")
def getWeather():
    aqicnUrl = "http://mapidroid.aqicn.org/aqicn/json/android/nokey/v10.json?cityID=China/%E6%88%90%E9%83%BD/%E9%87%91%E6%B3%89%E4%B8%A4%E6%B2%B3"
    url = "https://api.heweather.com/v5/weather?key=66a5858fdf344933b7a585bb56a906a8&city=CN101270107&lang=zh-cn"

    urlBase = "https://api.heweather.com/v5/weather?"
    urlParams = request.args.items()
    if len(urlParams)>0:
        for para in urlParams:
            urlBase += para[0] + "=" + para[1] + "&"
        url = urlBase

    response1 = urllib2.urlopen(aqicnUrl)
    response = urllib2.urlopen(url)
    data1 = json.loads(response1.read())
    data = json.loads(response.read())
    if(data1 and data):
        data['HeWeather5'][0]['aqi']['city']['pm25'] = data1['a']
    return json.dumps(data) 

if __name__ == "__main__":
    application.run(host='0.0.0.0')

