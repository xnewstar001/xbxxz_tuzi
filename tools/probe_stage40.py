# -*- coding: utf-8 -*-
"""
stage40: 长保活验证 —— 检查二进制 tempid（无 'end' 字段）是否触发授权看门狗掉线。
真实直连（无转发器），与 GUI 实际路径完全一致。在 run/ 下用 py27 运行。
"""
import sys, os, json, time, threading, traceback

sys.path.insert(0, os.getcwd())

KEEP_SECONDS = 300

import ConfigParser
token, gw_ip, gw_port, server_id = None, None, None, 0
cp = ConfigParser.ConfigParser()
cp.read('config.ini')
try:
    server_id = int(cp.get('login', 'server_id') or 0)
except Exception:
    server_id = 0
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
try:
    g = cp.get('login', 'gateway').strip()
    if g and ':' in g:
        _ip, _p = g.rsplit(':', 1)
        gw_ip, gw_port = _ip.strip(), int(_p)
except Exception:
    pass
if not token or not gw_ip:
    print('[cfg] 缺少 token/gateway：请在 config.ini [login] 配置 token= 与 gateway=（见 docs/07 §6）')
    os._exit(1)
print('[cfg] server_id=%d gw=%s:%d token_len=%s' % (server_id, gw_ip, gw_port, len(token) if token else None))

import local_auth
local_auth.install()
import game

class Sig(object):
    def emit(self, *ev):
        try:
            s = json.dumps(list(ev), ensure_ascii=False)
        except Exception:
            s = repr(ev)
        # 掉线/失败类消息醒目打印
        if any(k in s for k in (u'掉线', u'失败', u'断开', u'错误')):
            print('!!! [emit]', s[:160])
        elif len(ev) > 1 and ev[1] in (1, 3, 15, 90):
            print('[emit]', s[:120])

print('== get_server_info (hooked) ==')
a, b, d = game.get_server_info(1, '0', token, server_id, gw_ip, gw_port,
                               'probe_user', 'probe_pass', '', '')
print('d =', repr(d), ' serverip=%s port=%s' % (b.get('serverip'), b.get('port')))
assert d == 'success', 'get_server_info 失败: %r' % d

print('== login (直连真实游戏服) ==')
game_obj = game.game(Sig(), '0')
ret = game_obj.login(b)
print('login ret:', repr(ret)[:80])
if ret is not True:
    print('=== LOGIN FAIL ===')
    os._exit(1)

print('=== 保活 %ds，观察是否被看门狗掉线 ===' % KEEP_SECONDS)
deadline = time.time() + KEEP_SECONDS
n = 0
while time.time() < deadline:
    time.sleep(10)
    n += 1
    print('[t+%ds] alive' % (n * 10))
print('=== 结果: %d 秒会话存活，无看门狗掉线 ===' % KEEP_SECONDS)
os._exit(0)
