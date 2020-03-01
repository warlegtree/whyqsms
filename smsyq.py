#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
client = AcsClient('xxxxxx', 'xxxxxx', 'cn-hangzhou')

def get_ncp_raw_data():
    qq_url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    qq_req = requests.get(qq_url, headers)
    qq_res = json.loads(qq_req.text)
    ncp_raw_data = json.loads(qq_res['data'])
    return ncp_raw_data

def get_total_ncp_data():
    input_data  = get_ncp_raw_data()
    total_ncp_data = input_data['chinaTotal']
    return total_ncp_data

def get_ncp_updatetime():
    input_data  = get_ncp_raw_data()
    ncp_updatetime = input_data['lastUpdateTime']
    return ncp_updatetime

def get_wh_ncp_data():
    input_data = get_ncp_raw_data()
    pc_ncp_data = input_data['areaTree'][0]['children']
    for i in pc_ncp_data:
        if i['name'] == '湖北':
            hb_data = (i['children'])
            for j in hb_data:
                if j['name'] == '武汉':
                    total_wh = j
    return total_wh

def phone_number():
    phone_list = []
    with open('/home/phone/phone.txt', 'r') as f:
        for i in f:
            i = i.rstrip("\n")
            phone_list.append(i)
    return phone_list



if __name__ == '__main__':
    total_data = get_total_ncp_data()
    time = get_ncp_updatetime()
    confirm = total_data['confirm']
    suspect = total_data['suspect']
    heal = total_data['heal']
    dead = total_data['dead']
    phone_json = phone_number()
    print (time,confirm,suspect,heal,dead)

    wh = get_wh_ncp_data()
    for xq in wh:
        wh_confirm = wh['total']['confirm']
        wh_suspect = wh['total']['suspect']
        wh_heal = wh['total']['heal']
        wh_dead = wh['total']['dead']
        wh_add = wh['today']['confirm']
    print(time, wh_confirm, wh_suspect, wh_heal, wh_dead, wh_add)

    #sms data
    def gen_sms_data():
        repeat_times = len(phone_json)
        signname = "来至bus801的问候"
        signname_data = []
        while repeat_times > 0:
            signname_data.append(signname)
            repeat_times -= 1
        return signname_data

    #template_date
    def gen_template_data():
        repeat_times = len(phone_json)
        template_data = []
        template_content = {"time": time, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead, "wh_confirm": wh_confirm, "wh_suspect": wh_suspect, "wh_heal": wh_heal, "wh_dead": wh_dead, "add_confirm": wh_add}
        while repeat_times > 0:
            template_data.append(template_content)
            repeat_times -= 1
        return template_data



    #gen json
    signname_json = gen_sms_data()
    template_json = gen_template_data()

    #print(str(phone_json))
    #print(str(signname_json))
    #print(str(template_json))


    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendBatchSms')

    request.add_query_param('RegionId', "cn-hangzhou")

    request.add_query_param('PhoneNumberJson', str(phone_json))

    request.add_query_param('SignNameJson', str(signname_json))
    request.add_query_param('TemplateCode', "SMS_183241972")
    request.add_query_param('TemplateParamJson', str(template_json))

    response = client.do_action(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))
