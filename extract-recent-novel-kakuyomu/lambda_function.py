import os
import re
import json
import time
import base64
import requests
import logging
from urllib.request import urlopen

from datetime import datetime
from bs4 import BeautifulSoup
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key


from connections import build_client_dynamo


PKEY = os.getenv("PKEY")
SKEY = os.getenv("SKEY")
TABLE_NAME = os.getenv("TABLE_NAME")


def get_info(pkey, skey):
    table = build_client_dynamo(table_name=TABLE_NAME)
    info = table.query(
        KeyConditionExpression = Key("pkey").eq(pkey) & Key("skey").eq(skey)
    )
    return info['Items'][0]


def get_html(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.content
    else:
        return None

def jst_str2ts_epoch_milli(jst, format="%Y-%m-%d %H:%M:%S"):
    dt = datetime.strptime(jst + "+0900", format + "%z")
    ts = dt.timestamp() * 1000
    return ts
    

def extract_recent_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    novels = soup.findAll('a', class_='widget-workCard-titleLabel bookWalker-work-title')
    links = [n.get('href') for n in novels]
    return links
    
    
def remove_duplicated_link(links, lastkey, default=False):
    idx = links.index(lastkey) if lastkey in links else default
    return links[:idx]
    
    
def lambda_handler(event, context):
    info = get_info(PKEY, SKEY)
    url = info['url']
    lastkey = info['lastkey']
    html = get_html(url).decode('utf-8')
    links = extract_recent_link(html)
    links = remove_duplicated_link(links, lastkey, len(links))
    if len(links) > 0:
        lastkey = links[0]
    return {
        'statusCode': 200,
        'pkey': info['pkey'],
        'skey': info['skey'],
        'lastkey': lastkey,
        'links': links
    }
