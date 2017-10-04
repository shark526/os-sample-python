#coding:utf-8
"""#time cn 20170312 13:00"""
import pytz
from dateutil.parser import parse,tz

DATE_FROMAT = "%Y-%m-%d %H:%M:%S"
tz_cn = pytz.timezone('Asia/Shanghai')
tz_au = pytz.timezone('Australia/Melbourne')
tz_in = pytz.timezone('Asia/Kolkata')
final_format = "中国:%s\r\n澳洲:%s\r\n印度:%s"
error_format = "呃...输入格式好像有点问题呢, 请发送格式: '#time cn 20170913 09:00', 其中'cn'代表中国, 目前支持au(澳大利亚), in(印度)"

def convert_date(time_str):
    tz_flag = "" 
    match = next((x for x in [" cn "," au "," in "] if x in time_str), "")
    if len(match)>0:
        tz_flag = match.strip()
    else:
        return error_format
    try:
	ctime =  parse(time_str,fuzzy=True)
    except:
	return error_format
    rst = ""
    if tz_flag=="cn":
        localtime = tz_cn.localize(ctime)#.strftime(DATE_FROMAT)
        rst = final_format % (
            localtime.strftime(DATE_FROMAT),
            localtime.astimezone(tz_au).strftime(DATE_FROMAT),
            localtime.astimezone(tz_in).strftime(DATE_FROMAT)
        )
    elif tz_flag=="au":
        localtime = tz_au.localize(ctime)
        rst = final_format % (
            localtime.astimezone(tz_cn).strftime(DATE_FROMAT),
            localtime.strftime(DATE_FROMAT),
            localtime.astimezone(tz_in).strftime(DATE_FROMAT)
        )
    elif tz_flag=="in":
        localtime = tz_in.localize(ctime)
        rst = final_format % (
            localtime.astimezone(tz_cn).strftime(DATE_FROMAT),
            localtime.astimezone(tz_au).strftime(DATE_FROMAT),
            localtime.strftime(DATE_FROMAT)
        )
    else:
        localtime = error_format

    return rst

if __name__ == "__main__":
    print convert_date("#time au 20170312 13:00")
    #print convert_date("2017/3/12 21:00")
    print convert_date("#time cn 021:62")
