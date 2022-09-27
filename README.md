# push_wechat_for_girl

## 项目介绍
<font color="blue">
    Python菜鸟学习项目
    每日向微信公众号定时推送天气、气温、风向、能见度、每日情话等信息
</font>

## 准备工作
1. 微信公众平台接口测试账号链接：https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login   
2. 获取appid、appsecret、微信号、模板id等信息
3. 在 config.conf 里面对应填写配置信息

## 本项目的模板
```text
{{name.DATA}},今天是 {{date.DATA}} 
地区：{{region.DATA}} 
天气：{{weather.DATA}} 
气温：{{temp.DATA}} 
风向：{{wind_dir.DATA}}
能见度：{{vis.DATA}}
今天是我们相恋的第{{love_day.DATA}}天 
{{birthday1.DATA}} 
{{birthday2.DATA}} 
{{honeywords.DATA}} 
```

## 和风天气API相关链接
和风天气开放平台（注册登录）：https://dev.qweather.com/   
控制台创建应用（获取Key）：https://console.qweather.com/#/apps?lang=zh  