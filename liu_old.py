from urllib import request
import json
import time
import logging
from fake_useragent import UserAgent
from datetime import datetime, timedelta
import requests


def getDate():
    now_time = datetime.now()
    utc_time = now_time + timedelta(hours=8) 
    utc_time = utc_time.strftime("%Y-%#m-%#d")
    return utc_time


hour = 6
minute = 59
second = 58
openid = "o-WiZ5QBscle7YmWjhgcS8J-zESU"  # 感觉是每个人的ID，不同人的ID不一样
SendKey = "SCT149167TcjYlDaLEJQfKSDtS8LKeAaGU"  # 方糖的微信推送码, 由平台给出

# 过滤条件
region = "八中"  # 地区
seatNLName = "22桌 F座"  # 座位名称
seatShortName = '-1'  # 座位号 : '1' 'A' 'F' 等

RequestCnt = 1000  # 表示一共要请求的次数，每0.1s请求一次

starttime = "1"  # 开始时间，默认从系统中获取，早上7:00
endtime = "1"  # 结束时间，默认从系统中获取，晚上22:00
day = getDate()

TotalRequest = 0
MyFlag = False
RepeatBook = "666"
GetSeatListFailed = "1111"
SeatUsed = "1122"
SuccessBook = "200"
SystemClosed = "201"
UnknowError = "403"
SeatLocked = "408"
regionNameList = {
    '三东北': {'name': '三层东书库北区', 'layerid': 3, 'regionId': 7},
    '三东南': {'name': '三层东书库南区', 'layerid': 3, 'regionId': 8},
    '三中': {'name': '三层中区', 'layerid': 3, 'regionId': 46},
    '三西北': {'name': '三层西书库北区', 'layerid': 3, 'regionId': 9},
    '三西南': {'name': '三层西书库南区', 'layerid': 3, 'regionId': 10},
    '四东北': {'name': '四层东书库北区', 'layerid': 4, 'regionId': 11},
    '四东南': {'name': '四层东书库南区', 'layerid': 4, 'regionId': 12},
    '四中': {'name': '四层中区', 'layerid': 4, 'regionId': 42},
    '四西北': {'name': '四层西书库北区', 'layerid': 4, 'regionId': 13},
    '四西南': {'name': '四层西书库南区', 'layerid': 4, 'regionId': 14},
    '五东北': {'name': '五层东书库北区', 'layerid': 5, 'regionId': 15},
    '五东南': {'name': '五层东书库南区', 'layerid': 5, 'regionId': 16},
    '五中': {'name': '五层中区', 'layerid': 5, 'regionId': 17},
    '五西北': {'name': '五层西书库北区', 'layerid': 5, 'regionId': 18},
    '五西南': {'name': '五层西书库南区', 'layerid': 5, 'regionId': 19},
    '六东北': {'name': '六层东书库北区', 'layerid': 6, 'regionId': 20},
    '六东南': {'name': '六层东书库南区', 'layerid': 6, 'regionId': 21},
    '六中': {'name': '六层中区', 'layerid': 6, 'regionId': 43},
    '六西北': {'name': '六层西书库北区', 'layerid': 6, 'regionId': 22},
    '六西南': {'name': '六层西书库南区', 'layerid': 6, 'regionId': 23},
    '七东北': {'name': '七层东书库北区', 'layerid': 7, 'regionId': 24},
    '七东南': {'name': '七层东书库南区', 'layerid': 7, 'regionId': 25},
    '七中': {'name': '七层中区', 'layerid': 7, 'regionId': -1},
    '七西北': {'name': '七层西书库北区', 'layerid': 7, 'regionId': 26},
    '七西南': {'name': '七层西书库南区', 'layerid': 7, 'regionId': 27},
    '八东北': {'name': '八层东书库北区', 'layerid': 8, 'regionId': 28},
    '八东南': {'name': '八层东书库南区', 'layerid': 8, 'regionId': 29},
    '八中': {'name': '八层中区', 'layerid': 8, 'regionId': 30},
    '八西北': {'name': '八层西书库北区', 'layerid': 8, 'regionId': 31},
    '八西南': {'name': '八层西书库南区', 'layerid': 8, 'regionId': 32},
    '九东北': {'name': '九层东书库北区', 'layerid': 9, 'regionId': 33},
    '九东南': {'name': '九层东书库南区', 'layerid': 9, 'regionId': 34},
    '九中': {'name': '九层中区', 'layerid': 9, 'regionId': 37},
    '九西北': {'name': '九层西书库北区', 'layerid': 9, 'regionId': 35},
    '九西南': {'name': '九层西书库南区', 'layerid': 9, 'regionId': 36},
    '十东北': {'name': '十层东书库北区', 'layerid': 10, 'regionId': 38},
    '十东南': {'name': '十层东书库南区', 'layerid': 10, 'regionId': 39},
    '十中': {'name': '十层中区', 'layerid': 10, 'regionId': -1},
    '十西北': {'name': '十层西书库北区', 'layerid': 10, 'regionId': 40},
    '十西南': {'name': '十层西书库南区', 'layerid': 10, 'regionId': 41}
}

Host = "172.18.249.143"
headers = {
    "Connection": "keep-alive",
    "User-Agent": UserAgent().random,
    "content_type": "application/json;charset=UTF-8",
    "Referer": "https://servicewechat.com/wx31f64ed54d4615c0/39/page-frame.html",
    "Accept_Encoding": "gzip, deflate, br"
}


# 微信消息推送
def send_message(status, request_cnt):
    title = "很遗憾,抢座失败!"
    url = 'https://sc.ftqq.com/' + SendKey + '.send'

    if status == 1:
        title = "恭喜您,抢座成功! 美好的一天又开始了!"

    message = "请求次数" + str(request_cnt)
    data = {
        'text': title,
        'desp': message
    }

    requests.post(url, data=data)


def getSeatId():
    if regionNameList.__contains__(region) == False:
        # print("The region you is not in dictionary's keyList")
        logger.error("The region you is not in dictionary's keyList")
        exit(0)
    layerid = regionNameList[region]['layerid']
    regionId = regionNameList[region]['regionId']
    if regionId == -1:
        # print("this region doesn't exsit!")
        logger.error("this region doesn't exsit!")
        exit(0)
    url = "https://wplib.haut.edu.cn/seatbook/api/seatbook/query?" \
          "starttime=" + day + "%2021%3A29%3A00&" \
                               "endtime=" + day + "%2021%3A30%3A00&" \
                                                  "layerid=" + str(layerid) + "&" \
                                                                              "regionid=" + str(regionId)
    req = request.Request(url=url, headers=headers)
    response = request.urlopen(req)
    global TotalRequest
    TotalRequest += 1
    html = response.read().decode('utf-8')
    dictionary = json.loads(html)
    if (dictionary.__contains__('seatList')):
        seatList = dictionary['seatList']
        for i in range(len(seatList)):
            seat = seatList[i]
            if filterSeat(seat):
                # print("success get the seat!")
                logger.info("Success get the seat!")
                return seat
    else:
        logger.warning("seatList get Failed!")
        return GetSeatListFailed


def filterSeat(seat):
    regionName = regionNameList[region]['name']
    ret = False
    if seat['regionName'] == regionName and (
            seat['seatNLName'] == seatNLName or seat['seatShortName'] == seatShortName):
        ret = True
    return ret


def bookSeat(seat):
    print("seat['isCan'] = " + seat['isCan'])
    global TotalRequest
    if seat['isCan'] != '1':
        send_message(0, TotalRequest)
        logger.warning("seat has been occured!")
        return SeatUsed
    else:
        seatId = str(seat['id'])
        url = "https://wplib.haut.edu.cn/seatbook/api/seatbook/addbooking?" \
              "bookingdate=null&" \
              "regionid=null&" \
              "channel=1003&" \
              "openid=" + openid + "&" \
                                   "seatid=" + seatId + "&" \
                                                        "starttime=" + day + "%2007%3A30%3A00&" \
                                                                             "endtime=" + day + "%2020%3A59%3A00"
        req = request.Request(url=url, headers=headers, method="GET")
        response = request.urlopen(req)
        TotalRequest += 1
        html = response.read().decode('utf-8')
        logger.info(html)
        json_msg = json.loads(html)
        if html == '{"msg":"本座位已锁定 请稍后再试","code":1122}':
            # print("seat has been locking!")
            logger.warning("seat has been locking!")
            return SeatLocked
        elif html == '{"msg":"你已有其他预约，不可重复预约！","code":666}':
            # print("You have booked a seat,can repeat book seat!")
            logger.error("You have booked a seat,can repeat book seat!")
            return RepeatBook
        elif html == '{"msg":"系统关闭，不可预约!系统将在7:00时间后开启预约","code":666}':
            print("System haven't opened!")
            return SystemClosed
        elif json_msg.__contains__("readerno") and json_msg.__contains__("seatName"):
            logger.info("Book Successful!")
            send_message(1, TotalRequest)
            # {"code":0,"readerno":"201916040117","seatName":"五层东书库北区 07桌 C座",
            # "list":null,"seatsno":"五层东书库北区 07桌 C座","bookingid":4867078,"realname":"刘培正"}
            return SuccessBook
        else:
            logger.info("UnknowError!")
            return UnknowError


def robSeat():
    global MyFlag
    if MyFlag:
        pass
    else:
        seat = getSeatId()
        if seat == GetSeatListFailed or seat == "111":
            pass
        else:
            status = bookSeat(seat)
            if status == SuccessBook:  # 成功预约了座位
                MyFlag = True
            elif status == RepeatBook:  # 已经预约了座位
                MyFlag = True
            elif status == SeatUsed:  # isCan = 0,这个座位被人预约走了，包括自己预约走
                MyFlag = True
            print(seat)


def work():
    for i in range(RequestCnt):
        try:
            robSeat()
        except Exception as e:
            print(e)
    global TotalRequest
    print('Total Request = ' + str(TotalRequest))
    logger.info("-------------------------------------------------------------")
    logger.info('Total Request = ' + str(TotalRequest))
    logger.info("-------------------------------------------------------------")


def logger_config(log_path, logging_name):
    '''
    配置log
    :param log_path: 输出log路径
    :param logging_name: 记录中name，可随意
    :return:
    '''
    '''
    logger是日志对象，handler是流处理器，console是控制台输出（没有console也可以，将不会在控制台输出，会在日志文件中输出）
    '''
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)
    # 输出DEBUG及以上级别的信息，针对所有输出的第一层过滤
    logger.setLevel(level=logging.DEBUG)
    # 获取文件日志句柄并设置日志级别，第二层过滤
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    # 生成并设置文件日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # console相当于控制台输出，handler文件输出。获取流句柄并设置日志级别，第二层过滤
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # 为logger对象添加句柄
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


logger = logger_config(log_path='log.txt', logging_name='-----')

if __name__ == '__main__':
    work()
