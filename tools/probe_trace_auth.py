# -*- coding: utf-8 -*-
"""授权数据流全追踪：包装 game 模块的 get_int*/make_int*/get_delta/get_str_time/
make_self_obj/check_charge_status/rsa_verify 等，跑真实登录链，打印每次调用。
（pyd 通过 game.<name> 模块全局查找调用这些函数，Python 层 setattr 即可拦截）
"""
import sys, os, json, time, base64, threading, traceback

threading.Timer(180, lambda: os._exit(7)).start()
sys.path.insert(0, os.getcwd())

import ConfigParser
token, gw_ip, gw_port, server_id = None, None, None, 0
try:
    cp = ConfigParser.ConfigParser()
    cp.read('config.ini')
    server_id = int(cp.get('login', 'server_id') or 0)
    for key in ('token_%d' % server_id if server_id > 0 else '', 'token'):
        if not key:
            continue
        try:
            v = cp.get('login', key).strip()
            if v and v != '0':
                token = v
                break
        except Exception:
            pass
    g = cp.get('login', 'gateway').strip()
    if g and ':' in g:
        _ip, _p = g.rsplit(':', 1)
        gw_ip, gw_port = _ip.strip(), int(_p)
except Exception as e:
    print('[cfg] %s' % e)
if not token or not gw_ip:
    print(u'缺少 token/gateway：请在 config.ini [login] 配置 token= 与 gateway=（见 docs/07 §6）')
    os._exit(1)
print('[cfg] server_id=%d gw=%s:%d token_len=%s' % (server_id, gw_ip, gw_port, len(token) if token else None))

import local_auth
local_auth.install()
import game
local_auth.patch_game(game)   # 与 xbxxz_helper.py 相同顺序：先 patch 再包装

# ---- 包装 ----
NAMES = ['get_int1', 'get_int2', 'get_int3', 'get_int4',
         'make_int1', 'make_int2', 'make_int3', 'make_int4',
         'get_delta', 'get_str_time', 'make_self_obj', 'make_string1',
         'check_charge_status', 'rsa_verify', 'calc_sign',
         'index_charge_value', 'gen_string_length', 'sign_tail_apple']
REAL = {}
def wrap(name, fn):
    def w(*a):
        try:
            r = fn(*a)
        except Exception as e:
            print('[%s] args=%s RAISED %s: %s' % (name, [repr(x)[:70] for x in a],
                                                  type(e).__name__, str(e)[:100]))
            raise
        print('[%s] args=%s -> %r' % (name, [repr(x)[:70] for x in a], r if not isinstance(r, (str,)) or len(repr(r)) < 120 else repr(r)[:120]))
        return r
    return w
for nm in NAMES:
    if hasattr(game, nm):
        REAL[nm] = getattr(game, nm)
        setattr(game, nm, wrap(nm, REAL[nm]))
print('[wrapped]', sorted(REAL.keys()))

# get_server_info 也包装记录返回
_real_gsi = game.get_server_info
def gsi(*a):
    r = _real_gsi(*a)
    print('[get_server_info] args=%s' % [repr(x)[:40] for x in a])
    print('[get_server_info] -> a=%r' % (r[0],))
    print('[get_server_info] -> b=%r' % (dict((k, v if k not in ('userid', 'tempid') else v) for k, v in r[1].items()),))
    print('[get_server_info] -> d=%r' % (r[2],))
    return r
game.get_server_info = gsi

class Sig(object):
    def emit(self, *ev):
        try:
            s = json.dumps(list(ev), ensure_ascii=False)
        except Exception:
            s = repr(ev)
        print('[emit]', s[:140])

print('== get_server_info ==')
a, b, d = game.get_server_info(1, '0', token, server_id, gw_ip, gw_port,
                               'probe_user', 'probe_pass', '', '')
print('d =', repr(d))
if d != 'success':
    os._exit(1)

print('== login ==')
game_obj = game.game(Sig(), a)
print('[game_obj attrs]', sorted(x for x in dir(game_obj) if not x.startswith('__'))[:80])
ret = game_obj.login(b)
print('login ret:', repr(ret)[:60])
if ret is True:
    print('== 会话 60s，观察周期性授权调用 ==')
    time.sleep(60)
print('done')
os._exit(0)
