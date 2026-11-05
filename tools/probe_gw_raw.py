# -*- coding: utf-8 -*-
"""raw gateway exchange: print FULL 0204 payload (len + hex) — run from run/ with py27"""
import sys, os, struct, socket
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
    print('缺少 token/gateway：请在 config.ini [login] 配置 token= 与 gateway=（见 docs/07 §6）')
    sys.exit(1)
print('gw=%s:%d server_id=%s token_len=%d' % (gw_ip, gw_port, server_id, len(token)))

def recv_exact(s, n):
    buf = ''
    while len(buf) < n:
        c = s.recv(n - len(buf))
        if not c:
            raise IOError('closed at %d/%d' % (len(buf), n))
        buf += c
    return buf

pkt0201 = struct.pack('<ibbiii', 14, 2, 1, 0, 0, 1999)
tok = token.encode('utf-8') if isinstance(token, unicode) else token
pkt0202 = struct.pack('<ibbi', 1 + 1 + 4 + 2 + len(tok), 2, 2, 0) + struct.pack('<h', len(tok)) + tok
s = socket.create_connection((gw_ip, gw_port), 15)
s.settimeout(15)
s.sendall(pkt0201 + pkt0202)
size = struct.unpack('<i', recv_exact(s, 4))[0]
print('resp pkt size=%d' % size)
rest = recv_exact(s, size - 4)
print('rest len=%d cmd=%d param=%d' % (len(rest), ord(rest[0]), ord(rest[1])))
payload = rest[6:]
print('PAYLOAD len=%d' % len(payload))
print(payload.encode('hex'))
s.close()
