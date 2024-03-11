import requests
import json
import datetime
from news_rss import get_date_new, get_c_name

class SendMessage(object):
    APPID = "your_app_id"
    APPSECRET = "your_app_key"
    TEMPID = "your_template_id"

    def __init__(self, app_id=APPID, app_secret=APPSECRET, template_id=TEMPID) -> None:
        """
        构造函数
        :param APPID: 微信公众测试号账号
        :param APPSECRET: 微信公众测试号密钥
        :param template_id: 模版id
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.template_id = template_id
        self.get_access_token()

    def get_access_token(self) -> str:
        """
        获取access_token凭证
        :return: access_token
        """
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        resp = requests.get(url)
        result = resp.json()
        if 'access_token' in result:
            self.access_token = result["access_token"]
            print('get access token success')
            # return result["access_token"]
        else:
            print(result)

    def get_user_list(self) -> list:
        """
        获取用户列表
        :return (usercount, ["OPENID1","OPENID2"])
        """
        url = f"https://api.weixin.qq.com/cgi-bin/user/get?access_token={self.access_token}"
        resp = requests.get(url)
        result = resp.json()
        if 'data' in result:
            return (result["count"], result["data"]["openid"])
        else:
            print(result)
            
    def get_send_data(self, json_data) -> object:
        """
        获取发送消息data
        :param json_data: json数据对应模板
        :return: 发送的消息体
        """
        return {
            "touser": json_data["touser"],
            "template_id": self.template_id,
            "url": json_data["url"],
            "topcolor": "#FF0000",
            # json数据对应模板
            "data": {
                "college":{
                    "value": json_data["college"],
                },
                "title": {
                    "value": json_data["title"],
                },
                "date": {
                    "value": json_data["date"],
                },
                "url": {
                    "value": json_data["url"],
                },
            }
        }

    def send_message(self, json_data) -> None:
        """
        发送消息
        :param json_data: json数据
        :return:
        """
        # 模板消息请求地址
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={self.access_token}"
        data = json.dumps(self.get_send_data(json_data))
        resp = requests.post(url, data=data)
        result = resp.json()
        if result["errcode"] == 0:
            print("消息发送成功")
        else:
            print(result)


if __name__ == '__main__':

    to_dict = {
        "your_user_id": 'your_subscribe_colleges_shortname'
    }

    sm = SendMessage()
    day = datetime.date.today()

    count, user_list = sm.get_user_list()
    print(count, ' user in send list')
    for u in user_list:
        c = to_dict[u]
        news = get_date_new(str(day), c)
        for new in news:
            (title, date, url) = new
            json_data = {"touser":u, "college": get_c_name(c), "title": title, "date": date, "url":url}
        # 发送消息
        sm.send_message(json_data=json_data)
