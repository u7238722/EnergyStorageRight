import math

import requests
from bs4 import BeautifulSoup
import json
from math import cos, sin, atan2, sqrt, pi, radians, degrees

# Get the solar information
def get_solar(geocode_list):
    '''if the front-end give the corodinates of a point,
       then we are able to get the solar info data,
       so the algorithm team will be able to use the data to build their algorithm,
       to give the result back to the front-end.
    '''
    # STEP 1: Build the url
    BASE_URL = 'https://api.globalsolaratlas.info/data/lta?loc='
    TOTAL_URL = BASE_URL + str(geocode_list[1]) + ',' + str(geocode_list[0])

    # STEP 2: request the content; Get the json data
    response = requests.get(TOTAL_URL)
    content = response.content
    soup = BeautifulSoup(content, 'lxml')
    soup_p = soup.p.string
    j = json.loads(soup_p)
    data_info = j['annual']['data']  # get the info

    return data_info

# Get the wind information
def get_wind(geocode):
    # STEP 1: The API for wind information
    url = 'https://globalwindatlas.info/api/gwa/custom/powerDensity'
    url2 = 'https://globalwindatlas.info/api/gwa/custom/windSpeed'



    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '221',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'globalwindatlas.info',
        'Origin': 'https://globalwindatlas.info',
        'Cookie': '_ga=GA1.2.1627731511.1598761481; _gid=GA1.2.1909282433.1598761481; nazkaCookie=accepted; _gat_gtag_UA_37540427_16=1',
        'Referer': 'https://globalwindatlas.info/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4238.2 Safari/537.36'
        }

    # STEP 2: Input points' positions
    longtitude=geocode[0]
    longtitude =  round(longtitude,6)   # Force conversion to 6 decimal places, the same below
    latitude=geocode[1]
    latitude = round(latitude,6)
    list1 = [[longtitude,latitude]]

    for i in range(1,5):
        longitude1 = longtitude+(0.01*i)
        longitude1 = round(longitude1,6)
        latitude1 = latitude+(0.01*i)
        latitude1 = round(latitude1,6)
        list1.append([longitude1,latitude1])

    data = {
        'coord':[list1],
        'height':100
        }

    data = json.dumps(data)
    result1=''     # Wind energy
    result2=''     # Wind speed

    result_dic={"power_density":"","wind speed":""}

    for j in range(5):
        try:
            html = requests.post(url,headers=headers,data=data,timeout=10)  # timeout is the timeout period, in seconds, the same below
            text = html.text

            result = json.loads(text)

            result1 = result['area_means'][0]['val']
            result_dic["power_density"]=result1

            html = requests.post(url2,headers=headers,data=data,timeout=10)
            text = html.text

            result = json.loads(text)

            result2 = result['area_means'][0]['val']
            result_dic["wind speed"]=result2

            break
        except:
            print('time out')
            pass
    return result_dic

