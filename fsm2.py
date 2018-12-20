from transitions.extensions import GraphMachine
import random as rd
import re
import time
import numpy as np
from utils import send_text_message
from poetry import  sign, ind    

def valid_input(valids, err_format, parse='(.*)'):
    '''Return a decorator can insuring inputs is valid'''

    def decorator(func):
        '''decorate `func` as `f`'''

        def f(self, e):
            '''Returns what `func` returns if input is valid'''
            try: 
                e['text'] = re.match(parse, e['text']).group(1)
                assert e['text'] in valids
                return func(self, e)
            except:
                send_text_message( e['id'], 
                                 err_format%('/'.join(valids) ) )

        return f
        
    return decorator


class TocMachine(GraphMachine):
    
    level = ['還好', '重要', '很重要']
    god_say = ['應該不是', '母湯喔', '喔!發誓不是']
    p = 0.5
    # prob = [ 2*p*(1-p), (1-p)**2, p**2 ]
    prob = [1, 0, 0]

    def __init__(self, **machine_configs):
        self.machine = GraphMachine( model=self, **machine_configs)
        # self._count = 0
        self.cooldown = -np.inf


    def 抽籤(self, e):
        n = rd.randint(1, 60)
        send_text_message(e['id'], '第%d籤'%n)
        self.poetry = sign(n, e['text'])


    def 擲笅(self, e):
        res = np.random.choice(['聖笅', '笑笅', '陰笅'],
                size = 1, p = self.prob )[0]
        send_text_message(e['id'], res)
        return res
    
    
    @valid_input(['求籤', '問事'], "選擇 (%s)")
    def is_going_to_ask(self, e):
        self.mode = e['text']
        return True
    
    
    @valid_input(['丟'], "請輸入'%s'")
    def is_god_ready(self, e):
        if time.time() > self.cooldown:
            if self.擲笅(e) == '聖笅':
                return True
            self.cooldown = time.time() + 5
        time_remain = self.cooldown - time.time()
        send_text_message(e['id'], "神明出門, 請%d秒後再試..."%time_remain)
     
    
    @valid_input(level, "請輸入 要問的事#(%s)" , '.*#(.*)')
    def ready_to_throw(self, e):
        self._count = self.level.index(e['text']) + 1
        return True


    @valid_input(ind, "可問#(%s)" , '.*#(.*)')
    def poe_to_throw(self, e):
        if self.擲笅(e) == '聖笅':
            self.抽籤(e)
            self._count = 2
            self.thing = e['text']
            return True
        send_text_message(e['id'], '不給抽')
    
    
    @valid_input(['丟', '一鍵擲笅'], '輸入(%s)')
    def is_going_to_fail(self, e):
        n = self._count if e['text'] == '一鍵擲笅' else 1
        for _ in range(n):
            if self.擲笅(e) != '聖笅':
                return True
            self._count -= 1
        if self._count == 0:
            self.say_yes(e)
    

    @valid_input(['再來'], '%s嗎?')
    def try_again(self, e):
        return True
    
    
    def on_enter_ask(self, e):
        send_text_message(e['id'], '擲一笅看神明在不在(輸入"丟")')
        
    def on_enter_ready(self, e):
        if self.mode == '問事':
            send_text_message(e['id'], '輸入: 是不是...#(還好/重要/很重要)')
        else:
            self.get_poe(e)
    
    def on_enter_poe(self, e):
        send_text_message(e['id'], '六十甲子籤 問什麼?')
        
    def on_enter_throw(self, e):
        send_text_message(e['id'], '選擇 (丟/一鍵擲笅)')
    
    def on_enter_fail(self, e):
        if self.mode == '問事':
            send_text_message(e['id'], 'QQ喔, 祂說:' + self.god_say[self._count] )
        else:
            send_text_message(e['id'], '不是這支喔' )
    
    def on_enter_yes(self, e):
        if self.mode == '問事':
            send_text_message(e['id'], 'OK的 祂說:是的')
        else:
            send_text_message(e['id'],
                     self.poetry['詩'] + '\n' + \
                     self.poetry[self.thing] )
        
# create fsm

def delta(*args):
    keyword = ('trigger', 'source', 'dest', 'conditions', 
                'unless', 'before', 'after', 'prepare')
    return dict( zip(keyword, args) )

machine = TocMachine(
    states=[ 'start', 'ask', 'ready', 'throw', 'fail', 'yes', 'poe' ],
    transitions=[
        delta( 'advance', 'start',    'ask',   'is_going_to_ask' ),
        delta( 'advance',   'ask',  'ready',      'is_god_ready' ),
        delta( 'advance', 'ready',  'throw',    'ready_to_throw' ),
        delta( 'get_poe', 'ready',    'poe',                     ),
        delta( 'advance',   'poe',  'throw',      'poe_to_throw' ),
        delta( 'advance', 'throw',   'fail',  'is_going_to_fail' ),
        delta( 'say_yes', 'throw',    'yes',                     ),
        delta( 'advance', ['fail', 
                            'yes'], 'start',         'try_again' ),
                ],
    initial='start',
    auto_transitions=False,
    show_conditions=True,
)