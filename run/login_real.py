# -*- coding: utf-8 -*-
import sys, os, json, time, struct, socket, base64

# ============================================================
# token / 网关来源：与辅助本体同一份 run/config.ini
#   （[login] token= 或 token_{区号}=；gateway=ip:port）
# 也可把抓包到的新鲜渠道登录串直接填到下面 TOKEN。
import ConfigParser
_cp = ConfigParser.ConfigParser()
_cp.read('config.ini')

def _cfg(key, default=''):
    try:
        v = _cp.get('login', key).strip()
        return v if v not in ('', '0') else default
    except Exception:
        return default

TOKEN = _cfg('token') or _cfg('access_token')
GW_IP, GW_PORT = '193.112.212.244', 15409   # 兜底（lenovo 渠道前置登录服）
_gw = _cfg('gateway')
if _gw and ':' in _gw:
    GW_IP, GW_PORT = _gw.rsplit(':', 1)[0].strip(), int(_gw.rsplit(':', 1)[1])
# ============================================================
# 登录后保持在线秒数
RUN_SECONDS = 120
# ============================================================


# ---- 前置登录服协议函数 ------------------------------------

def make_0201():
    """
    0201 VerifyVerCmd:
      size(i32)=14  cmd(u8)=2  param(u8)=1  ts(i32)=0  reserve(i32)=0  version(i32)=1999
    size=14 = 不含 size 自身4字节的包体长度(1+1+4+4+4=14)，总包长=18字节
    """
    return struct.pack('<ibbiii', 14, 2, 1, 0, 0, 1999)

def make_0202(token):
    """
    0202 RequestLoginCmd:
      size(i32)  cmd(u8)=2  param(u8)=2  ts(i32)=0  toklen(i16)  token_bytes
    size = 1+1+4+2+len(tok)（不含 size 自身4字节），总包长 = 4+8+len(tok)
    """
    tok = token.encode('utf-8') if isinstance(token, type(u'')) else token
    inner_size = 1 + 1 + 4 + 2 + len(tok)   # 不含 size 自身
    return struct.pack('<ibbi', inner_size, 2, 2, 0) + struct.pack('<h', len(tok)) + tok

def read_exactly(sock, n):
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise IOError('connection closed after %d/%d bytes' % (len(buf), n))
        buf += chunk
    return buf

def gateway_exchange(token, gw_ip, gw_port, timeout=15):
    """
    连前置登录服，发 0201+0202，收 0204。
    返回 (game_ip_str, game_port_int, user_id_bytes_8, login_id_bytes_4)
    失败抛异常。
    """
    pkt0201 = make_0201()
    pkt0202 = make_0202(token)
    print('[gw] connecting %s:%d ...' % (gw_ip, gw_port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((gw_ip, gw_port))
    print('[gw] connected, sending 0201(%dB) + 0202(%dB)' % (len(pkt0201), len(pkt0202)))
    print('[gw] 0201 hex:', pkt0201.encode('hex'))
    print('[gw] 0202 hex prefix (32B):', (pkt0201 + pkt0202).encode('hex')[:64])
    s.sendall(pkt0201 + pkt0202)

    # 读包头 size(4)
    raw_size = read_exactly(s, 4)
    pkt_size = struct.unpack('<i', raw_size)[0]
    print('[gw] recv pkt_size=%d' % pkt_size)
    if pkt_size < 6 or pkt_size > 65536:
        raise ValueError('invalid pkt_size: %d' % pkt_size)

    # 读剩余字节
    rest = read_exactly(s, pkt_size - 4)
    s.close()

    cmd   = struct.unpack('B', rest[0:1])[0]
    param = struct.unpack('B', rest[1:2])[0]
    print('[gw] cmd=%d param=%d' % (cmd, param))
    if cmd != 2:
        raise ValueError('unexpected cmd=%d' % cmd)
    if param == 3:
        raise ValueError('gateway rejected (0203): token expired or invalid - please get a fresh token')
    if param != 4:
        raise ValueError('unexpected param=%d (expected 4=0204), server may have closed - check token validity' % param)

    # 0204 payload 从 rest[6:] 开始（rest = cmd(1)+param(1)+ts(4)+payload）
    # 服务器发送顺序（LocalB2Client.cs Receive）：
    #   userId(8B) + loginId(4B) + domain(65B) + port(2B) = 79 bytes
    payload = rest[6:]
    if len(payload) < 79:
        raise ValueError('0204 payload too short: %d bytes' % len(payload))

    user_id_bytes  = payload[0:8]
    login_id_bytes = payload[8:12]
    domain_bytes   = payload[12:77]
    port_bytes     = payload[77:79]

    user_id   = struct.unpack('<Q', user_id_bytes)[0]
    login_id  = struct.unpack('<I', login_id_bytes)[0]
    game_port = struct.unpack('<H', port_bytes)[0]
    game_ip   = domain_bytes.rstrip(b'\x00').decode('utf-8')

    print('[gw] userId=%d loginId=%d game=%s:%d' % (user_id, login_id, game_ip, game_port))
    return game_ip, game_port, user_id_bytes, login_id_bytes


# ---- 屏蔽作者服务器 HTTP 请求（已失效，避免启动卡顿）------

sys.path.insert(0, os.getcwd())

import requests as _real
class _FakeResp(object):
    status_code = 200; text = ''; content = b''; url = ''; headers = {}; encoding = 'utf-8'
    def json(self): return {}
    def raise_for_status(self): pass
_real.post = lambda *a, **k: _FakeResp()
_real.get  = lambda *a, **k: _FakeResp()

import game


# ---- 信号桩（打印 emit 事件）-------------------------------

class Sig(object):
    def emit(self, *a):
        try:
            print('[emit]', json.dumps(list(a), ensure_ascii=False)[:200])
        except Exception:
            print('[emit]', repr(a)[:200])


# ---- 主流程 ------------------------------------------------

def main():
    # 第一步：前置登录服换取游戏服地址 + userId/loginId
    game_ip, game_port, user_id_bytes, login_id_bytes = gateway_exchange(
        TOKEN, GW_IP, GW_PORT
    )

    # 第二步：构造 game.pyd 期望的参数（正确格式，见 docs/07 §2.2）
    #   0205 载荷 = [b64decode(tempid)][b64decode(userid)][补零]
    #   服务器解析 [0:4]=loginTempID [4:12]=dwUserID，其后 name/password 可全零
    b = {}
    b['serverip'] = str(game_ip)
    b['port']     = game_port
    b['tempid']   = base64.b64encode(login_id_bytes + user_id_bytes)   # 16字符，解码恰12字节
    b['userid']   = base64.b64encode('\x00' * 12)                      # name 槽，全零即可

    print('[main] game server: %s:%d' % (b['serverip'], b['port']))
    print('[main] userid(b64): %s' % b['userid'])

    # 第三步：调 game.pyd 登录游戏服
    obj = game.game(Sig(), '0')
    r = obj.login(b)
    print('[main] login ret:', repr(r)[:120])

    if r is True:
        print('=== LOGIN OK, keeping alive %ds ===' % RUN_SECONDS)
        time.sleep(RUN_SECONDS)
    else:
        print('=== login() returned non-True, check emit log above ===')

    print('done')
    os._exit(0)


if __name__ == '__main__':
    main()
