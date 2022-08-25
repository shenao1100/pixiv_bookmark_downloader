#-*- coding:utf-8 -*-
#CREATER: ShenAo
#import qrcode
import re
import requests
import urllib
import urllib3

import base64
import threading

#功能性函数
#text content cookie
def get(url, header='', data='', proxy=''):

    requests.packages.urllib3.disable_warnings()
    try:
        response = requests.get(url=url, headers=header, data=data, proxies=proxy, verify=False, timeout=10)
        cookie_value = {}
        for key,value in response.cookies.items():  
            cookie_value[key] = value 
        return {'text':response.text, 'content': response.content, 'cookie': cookie_value, 'headers': response.headers}
    except:
        return {'text': False, 'content': False, 'cookie': False, 'headers': False}


def post(url, header='', data='', proxy=''):
    requests.packages.urllib3.disable_warnings()
    try:
        response = requests.post(url=url, headers=header, data=data, proxies=proxy, verify=False)
        cookie_value = {}
        for key,value in response.cookies.items():  
            cookie_value[key] = value 
        return {'text':response.text, 'content': response.content, 'cookie': cookie_value, 'headers': response.headers}
    except:
        return {'text': False, 'content': False, 'cookie': False, 'headers': False}

def put(url, header='', data='', proxy=''):
    requests.packages.urllib3.disable_warnings()
    try:
        response = requests.put(url=url, headers=header, data=data, proxies=proxy, verify=False)
        cookie_value = {}
        for key,value in response.cookies.items():  
            cookie_value[key] = value 
        return {'text':response.text, 'content': response.content, 'cookie': cookie_value, 'headers': response.headers}
    except:
        return {'text': False, 'content': False, 'cookie': False, 'headers': False}

def clean_file_name(filename:str):
    invalid_chars='[\\\/:*?"<>|]'
    replace_char='-'
    return re.sub(invalid_chars,replace_char,filename)


def getSubstr(input,start,end):
    #php中的setsubstr    获取在input中夹在start和end中间的文本
    find_num = input.find(start)
    result = input[find_num+len(start):]
    find_end_num = result.find(end)
    result = result[:find_end_num]
    return result

def strstr(input,fn):
    #php中的strstr      获取input中fn后的所有文本
    find_num = input.find(fn)
    result = input[find_num+len(fn):]
    return result

def strstr_front(input,fn):
    #获取input中fn前的所有文本
    find_num = input.find(fn)
    result = input[:find_num]
    return result

def read_file(path):
    with open(path) as fp:
        content = fp.read()
        try:
            return content
        except:
            write_file(path, content)
            return content

def write_file(filepath,insert):
    filepath = filepath.replace('/','\\')
    try:
        with open(filepath,'w',encoding='utf-8') as wf:
            wf.write(insert)
        return True
    except:
        return False

def urlencode(str) :
    reprStr = repr(str).replace(r'\x', '%')
    return reprStr[1:-1]

def byteOrBytes(size):
    if size == 1: return '字节'
    return '字节'

def size(size):
    times = 0
    size = int(size)
    while size > 1024:
        size /= 1024
        times += 1
    switch = {0: byteOrBytes(size),
            1 : 'KB',
            2 : 'MB',
            3 : 'GB',
            4 : 'TB',
            5 : 'EB',
            6 : 'ZB',
        }
    unit =  switch.get(times, '未知单位')
    fSize = '%.2f' % size
    if int(float(fSize)) == float(fSize):
        return str(int(float(fSize))) + unit
    return str(fSize) + unit

def get_back_path(input):
    if input != '/':
        temp_result = input[:(len(input) - len(input.split('/')[-1]) - 1)]
        if temp_result == '':
            temp_result = '/'
    else:
        temp_result = '/'
    temp_result = temp_result.replace('//','/')
    return temp_result


