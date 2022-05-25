import requests
from lxml import etree


class Judge(object):
    def __init__(self, userID: str, pwd: str):
        self.__userid = userID
        self.__pwd = pwd
        self.__version = '1.0'
        self.__rq = requests.session()
        self.__postData = {
            "eid": "722540",
            "summarize": "暂无",
            "content": [{
                "7": "100"
            }, {
                "8": "100"
            }, {
                "5": "100"
            }, {
                "6": "100"
            }, {
                "17": "100"
            }, {
                "10": "100"
            }, {
                "19": "100"
            }, {
                "15": "100"
            }, {
                "16": "100"
            }, {
                "14": "100"
            }, {
                "11": "100"
            }, {
                "13": "100"
            }, {
                "12": "100"
            }, {
                "18": "100"
            }, {
                "21": "100"
            }, {
                "20": "100"
            }, {
                "23": "100"
            }, {
                "32": "100"
            }, {
                "42": "100"
            }, {
                "43": "100"
            }, {
                "44": "100"
            }]
        }
        self.__msg = ''
        self.__findClass(self.__getAll())

    def getInfo(self):
        return self.__version

    def __login(self):
        loginURL = 'http://zxpj.nuc.edu.cn/userlogin'
        data = {
            'username': self.__userid,
            'userpassword': self.__pwd,
            'isstudent': 1,
            'kaptcha': 'a@a'
        }
        try:
            ret = self.__rq.post(url=loginURL, data=data).text
            if "显示验证码" not in ret and "查询无此账号" not in ret:
                # print('登陆成功')
                self.__msg = '登陆成功' + '\n'
            else:
                self.__msg = '登录错误,请检查学号或密码' + '\n'
        except:
            self.__msg = '登录错误' + '\n'
            exit(0)

    def __getAll(self) -> etree.HTML:
        self.__login()
        url = 'http://zxpj.nuc.edu.cn/evaluateRet/studentEva/?search=&ifCurrent=1&cyear=2020&csetype=0'
        rq = self.__rq.get(url=url)
        resp = etree.HTML(rq.text)
        return resp

    def __findClass(self, resp: etree.HTML):
        i = 1
        try:
            for i in range(1, 30):
                eid = resp.xpath('/html/body/div[2]/div/section/dl/dd/div/form/div/div/div[1]/ul[{}]/li/div['
                                 '3]/button[2]/@onclick'.format(str(i)))[0].strip('evaluatebutton(').strip(')')
                name = resp.xpath(
                    '/html/body/div[2]/div/section/dl/dd/div/form/div/div/div[1]/ul[{}]/li/div[1]/div[2]/text()'.format(
                        str(i)))[0].strip()
                teacher = resp.xpath(
                    '/html/body/div[2]/div/section/dl/dd/div/form/div/div/div[1]/ul[{}]/li/div[1]/div[3]/text()'.format(
                        str(i)))[0].strip()
                self.__msg = self.__msg + str(i) + name + ':' + teacher + '---' + str(eid)
                if self.__postEva(eid) == 200:
                    self.__msg = self.__msg + '该课程已评课成功!' + '\n'
                else:
                    self.__msg = self.__msg + '评课失败,请检查错误!' + '\n'
        except IndexError as e:
            self.__msg = self.__msg + '共有{}个未评课程!'.format(str(i - 1))

    def __postEva(self, eid: str) -> int:
        baseurl = 'http://zxpj.nuc.edu.cn/evaluateRet/addEvaluate/'
        self.__postData['eid'] = eid
        header = {
            'Referer': 'http://zxpj.nuc.edu.cn/evaluateRet/selectInfoByEid/' + eid,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        ret = self.__rq.post(url=baseurl, headers=header, json=self.__postData).status_code
        return ret

    def getMsg(self):
        return self.__msg


if __name__ == "__main__":
    print(Judge('xuehao','mima').getMsg())
