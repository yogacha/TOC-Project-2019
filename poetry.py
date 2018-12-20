import re
import requests

url = 'https://qiangua.temple01.com/qianshi.php?t=fs60&s='

ind = ['凡事', '作事', '家事', '家運', '婚姻', '求兒', '六甲', '求財', '功名', '歲君', '治病', '出外',
       '經商', '來人', '行舟', '移居', '失物', '求雨', '官事', '六畜', '耕作', '築室', '墳墓', '討海',
       '作塭', '魚苗', '月令', '尋人', '遠信']

def sign(i, ask):
    result = requests.get( url + str(i) )
    result.encoding = 'utf-8'
    t = result.text
    
    start = t.index('fs_poetry_w_text')
    end = t.index('/div>', start)
    poetry = '\n'.join( re.findall('>([^><]*)<', t[start:end]) )
    
    start = t.index('籤解', end)
    end = t.index('/div>', start)
    pairs = re.findall('[>\r\n　]([^>\r\n　]*)　([^<]*)<', t[start:end] )

    return poetry, dict(pairs)[ask]
