# ZJU学院新闻订阅
自动ZJU抓取新通知发送邮箱

> 可按以下方式本地部署，也可直接订阅[mlab订阅服务](https://proxy.ocmlab.top/zju2024email)

## 依赖安装

1、[wkhtmltoimage](https://wkhtmltopdf.org/) 网页保存图片/PDF工具

2、python3, 需要hashlib与stmplib

* 如果要定时执行，在linux上可以用crontab


## 使用方法
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

## 当前支持学院
-  文学院
-  历史学院
-  哲学学院
-  外国语学院
-  传媒与国际文化学院
-  艺术与考古学院
-  经济学院
-  光华法学院
-  教育学院
-  管理学院
-  公共管理学院
-  马克思主义学院
-  数学科学学院
-  物理学院
-  化学系
-  地球科学学院
-  心理与行为科学系
-  机械工程学院
-  材料科学与工程学院
-  能源工程学院
-  电气工程学院
-  建筑工程学院
-  化学工程与生物工程学院
-  海洋学院
-  航空航天学院
-  高分子科学与工程学系
-  光电科学与工程学院
-  信息与电子工程学院
-  控制科学与工程学院
-  计算机科学与技术学院
-  软件学院
-  生物医学工程与仪器科学学院
-  集成电路学院
-  生命科学学院
-  生物系统工程与食品科学学院
-  环境与资源学院
-  农业与生物技术学院
-  动物科学学院
-  医学院
-  药学院
