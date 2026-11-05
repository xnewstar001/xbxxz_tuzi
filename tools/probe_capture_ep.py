# -*- coding: utf-8 -*-
"""作者服务器端点全捕捉：URL + 请求体(密文+解密) + 应答，跑真实登录链 300s。
 run/ 下 py27 运行。"""
import sys, os, json, time, base64, threading, traceback

threading.Timer(330, lambda: os._exit(7)).start()
sys.path.insert(0, os.getcwd())

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

import local_auth as LA
LA.install()

OUT = open('endpoint_capture.log', 'w')
LOCK = threading.Lock()

def w(line):
    with LOCK:
        OUT.write(line + '\n')
        OUT.flush()
        print(line[:150])

from Crypto.Cipher import AES

def try_decrypt(body):
    """尝试用已知密钥解密请求体，返回 (标签, 明文)。"""
    if body is None:
        return 'empty', ''
    if not isinstance(body, str):
        try:
            body = str(body)
        except Exception:
            return 'type?', repr(body)[:100]
    # JSON 明文?
    s = body.strip()
    if s.startswith('{'):
        return 'plain-json', s[:400]
    # AES-128-ECB iguietjs988435#1
    try:
        if len(body) % 16 == 0 and len(body) > 0:
            c = AES.new('iguietjs988435#1', AES.MODE_ECB)
            p = c.decrypt(body)
            n = ord(p[-1])
            if 1 <= n <= 16 and p[-n:] == chr(n) * n:
                return 'aes-ecb-key1', p[:-n][:400]
    except Exception:
        pass
    return 'unknown(%d bytes)' % len(body), body[:64].encode('hex') if hasattr(body, 'encode') else body[:64]

_orig_ha = LA._handle_author
def capture_handler(url, args, kw):
    body = LA._extract_data(args, kw)
    tag, plain = try_decrypt(body)
    t0 = time.time()
    try:
        r = _orig_ha(url, args, kw)
        resp = r.text if r is not None else None
    except Exception as e:
        r = None
        resp = '<handler error %s>' % e
    w('[%s] %s\n  body(%s): %s\n  resp: %r\n' % (
        time.strftime('%H:%M:%S'), url, tag,
        (plain[:500] if isinstance(plain, str) else repr(plain)[:500]),
        (resp or '')[:200]))
    return r
LA._handle_author = capture_handler
w('capture armed')

import game
LA.patch_game(game)

class Sig(object):
    def emit(self, *ev):
        pass

a, b, d = game.get_server_info(1, '0', token, server_id, gw_ip, gw_port,
                               'probe_user', 'probe_pass', '', '')
print('login d =', repr(d))
if d != 'success':
    os._exit(1)
game_obj = game.game(Sig(), a)
ret = game_obj.login(b)
print('login ret:', repr(ret)[:50])
if ret is True:
    print('== 运行 300s 捕捉周期性端点 ==')
    time.sleep(300)
w('capture done')
os._exit(0)
