# -*- coding: utf-8 -*-
import json
import urllib2
import pinyin
import dbservice
from datetime import datetime
import pytz

aqiToken = "afd1d144aad6b459aa2fd3c436611434faf937ad"
locationAPIUrl = "http://api.waqi.info/feed/geo:%s/?token=%s"
cityAPIUrl = "http://api.waqi.info/feed/%s/?token=%s"
queryResultString = u"当前空气质量指数是:%s %s\r\n数据采集时间:%s点\r\n"
queryErrorString = u"嘢?找不到你要的数据呢,要不换个姿势再试试?"
return_msg_template = u"您查询的是:%s\r\n%s"
tz = pytz.timezone("Asia/Shanghai")
wrong_city_input = u"哎呀呀， 您输入的城市名称好像有点问题呢， 要不换个试试？"
AirPollutionLevel= [
    [50,u"一级(优)"],
    [100,u"二级(良)"],
    [150,u"三级(轻度污染)"],
    [200,u"四级中度污染"],
    [300,u"五级(重度污染)"],
    [1000,u"六级(严重污染)"]]

def to_pinyin(var_str):
    if (isinstance(var_str, str)or isinstance(var_str,unicode)):
        if var_str == 'None':
            return ""
        else:
            return pinyin.get(var_str, format='strip', delimiter="")
    else:
        return 'wrong'

def requestAQI(userid,para, qtype,qcity):
    try:
        if qtype=="c":
            qurl = cityAPIUrl % (para,aqiToken)
        else:
            qurl = locationAPIUrl % (para,aqiToken)
        data = json.loads(urllib2.urlopen(qurl).read()) 
        if data["status"]=="ok":        
            returnMessage = (data["data"]["aqi"],data["data"]["time"]["s"].replace(":00:00",""))
            #save to db
            userinfo = (userid, para, qcity, qtype,str(returnMessage[1]), datetime.now(tz).strftime('%Y-%m-%d %H'), str(returnMessage[0]))
            dbservice.update_user_info(userinfo)
        else:
            return "wrong"
        
    except:
        returnMessage = "error occured when request aqi: %s %s" % (para, qtype)#traceback.format_exc()
    return returnMessage

def get_aqi_level(aqivalue):
    curlevel = None
    for level in AirPollutionLevel:
        if int(aqivalue) < level[0] :
            curlevel = level[1]
            break
    return curlevel

def get_final_return_msg(cityname, returndata):
    if len(returndata)<2:
        return queryErrorString
    aqilevel =  get_aqi_level(returndata[0])
    finalmsg = queryResultString % (returndata[0],aqilevel,returndata[1])
    finalmsg = return_msg_template %(cityname,finalmsg)
    return finalmsg

def getAQIByCityName(userid,input_content):

    cityName = input_content.lstrip().strip().replace(u"空气","")
    pycityName = to_pinyin(cityName)
    if pycityName == "wrong":
        return wrong_city_input
    returndata= requestAQI(userid,pycityName, "c",cityName)
    if len(returndata)>2 and returndata=="wrong":
        return wrong_city_input
    returnMessage = get_final_return_msg(cityName, returndata)
    return returnMessage

def getAQIByLocation(userid,location,location_lable):

    returndata = requestAQI(userid,location, "l",location_lable)
    returnMessage = get_final_return_msg(location_lable, returndata)
    return returnMessage

def getRecentAqi(userid):
    try:
        #get data from db
        qresult = dbservice.get_user_info((userid,))
        #[(u'fkfuks211', u'123.5,1354.3', u'chengdu', u'l', u'2017-09-02 23', u'88')]
        if len(qresult)>0:
            qlocation = qresult[0][1]
            qcity = qresult[0][2]
            qtype = qresult[0][3]
            qutime = qresult[0][4]
            qtime = qresult[0][5]
            qvalue = qresult[0][6]
            curtime = datetime.now(tz).strftime('%Y-%m-%d %H')
            if qtime==curtime:
                # returnMessage = (queryResultString % (qvalue,curtime))
                # returnMessage = return_msg_template %(qcity,returnMessage)
                returnMessage = get_final_return_msg(qcity, (qvalue,curtime))
            else:
                #query via api
                if qtype=="l":
                    returnMessage = getAQIByLocation(userid,qlocation,qcity)
                else:
                    returnMessage = getAQIByCityName(userid,qcity)
        else:
            returnMessage = u"没找到您最近一次查询呢, 请按照步骤按城市名或发送位置再查一次,这次我一定记住;-)"
    except:
        returnMessage = "error occured when getRecentAqi for user: %s" % (userid)
    return returnMessage


if __name__ == '__main__':
    pass
    # print getAQIByLocation("user1","123;456", "cdd lable")
    # print getAQIByCityName("user2",u"沈")
    # print getRecentAqi("user1")
    # print getRecentAqi("fkfuk")
