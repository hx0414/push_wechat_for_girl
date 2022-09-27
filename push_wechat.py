from datetime import date,datetime
from time import localtime, sleep
import os,sys,time
from requests import get,post
from zhdate import ZhDate



# 获得令牌
def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token
   
   
def get_weather(region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    key = config["weather_key"]
    region_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(region, key)
    response = get(region_url,headers=headers).json()
    if response["code"] == "404":
        print("推送消息失败，请检查地区名是否有误！")
        os.system("pause")
        sys.exit(1)
    elif response["code"] == "401":
        print("推送消息失败，请检查和风天气key是否正确！")
        os.system("pause")
        sys.exit(1)
    else:
        # 获取地区的location--id
        location_id = response["location"][0]["id"]
    weather_url = "https://devapi.qweather.com/v7/weather/now?location={}&key={}".format(location_id, key)
    response = get(weather_url, headers=headers).json()
    # 天气
    weather = response["now"]["text"]
    # 当前温度
    temp = response["now"]["temp"] + u"\N{DEGREE SIGN}" + "C"
    # 风向
    wind_dir = response["now"]["windDir"]
    # 可见度
    vis = response["now"]["vis"]
    return weather,temp,wind_dir,vis

def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 获取农历生日的今年对应的月和日
        try:
            birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        except TypeError:
            print("请检查生日的日子是否在今年存在")
            os.system("pause")
            sys.exit(1)
        birthday_month = birthday.month
        birthday_day = birthday.day
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)

    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day
    
# 获取每日情话
def get_honeywords():
    url = "https://api.vvhan.com/api/love?type=json"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    return r.json()["ishan"]


# 发送信息
# 参数：目标用户、令牌、地区、天气、气温、风力、可见度、每日情话
def send_msg(_users,_token,_region,_weather,_temp,_wind,_vis,_honeywords):
    # 令牌url
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(_token)
    # 获取日期和星期
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year,month=month,day=day))
    weeklist = ["星期日","星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    week = weeklist[today.isoweekday()%7]
    # 得到恋爱时长
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v    
    # 发送数据格式
    data = {
        "touser":_users,
        "template_id":config['template_id'],
        "url":"http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data":{
            "date":{
                "value": "{} {}".format(today,week),
                "color": ""
            },
            "name":{
                "value": config["name"],
                "color": "#FFB6C1"
            },
            "region":{
                "value": _region,
                "color": ""
            },
            "weather":{
                "value": _weather,
                "color": ""
            },
            "temp":{
                "value": _temp,
                "color": ""
            },
            "wind_dir":{
                "value": _wind,
                "color": ""
            },
            "vis":{
                "value": _vis,
                "color": ""
            },
            "lovedays":{
                "value": love_days,
                "color": "#6B1149"
            },
            "honeywords":{
                "value": "来自悄悄话："+_honeywords,
                "color": ""
            },
        } 
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value["birthday"], year, today)
        if birth_day == 0:
            birthday_data = "今天{}生日哦，祝{}生日快乐！".format(value["name"], value["name"])
        else:
            birthday_data = "距离{}的生日还有{}天".format(value["name"], birth_day)
        # 将生日数据插入data
        data["data"][key] = {"value": birthday_data, "color": "#FFB6C1"}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("[{}]推送消息成功".format(now))
    else:
        print(response)
    return 


if __name__ == "__main__":
    # 读取配置文件
    try:
        with open("./config.conf") as fd:
            config = eval(fd.read())
            print(config)
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)
        
    # 获取accessToken
    accessToken = get_access_token()
    # 用户信息
    users = config["user"]
    # 地区信息
    region = config["region"]
    # 天气信息
    weather,temp,wind_dir,vis = get_weather(region)
    # 获取每日情话
    honeywords = get_honeywords()
    # 每天定点发送，9：30、17：30
    notice_time = config["notice_time"]
    time_list = []
    for t in notice_time:
        t_hour,t_min = int(t.split(':')[0]), int(t.split(':')[1])
        time_list.append(f'{t_hour}.{t_min}')
    # 无限循环
    # 计算现在的时间，如果是目标时间，推送
    while 1==1:
        timeArray = time.localtime(time.time())
        # now = datetime.datetime.now().strftime('%H:%M')
        now_time = f'{int(timeArray.tm_hour)}.{int(timeArray.tm_min)}'
        if now_time in time_list:
            for user in users:
                send_msg(user,accessToken,region,weather,temp,wind_dir,vis,honeywords)
            # 延时，避免同时间发送太多次
            time.sleep(60)