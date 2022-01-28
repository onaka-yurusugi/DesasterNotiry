# "キーワード"でツイートを取得 → ツイート内容をLINEに送信

import requests

from requests_oauthlib import OAuth1Session
import json
import time
import datetime

# 閾値設定-----------------------------------------------------------
threshold = 5

# LINE関連-----------------------------------------------------------------
# LINE Notify from Python
line_notify_token = '*'
line_notify_api = 'https://notify-api.line.me/api/notify'
#message = (tweet['text']) # 通知したい内容をここに入力　上のツイート検索から引用


# ツイッター関連-----------------------------------------------------------
# Twitter_serch
CK = '*'
CS = '*'
AT = '*'
AS = '*'


# タイムライン取得用のURL
url = "https://api.twitter.com/1.1/search/tweets.json"

# QAuth で GET
twitter = OAuth1Session(CK, CS, AT, AS)
params = {}
list = []
message = "検知：桜島噴火"

# ここからtwitter_search関数を作成
def twitter_search(word):
    res = twitter.get(url, params = {'q':word}) #'count':1
    res_text = json.loads(res.text)

    for tweet in res_text['statuses']:
        print('------')
        text = tweet['text']
        print (text)
        list.append(text)

    # if文とlen関数使って閾値を越えたら警告メッセージを発信
def Line_notify():
    if len(list) >= threshold:
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        line_notify = requests.post(line_notify_api, data=payload, headers=headers)

while True:
    # 5分前のメソッド
    now = datetime.datetime.now()
    now2 = datetime.timedelta(minutes=5)
    now_5m_ago = now - now2
    now_5m_ago = '{0:%Y-%m-%d_%H:%M:%S}'.format(now_5m_ago)
    print(now_5m_ago)

    # ツイッター検索
    twitter_search("桜島 噴火 since:" + now_5m_ago + "_JST" ) # キーワードで検索
    print(len(list))
    Line_notify()
    list.clear()
    time.sleep(300)



'''
-----------------------------------------------------------------------------
全体の動きとしては：
ツイート検索 高度な検索を使ってsince 現在時刻 - n 分
みたいな感じでn分前からの最新ツイート取得
取得したツイートをlistに追加してlen関数でツイート取得数を表示

ツイート取得数の閾値を仮に5以上と設定して、
閾値を超えた場合に信憑性があると判断しLINEに警告メッセージを発信

その際に付け加えたい行動もあればその都度実装

これらを5分毎に動かそう
'''
