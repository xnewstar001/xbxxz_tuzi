# -*- coding: utf-8 -*-
"""get_int1..4 / make_int1..4 黑盒格式探测（run/ 下 py27 运行）"""
import sys, os, base64, threading, struct

threading.Timer(90, lambda: os._exit(7)).start()
sys.path.insert(0, os.getcwd())

import local_auth
local_auth.install()
import game

SAMPLE = 'xbxxz_0FDVtiIBQWCyDfG0mifWRklm2n5ODahI0nx+pxOwuAFnCgP/DQV+EtnivUlcfVMN'
BODY = SAMPLE.split('_', 1)[-1]

def call(fn, *a):
    try:
        r = getattr(game, fn)(*a)
        print('%s(%r) -> %r' % (fn, a[0] if a else None, r))
        return r
    except Exception as e:
        print('%s(%r) !! %s: %s' % (fn, a[0] if a and a[0] is not None else None,
                                    type(e).__name__, str(e)[:100]))
        return None

print('== get_int1..4(样本) ==')
for i in (1, 2, 3, 4):
    call('get_int%d' % i, SAMPLE)
    call('get_int%d' % i, BODY)

print('== get_int1..4(数字串/简单串) ==')
for s in ('1', '12', '1234', 'ABCDEFGH', 'AAAAAAAAAAAAAAAA', base64.b64encode('\x01' * 12)):
    call('get_int1', s)

print('== make_int1..4(整数) ==')
for i in (0, 1, 255, 65536, 1753549047, 2109082018):
    call('make_int1', i)
call('make_int2', 1, 2)
call('make_int3', 1, 2, 3)
call('make_int4', 1, 2, 3, 4)

print('== 其他辅助函数 ==')
call('make_string1', 'test')
call('make_self_obj')
call('index_charge_value', 0)
call('calc_sign', 'test')

os._exit(0)
