# 学院新闻订阅
自动抓去新通知发送邮箱

## 依赖安装

1、[wkhtmltoimage](https://wkhtmltopdf.org/) 网页保存图片/PDF工具

2、python3, 需要hashlib与stmplib

* 如果要定时执行，在linux上可以用crontab


## 使用
修改news_rss.py中的config
```
config = {
    'days': 0, #检索时间范围(往前检索多少天，以避免岁月史书)
    'college': '药学院', # 学院名
    'tolist':[''], #接收邮箱列表
    'path':'.', #本目录地址,如用crontab需要配置绝对路径
    'wkhtmltoimage_path':'path_to_wkhtmltoimage', #wkhtmltoimage路径
    'email':'', #发件邮箱地址
    'stmp_key':'', #发件邮箱stmp key
    'stmp_server':'smtp.126.com', #发件邮箱stmp服务器
    'stmp_port':465 #发件邮箱stmp服务器端口
}
```
然后运行python news_rss.py 即可
