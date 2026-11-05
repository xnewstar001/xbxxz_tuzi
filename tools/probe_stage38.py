# -*- coding: utf-8 -*-
"""
stage38: 端到端验证"脱离作者服务器"改造（在 fuzhu_project/run 目录用 py27 运行）

验证链路：
  game.get_server_info（真 pyd 函数）
    -> local_auth 钩子拦截（不发往 211.159.180.131）
    -> 本地解密请求 + 前置登录服 0201/0202/0204 交换
    -> 合成 {a,b,c,d} 响应 -> pyd 解析
  game_obj.login(b)（b 的地址改写为本地转发器）
    -> TCP 游戏服
  判定：登录后 S->C 是否有回包（此前 stage35/36/37 全是 0 回包的假会话，
        本探针的核心验收标准就是 S->C > 0）

token 来源：与辅助本体同一份 run/config.ini（[login] token/token_{区号} + gateway）。
"""
import sys, os, json, time, base64, threading, traceback
import socket as pysocket
import SocketServer

threading.Timer(240, lambda: os._exit(7)).start()
sys.path.insert(0, os.getcwd())

# ---- token / 网关来源：与辅助本体同一份 run/config.ini -----------------------
#   config.ini [login]: token= 或 token_{区号}=（渠道登录串）、gateway=（前置登录服 ip:port）
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
print('[cfg] server_id=%d gw=%s:%d token_len=%d' % (server_id, gw_ip, gw_port, len(token)))

# ---- 安装本地授权层（必须在 import game 之前）--------------------------------
import local_auth
local_auth.install()

# ---- 本地转发器（抓包）：127.0.0.1:25409 -> 真实游戏服 ------------------------
FWD_PORT = 25409
LOG = []
LOCK = threading.Lock()

def tee(tag, data):
    with LOCK:
        LOG.append((tag, len(data)))
        try:
            printable = ''.join(c if 32 <= ord(c) < 127 else '.' for c in data[:100])
        except Exception:
            printable = ''
        print('[%s] %dB %s | %s' % (tag, len(data), data.encode('hex')[:96], printable[:70]))

class Handler(SocketServer.BaseRequestHandler):
    def handle(self):
        print('[FWD] client in')
        upstream = pysocket.socket()
        upstream.connect((UPSTREAM[0], UPSTREAM[1]))
        print('[FWD] upstream ok %s:%d' % UPSTREAM)
        errs = []

        def pump(src, dst, tag):
            try:
                src.settimeout(90)
                while True:
                    data = src.recv(65535)
                    if not data:
                        break
                    tee(tag, data)
                    dst.sendall(data)
            except Exception as e:
                errs.append('%s: %s' % (tag, e))

        t1 = threading.Thread(target=pump, args=(self.request, upstream, 'C->S'))
        t2 = threading.Thread(target=pump, args=(upstream, self.request, 'S->C'))
        t1.start(); t2.start(); t1.join(); t2.join()
        try:
            upstream.close()
        except Exception:
            pass
        print('[FWD] closed, errs=%s' % errs[:4])

class Server(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

# ---- 第一步：裸网关交换，拿真实游戏服地址（转发器上游）------------------------
import local_auth as LA
game_ip, game_port, uid8, lid4 = LA.gateway_exchange(token, gw_ip, gw_port)
print('[gw1] game server: %s:%d  userId=%s loginId=%s' %
      (game_ip, game_port, uid8.encode('hex'), lid4.encode('hex')))
UPSTREAM = (game_ip, int(game_port))

fwd = Server(('127.0.0.1', FWD_PORT), Handler)
threading.Thread(target=fwd.serve_forever).start()
print('[fwd] listening 127.0.0.1:%d' % FWD_PORT)

# ---- 第二步：真 pyd 的 get_server_info 走本地授权层 ---------------------------
import game

print('== get_server_info (hooked) ==')
a, b, d = game.get_server_info(1, '0', token, server_id, gw_ip, gw_port,
                               'probe_user', 'probe_pass', '', '')
print('d =', repr(d), ' a =', repr(a)[:60])
print('b keys =', sorted(b.keys()))
assert d == 'success', '期望 success，实际 %r' % d
for k in ('serverip', 'port', 'tempid', 'userid'):
    assert k in b, 'b 缺字段 %s' % k
print('serverip=%s port=%s' % (b['serverip'], b['port']))
print('tempid=%s' % b['tempid'])
uid = base64.b64decode(b['userid'])
print('userid b64 -> %d bytes: %s' % (len(uid), uid.encode('hex')))

# ---- 第三步：改写地址走转发器，真登录 ----------------------------------------
b['serverip'] = '127.0.0.1'
b['port'] = FWD_PORT

class Sig(object):
    def emit(self, *ev):
        try:
            print('[emit]', json.dumps(list(ev), ensure_ascii=False)[:160])
        except Exception:
            print('[emit]', repr(ev)[:160])

print('== game_obj.login(b) ==')
sig = Sig()
game_obj = game.game(sig, '0')
ret = game_obj.login(b)
print('login ret:', repr(ret)[:80])

if ret is True:
    print('=== 保活 30s，统计 S->C 回包（>0 即真实会话）===')
    time.sleep(30)
    cs = sum(n for tag, n in LOG if tag == 'C->S')
    sc = sum(n for tag, n in LOG if tag == 'S->C')
    print('=== 验收结果: C->S=%dB  S->C=%dB  -> %s ===' %
          (cs, sc, 'LIVE SESSION（真实会话）' if sc > 0 else 'DEAD（服务器无回包，token 或登录载荷无效）'))
else:
    print('=== login 失败：', ret)
os._exit(0)
