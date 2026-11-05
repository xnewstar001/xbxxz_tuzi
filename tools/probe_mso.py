# -*- coding: utf-8 -*-
"""make_self_obj / get_delta / get_str_time 输入格式探测"""
import sys, os, base64, threading

threading.Timer(60, lambda: os._exit(7)).start()
sys.path.insert(0, os.getcwd())

import local_auth
local_auth.install()
import game

SAMPLE = 'xbxxz_0FDVtiIBQWCyDfG0mifWRklm2n5ODahI0nx+pxOwuAFnCgP/DQV+EtnivUlcfVMN'
BODY = SAMPLE.split('_', 1)[-1]

def call(fn, *a):
    try:
        r = getattr(game, fn)(*a)
        print('%s(%r) -> %r' % (fn, a[0] if len(a) == 1 else a, r))
        return r
    except Exception as e:
        print('%s(%r) !! %s: %s' % (fn, a[0] if len(a) == 1 else a, type(e).__name__, str(e)[:110]))
        return None

print('== make_self_obj 输入变体 ==')
call('make_self_obj', SAMPLE)
call('make_self_obj', BODY)
call('make_self_obj', base64.b64decode(BODY.encode('ascii')))
call('make_self_obj', 'xbxxz_' + 'A' * 64)
call('make_self_obj', '')
call('make_self_obj', 'test')

print('== get_delta / get_str_time 语义 ==')
import time as _t
now = _t.time()
call('get_delta', now + 86400 * 10, now)          # 未来10天?
call('get_delta', now, now + 86400 * 10)
call('get_delta', now + 3600, now)
call('get_str_time', now + 86400 * 10)
call('get_str_time', now)

os._exit(0)
