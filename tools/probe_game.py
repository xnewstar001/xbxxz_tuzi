# -*- coding: utf-8 -*-
"""
game.pyd 动态探针：在 py2.7 下 patch requests/socket 后调用 game.get_server_info，
记录全部网络行为。必须在 fuzhu_project/run/ 目录下用 tools/py27/python.exe 运行。
用法: python probe_game.py [stage]   stage1=导入+get_server_info(哑参数)
"""
import sys, os, json, time, types, threading, traceback
sys.path.insert(0, os.getcwd())   # 保证从 run/ 目录加载第三方包与应用模块

# 自杀看门狗，防止挂死
WATCHDOG = int(os.environ.get('PROBE_WATCHDOG', '75'))
threading.Timer(WATCHDOG, lambda: os._exit(7)).start()

LOG = {'requests': [], 'sockets': [], 'sleeps': [], 'calls': []}
FAKE = {}  # url 子串 -> (status, body)

def log(o):
    LOG.setdefault(o[0], []).append(o[1])
    tag, body = o
    try:
        print('[%s] %s' % (tag, json.dumps(body, ensure_ascii=False)[:600]))
    except Exception:
        print('[%s] %s' % (tag, repr(body)[:600]))

# ---------- patch requests ----------
import requests

class FakeResp(object):
    def __init__(self, status=200, body='', url=''):
        self.status_code = status
        self.text = body
        self.content = body.encode('utf-8') if isinstance(body, unicode) else body
        self.url = url
        self.headers = {'Content-Type': 'text/html'}
        self.encoding = 'utf-8'
    def json(self):
        return json.loads(self.content)
    def raise_for_status(self):
        pass
    def iter_content(self, n=1):
        yield self.content

def _wrap(fn, name):
    def w(*a, **kw):
        url = a[0] if a else kw.get('url', '')
        rec = {'api': name, 'url': url,
               'args': [repr(x)[:200] for x in a[1:]],
               'kw': dict((k, repr(v)[:400]) for k, v in kw.items())}
        log(('REQ', rec))
        for pat, (st, body) in FAKE.items():
            if pat in url:
                log(('FAKE', {'url': url, 'status': st, 'len': len(body)}))
                return FakeResp(st, body, url)
        log(('EMPTY', {'url': url}))
        return FakeResp(200, '', url)
    w.__name__ = name
    return w

requests.get = _wrap(requests.get, 'get')
requests.post = _wrap(requests.post, 'post')
requests.head = _wrap(requests.head, 'head')
requests.request = _wrap(requests.request, 'request')
_orig_session_request = requests.Session.request
def _sess_req(self, method, url, *a, **kw):
    rec = {'api': 'Session.request', 'method': method, 'url': url,
           'kw': dict((k, repr(v)[:400]) for k, v in kw.items())}
    log(('REQ', rec))
    return FakeResp(200, '', url)
requests.Session.request = _sess_req

# ---------- patch socket ----------
import socket
_orig_connect = socket.socket.connect
def _connect(self, addr):
    log(('SOCK', {'af': self.family, 'addr': repr(addr)}))
    raise IOError('probe-blocked: %r' % (addr,))
socket.socket.connect = _connect

# ---------- patch sleep（记录但保留短睡眠） ----------
_orig_sleep = time.sleep
def _sleep(s):
    log(('SLEEP', {'sec': s}))
    _orig_sleep(min(s, 0.05) if s > 1 else s)
time.sleep = _sleep

# ---------- 开始 ----------
print('=' * 60)
print('python', sys.version)
import game
print('game imported. dir(game) ->')
names = [n for n in dir(game) if not n.startswith('__')]
print(len(names), 'names')

stage = sys.argv[1] if len(sys.argv) > 1 else 'stage1'
if stage == 'stage1':
    args = dict(flag_login=1, accountId='0', access_token='', server_id=0,
                server_ip='127.0.0.1', server_port=8080,
                username='probe_user', password='probe_pass',
                phonenum='', verifynum='')
    LOG['calls'].append({'fn': 'get_server_info', 'args': args})
    print('CALLING game.get_server_info with', args)
    try:
        ret = game.get_server_info(**args)
        print('RET type=%s len=%s' % (type(ret), len(ret) if hasattr(ret, '__len__') else '-'))
        try:
            print('RET repr:', repr(ret)[:2000])
        except Exception as e:
            print('RET repr fail:', e)
    except Exception:
        print('EXCEPTION in get_server_info:')
        traceback.print_exc()

print('=' * 60)
with open('probe_log.json', 'w') as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print('log saved: probe_log.json')
os._exit(0)
