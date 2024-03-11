import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import requests
import datetime
import base64
import re
import json
import hashlib

config = {
    'days': 0, #检索时间范围(往前检索多少天，以避免岁月史书)
    'college': '药学院', # 学院名
    'tolist':[''], #接收邮箱列表
    'path':'.', #本目录地址,如用crontab需要配置绝对路径
    'wkhtmltoimage_path':'path_to_wkhtmltoimage', #wkhtmltoimage路径(用于下载网页)
    'email':'', #发件邮箱地址
    'stmp_key':'', #发件邮箱stmp key
    'stmp_server':'smtp.126.com', #发件邮箱stmp服务器
    'stmp_port':465 #发件邮箱stmp服务器端口
}

with open(config['path']+'/colleges.json', 'r') as file:
    colleges = json.load(file)
    colleges_r = dict([(k[0],v) for v,k in colleges.items()])

def get_date_new(date, page=1):
    name, host, params = colleges[colleges_r[config['college']]]
    host = host.split('zju.edu.cn')[0] + 'zju.edu.cn/'
    # host = 'https://webplus.zju.edu.cn/'
    params = (base64.b64encode(params.encode('utf-8'))).decode('utf-8')
    data = '[{"field":"pageIndex","value":'+str(page)+'},{"field":"group","value":0},{"field":"searchType","value":"1"},{"field":"keyword","value":""},{"field":"recommend","value":"1"},{"field":4,"value":""},{"field":5,"value":""},{"field":6,"value":"'+date+'"},{"field":7,"value":""}]'
    data = 'searchInfo='+(base64.b64encode(data.encode('utf-8'))).decode('utf-8')
    header = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': host+'_web/_search/api/search/new.rst'
    }
    # params = 'YXM9NTM4JnQ9MTM1NyZkPTU1NDYmcD0xJm09U04m'
    res = requests.post(host+'_web/_search/api/searchCon/create.rst?_p='+params, data=data, headers=header)
    rep_data = [x.strip() for x in json.loads(res.text)['data'].split('\r\n') if len(x.strip()) > 0]
    title = [re.sub(r'.*target="_blank">(.*)</a>.*',r'\1',x) for x in rep_data]
    url = [re.sub(r'.*(http.*)\' target="_blank">.*',r'\1',x) for x in rep_data]
    date = [re.sub(r'.*发布时间:(.*?) .*</span>.*',r'\1',x) for x in rep_data]
    # url = 'https://webplus.zju.edu.cn'+re.sub(r'.*item_title"> <a href=\'(.*psp).*',r'\1',rep_data)
    return list(zip(title, date, url))

def send_email(data, tolist):
    name, host, params = colleges[colleges_r[config['college']]]
    title, date, url = data
    title = re.sub(r'/', '_', title)
    _hash = hashlib.md5(title.encode(encoding='UTF-8')).hexdigest()
    file_path = os.path.normpath(f'{config["path"]}/cache/{config["college"]}_{date}_{str(_hash)}.jpg')
    if os.path.exists(file_path):
#        print("news has been sent")
        return 0
    if title.find('因公出')>-1:
#        print(f"skip {title}")
        return 0
    os.system(f'{config["wkhtmltoimage_path"]} {url} {file_path}')
    if not os.path.exists(file_path):
        os.system(f'touch {file_path}')
    smtp = smtplib.SMTP_SSL(config['stmp_server'],config['stmp_port'])
    smtp.login(config['email'], config['stmp_key'])
    msg = MIMEMultipart('mixed')
    imageApart = MIMEImage(open(file_path, 'rb').read(), 'jpg')
    imageApart.add_header('Content-ID', '<image1>')
    msg.attach(imageApart)
    html = f"""
<html>
<head></head>
<body>
<br>
<p> 页面链接：{url} </p>
<p> 页面标题：{title}</p>
<br>
<img src="cid:image1">
<br>
</body>
</html>
"""
    text = MIMEText(html, 'html', 'utf-8')
    msg.attach(text)
    msg['Subject'] = f'{name}：{title}'
    msg['From'] = config['email']
    msg['To'] = "Subscriber"
    for user in tolist:
        msg.replace_header('To', user)
        smtp.sendmail(config['email'], user, msg.as_string())
    smtp.quit()
    return 1

if __name__ == '__main__':
    day = datetime.date.today() - datetime.timedelta(days=config['days'])
    tolist = config['tolist']
    if len(tolist) == 0:
        print("请设置接收邮箱")
        exit()
    if config['college'] not in colleges_r:
        print("学院名称有误，请从以下学院名称中选择配置：")
        print('\t' + '\n\t'.join(colleges_r.keys()))
        exit()
    news = []
    page = 1
    while True:
        new = get_date_new(str(day), page=page)
        page += 1
        if len(new) == 0:
            break
        else:
            news += new
    n = 0
    for new in news:
        n += send_email(new, tolist)
    with open(config['path']+'/log.txt', 'a') as file:
        file.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] send {config['college']} {n} news\n")
