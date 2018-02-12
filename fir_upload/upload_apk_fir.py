# encoding=utf8
import requests
import time
import sys
import urllib3

urllib3.disable_warnings()


def get_upload_info():
    minlen = 8
    syslen = len(sys.argv)  # 获取输入参数
    # 检查输入参数
    if syslen < minlen:
        print('input params error')
        return
    else:
        appname = sys.argv[1]  # app name
        appversion = sys.argv[2]  # app version
        buildnum = sys.argv[3]  # build
        iconpath = sys.argv[4]  # 图标路径
        apkpath = sys.argv[5]  # apk路径
        bundleid = sys.argv[6]  # app package
        apitoken = sys.argv[7]  # fir api token
    url = 'http://api.fir.im/apps'
    type = 'android'
    bundle_id = bundleid
    params = {'type': type, 'bundle_id': bundle_id, 'api_token': apitoken}
    response_data = requests.post(url, data=params)
    resjson = response_data.json()
    print(resjson['cert']['icon'])  # icon字典
    print(resjson['cert']['binary'])  # 二进制文件上传字典

    upload_iocn(resjson['cert']['icon'], iconpath)
    upload_apk(resjson['cert']['binary'], appname, appversion, buildnum, apkpath)


def upload_iocn(icondict, iconpath):
    try:
        print("start upload icon")
        url = icondict['upload_url']
        key = icondict['key']
        token = icondict['token']
        paramdata = {'key': key, "token": token}
        iconfile = {'file': open(iconpath, 'rb')}
        # 上传icon
        res = requests.post(url, files=iconfile, data=paramdata, verify=False)
        print(res.text)
    except BaseException as e:
        print(e)
    finally:
        print('iocn upload finally')


def upload_apk(binarydict, appname, appversion, buildnum, apkpath):
    try:
        print("start upload apk")
        url = binarydict["upload_url"]
        key = binarydict["key"]
        token = binarydict["token"]
        changelog = str('time :' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        paramdata = {
            'key': key,
            'token': token,
            'x:name': appname,  # '必赢'
            'x:version': appversion,  # '1.0.0'
            'x:build': buildnum,  # 11
            'x:changelog': changelog  # 日志
        }
        apkfile = {'file': open(apkpath, 'rb')}
        res = requests.post(url, files=apkfile, data=paramdata, verify=False)
        print(res.text)
        print("upload success")
    except BaseException as e:
        print(str(e))
    finally:
        print('apk upload finally')


def test_print():
    minlen = 5
    syslen = len(sys.argv)  # 获取输入参数
    appname = sys.argv[1]  #
    appversion = sys.argv[2]
    iconpath = sys.argv[3]
    apkpath = sys.argv[4]
    print(apkpath)


if __name__ == '__main__':
    get_upload_info()
