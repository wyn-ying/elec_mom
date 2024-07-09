# -*- coding: utf-8 -*-
import os
import requests
import json
import time
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

APPKEY='xxx'       #获取Appkey请前往控制台：https://nls-portal.console.aliyun.com/applist
AK_ID='xxx'
AK_SECRET='xxx'
# 全流程 https://help.aliyun.com/zh/isi/developer-reference/restful-api
# VOICEID= 'zhida'
# speech_rate = 80
# volume = 70
# VOICEID = 'voice-001c648'  #妈妈的声音
VOICEID = 'voice-cd4964d'  #妈妈的声音2
speech_rate = 0
volume = 50
download_dir = '/volume1/music/eleven/'

def get_token():
    # https://help.aliyun.com/zh/isi/getting-started/obtain-an-access-token-in-the-console
    # 创建AcsClient实例
    client = AcsClient(AK_ID, AK_SECRET, 'cn-shanghai')

    # 创建request，并设置参数。
    request = CommonRequest()
    request.set_method('POST')
    request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request.set_version('2019-02-28')
    request.set_action_name('CreateToken')

    try :
       response = client.do_action_with_exception(request)
       print(response)

       jss = json.loads(response)
       if 'Token' in jss and 'Id' in jss['Token']:
          token = jss['Token']['Id']
          expireTime = jss['Token']['ExpireTime']
          print('token = ' + token)
          print('expireTime = ' + str(expireTime))
    except Exception as e:
       print(e)
    return token

def submit(token, text, voiceid=VOICEID):
    url = 'https://nls-gateway-cn-shanghai.aliyuncs.com/rest/v1/tts/async'
    d = {
        'payload': {
            'tts_request': {
                'voice': voiceid,
                'speech_rate': speech_rate,
                'volume': volume,
                'format': 'mp3',
                'text': text,
                'enable_subtitle': True,
            },
            'enable_notify': False,
        },
        'context': {
            'device_id': 'mydid',
        },
        'header': {
            'appkey': APPKEY,
            'token': token,
        }
    }
    resp = requests.post(url, json=d)
    print('submit response')
    print(resp.json())
    respdata = resp.json()
    if respdata['status'] != 200:
        return None
    taskid = respdata['data']['task_id']
    return taskid

def check_result(token, taskid):
    url = 'https://nls-gateway-cn-shanghai.aliyuncs.com/rest/v1/tts/async'
    d = {
        'appkey': APPKEY,
        'token': token,
        'task_id': taskid,
    }
    resp = requests.get(url, params=d)
    print('check_result response')
    print(resp.json())
    respdata = resp.json()
    if respdata['status'] != 200:
        return None
    if respdata['error_message'] != 'SUCCESS':
        return ''
    return respdata['data']['audio_address']

def download(url, title=None):
    resp = requests.get(url)
    print('get_data response')
    if resp.status_code == 200:
        title = 'test' if title is None else title
        fname = os.path.join(download_dir, title + '.mp3')
        print(f'downloading to {fname} ...')
        with open(fname, 'wb') as f:
            f.write(resp.content)
    print('finish download')

def run_once(text, title=None, token=None, test=False, voiceid=None):
    token = get_token() if token is None else token
    voiceid = VOICEID if voiceid is None else voiceid
    taskid = submit(token, text, voiceid)
    if taskid is None:
        return 
    url = ''
    while url == '':
        time.sleep(0.1)
        url = check_result(token, taskid)
    if url is None:
        return
    if (title is None or title == '') and test is False:
        title = [c for c in text.split('\n') if c != ''][0]
    download(url, title)

if __name__ == '__main__':
    TEXT="""
    三字经
    人之初，性本善。性相近，习相远。
    苟不教，性乃迁。教之道，贵以专。
    昔孟母，择邻处。子不学，断机杼。
    窦燕山，有义方。教五子，名俱扬。
    养不教，父之过。教不严，师之惰。
    子不学，非所宜。幼不学，老何为。
    玉不琢，不成器。人不学，不知义。
    """
    run_once(TEXT)
