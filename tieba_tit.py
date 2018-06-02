#! /usr/bin/env python
#coding=utf-8
# Author:nws0507

import urllib.request
import json
import hashlib

def md5(s):
    str0=s+'tiebaclient!!!'
    a = bytes(str0, 'utf-8')      
    #print(type(a),a)     
    md5 = hashlib.md5(a).hexdigest().upper()
    #print(md5)
    return md5
def post(url,payload):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    payload =payload
    data=urllib.parse.urlencode(payload)
    data=data.replace('&','')
    #print(data)
    payload['sign']=md5(data)
    #print(payload)
    payload=urllib.parse.urlencode(payload).encode(encoding='utf-8')
    req=urllib.request.Request(url,payload,headers) 
    reponse = urllib.request.urlopen(req).read()
    #print(reponse)
    return reponse

def uid(jsonData):
    res=[]
    value = json.loads(jsonData)
    if 'user_info' not in value:
        err=value['error_msg']
        return err
    subvalue = value['user_info'][0]
    res.append(subvalue['user_id'])
    s=','.join(res)
    #print(s)
    return s
    
def praserJsonFile(jsonData):
    global more
    try:
        value = json.loads(jsonData)
        more=value['has_more']
        #subvalue = value['forum_list']['non-gconforum']
        #print(len(value['forum_list']))
        subvalue=[]
        for j in value['forum_list'].keys():
            subvalue=subvalue+value['forum_list'][j]
        #print (subvalue)
        for i in range(len(subvalue)):
            #print(subvalue[i])
            subkeys=['name','level_id','level_name']
            res=[]
            for subkey in subkeys:
                #print (subkey,subvalue[i][subkey])
                res.append(subvalue[i][subkey])
                s=' '.join(res)
            print(s)
        #print(more)
    except Exception as e:
        #print(e,type(e))
        if str(e)=="'list' object has no attribute 'keys'":
            print('没有找到该用户关注的贴吧')

def finduid():
    global fr_uid
    name=str(input('输入用户名：'))      
    uid_url = 'http://c.tieba.baidu.com/c/r/friend/searchFriend'
    uid_payload={ '_client_version':'7.0.0.0','search_key':name}
    ret=post(uid_url,uid_payload)
    fr_uid=uid(ret.decode('unicode_escape'))
    print(fr_uid)
    
def findtit():
    tit_url='http://c.tieba.baidu.com/c/f/forum/like'
    page='1'
    while 1:
        tit_payload={'_client_version':'7.0.0.0','friend_uid':fr_uid,'is_guest':'1','page_no':page,'uid':'666'}
        tit=post(tit_url,tit_payload)
        praserJsonFile(tit.decode('unicode_escape'))
        if more=='0':
            break
        else:
            page=str(int(page)+1)
def main():
    finduid()
    if str(fr_uid)!='用户不存在':
        findtit()

if __name__ == '__main__':
    main()
