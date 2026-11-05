# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import base64
import socket
import struct
import traceback

try:
    import configparser
except ImportError:                       # 兜底：原生 py2.7 的模块名
    import ConfigParser as configparser

import requests

# ---- 逆向确认的协议常量（与 docs/03、docs/06 一致） -------------------------
AUTHOR_HOSTS = ('211.159.180.131',)       # 作者服务器（已失效）
LOGIN_MARK = 'servers_login800.php'       # 登录端点
REQ_AES_KEY = 'iguietjs988435#1'          # 请求体 AES-128-ECB 密钥
SESSION_POSTFIX = 'uiejgkl!'              # key2 = 盐(8B) + 该后缀
SALT = 'AAAAAAAA'                         # 会话盐（逆向确认：任意值，无校验）

CONFIG_FILE = 'config.ini'
LOG_FILE = os.path.join('log', 'local_auth.log')

_installed = False
_real_post = None
_real_get = None


class GatewayError(Exception):
    """前置登录服交换失败（含 0203 拒绝）。"""


# ---- 日志（永不抛异常） ----------------------------------------------------

def _log(msg):
    try:
        d = os.path.dirname(LOG_FILE)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        line = '[%s] %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)
        f = open(LOG_FILE, 'a')
        try:
            f.write(line)
        finally:
            f.close()
    except Exception:
        pass


def _mask_token(token):
    """日志里屏蔽 sign/access_token 的值，只留结构特征。"""
    try:
        parts = []
        for kv in token.split('&'):
            if '=' in kv:
                k, v = kv.split('=', 1)
                parts.append('%s=%s' % (k, (v[:6] + '...') if len(v) > 10 else v))
            else:
                parts.append(kv)
        return '&'.join(parts)
    except Exception:
        return '<unprintable>'


# ---- 配置 ------------------------------------------------------------------

def _load_cfg():
    cfg = configparser.ConfigParser()
    try:
        cfg.read(CONFIG_FILE)
    except Exception:
        pass
    return cfg


def _cfg_get(cfg, key, default=''):
    try:
        v = cfg.get('login', key)
        if v is None:
            return default
        v = v.strip()
        return v if v not in ('', '0') else default
    except Exception:
        return default


def resolve_token(creds):
    """token 优先级：config token_{区号} > config token > 请求里的 access_token。"""
    cfg = _load_cfg()
    sid = ''
    try:
        sid = str(creds.get('server_id', '') or '').strip()
    except Exception:
        sid = ''
    if sid:
        v = _cfg_get(cfg, 'token_' + sid)
        if v:
            return v
    v = _cfg_get(cfg, 'token')
    if v:
        return v
    at = creds.get('access_token') or ''
    if isinstance(at, unicode):
        at = at.encode('utf-8')
    at = (at or '').strip()
    if len(at) > 20:                      # 完整渠道串必然很长，'0'/空串不算
        return at
    return ''


def resolve_gateway(creds):
    """网关 = config gateway 覆盖 > 请求里的 server_ip:server_port（UI 选中区条目）。"""
    cfg = _load_cfg()
    g = _cfg_get(cfg, 'gateway')
    if g and ':' in g:
        ip, _, p = g.rpartition(':')
        try:
            return ip.strip(), int(p)
        except Exception:
            pass
    ip = creds.get('server_ip') or ''
    port = creds.get('server_port') or 0
    try:
        port = int(port)
    except Exception:
        port = 0
    if not ip or not port:
        raise GatewayError(u'未指定前置登录服地址：请在 config.ini [login] 配置 gateway=ip:port')
    return ip, port


# ---- AES / 应答合成 ---------------------------------------------------------

def _auth_days():
    """本地授权天数（config [login] auth_days，默认 3650）。"""
    cfg = _load_cfg()
    v = _cfg_get(cfg, 'auth_days')
    try:
        n = int(v)
        if n > 0:
            return n
    except Exception:
        pass
    return 3650


def patch_game(game_mod):
    """import game 之后调用：覆写 game.make_self_obj。

    make_self_obj(chargeId) 是作者服务器的授权状态解析器：解析 a 字段（xbxxz_<加密blob>）
    返回 (剩余天, 时, 分)，登录时显示剩余时长，且作为功能闸的到期状态（
    "辅助到期，无法继续本功能！"）。本地模式下 a 由 build_login_response 合成为
    'xbxxz_local:<天数>'，这里解析它返回对应元组；其余输入走原函数兜底。
    pyd 通过模块全局查找调用该函数（动态追踪 probe_trace_auth 证实），覆写必然生效。
    """
    orig = getattr(game_mod, 'make_self_obj', None)
    marker = 'xbxxz_local:'

    def make_self_obj_local(charge_id, *args):
        try:
            s = charge_id if isinstance(charge_id, str) else str(charge_id)
            if s.startswith(marker):
                days = int(s[len(marker):].split('|', 1)[0])
                return (days, 0, 0)
        except Exception:
            pass
        if orig is not None:
            return orig(charge_id, *args)
        return (0, 0, 0)

    game_mod.make_self_obj = make_self_obj_local
    _log('patched game.make_self_obj -> local auth state')

    # ---- game.game 包装：灵根等角色属性默认值 ----
    # jinlinggen 等五灵根由 pyd 在处理服务器角色属性数据时按名字 setattr（动态时序），
    # 而 GameThread 在 login 返回后立即 start_work，数据未到时读取会 AttributeError
    # （原版同样存在该竞态）。构造时注入 0 值搭桥，服务器数据到达后被 pyd 覆盖自愈。
    orig_game = getattr(game_mod, 'game', None)
    default_attrs = ('jinlinggen', 'mulinggen', 'shuilinggen', 'tulinggen', 'huolinggen')
    if orig_game is not None and not getattr(orig_game, '_local_auth_patched', False):
        def game_with_defaults(*args, **kw):
            obj = orig_game(*args, **kw)
            for name in default_attrs:
                try:
                    if not hasattr(obj, name):
                        setattr(obj, name, 0)
                except Exception:
                    pass
            return obj
        game_with_defaults._local_auth_patched = True
        game_mod.game = game_with_defaults
        _log('patched game.game -> inject default linggen attrs %s' % (default_attrs,))


def _pkcs7_pad(s):
    n = 16 - len(s) % 16
    return s + chr(n) * n


def decrypt_request(body):
    """解出 get_server_info 请求 JSON（AES-128-ECB + PKCS7）。"""
    from Crypto.Cipher import AES
    if isinstance(body, dict):
        return body
    if isinstance(body, unicode):
        body = body.encode('utf-8')
    if not body:
        raise GatewayError(u'请求体为空')
    if len(body) % 16 != 0:
        raise GatewayError(u'请求体长度非 16 倍数（%d）' % len(body))
    cipher = AES.new(REQ_AES_KEY, AES.MODE_ECB)
    plain = cipher.decrypt(body)
    n = ord(plain[-1])
    if n < 1 or n > 16:
        raise GatewayError(u'请求体 PKCS7 校验失败（尾字节 %d）' % n)
    plain = plain[:-n]
    return json.loads(plain)


def encrypt_inner(inner_text, salt=SALT):
    """内层JSON -> base64(AES-ECB(salt+uiejgkl!))，即响应的 b 字段。"""
    from Crypto.Cipher import AES
    cipher = AES.new(salt + SESSION_POSTFIX, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(_pkcs7_pad(inner_text)))


def build_login_response(creds, game_ip, game_port, uid8, lid4):
    """按原协议组装 {"a","b","c","d"}。

    关键（stage38/39 实证 + C# 参考 stPasswdLogonMessage_XBXXZ 对齐）：
    pyd 的 0205 登录包载荷 = [b64decode(tempid)][b64decode(userid)][补零至76字节]，
    服务器解析 [0:4]=loginTempID、[4:12]=dwUserID、其后为 name(48)/password(16)（可全零）。
    因此 tempid 必须 = base64(loginTempID_4B + dwUserID_8B)，userid 进 name 槽（全零即可）。
    注意：docs/06 早期"tempid=JSON{'end'}"的结论只对授权闸成立（json.loads 恰好能解析），
    对发包格式是错的——JSON 串被当 b64 解出的垃圾字节占住了 lid/uid 位置，导致服务器静默丢弃。
    """
    inner = json.dumps({
        'serverip': str(game_ip),
        'port': int(game_port),
        'tempid': base64.b64encode(lid4 + uid8),
        'userid': base64.b64encode('\x00' * 12),
        # 原作者服务器应答含渠道专用字段；小米渠道(flag_login==7)的 GameThread 会读
        # b['xiaomi_chonglian']，缺失会 KeyError 进兜底 except，故补 0
        'xiaomi_chonglian': 0,
    })
    # a = 授权状态载体：原版是 'xbxxz_<加密blob>'（make_self_obj 解析出剩余时长），
    # 本地版带天数标记，由 patch_game 覆写的 make_self_obj 消费。
    resp = {
        'a': 'xbxxz_local:%d' % _auth_days(),
        'b': encrypt_inner(inner, SALT),
        'c': SALT,
        'd': 'success',
    }
    return json.dumps(resp)


def local_error(msg):
    """d='local_error'，GameThread.run 的对应分支会把 a 显示到日志面板。"""
    _log('local_error: %s' % msg)
    return LocalResp(json.dumps({'a': msg, 'b': '', 'c': SALT, 'd': 'local_error'}))


# ---- 前置登录服（网关）0201/0202/0204 ----------------------------------------

def _recv_exact(sock, n):
    buf = ''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise GatewayError(u'网关连接中断（已收 %d/%d 字节）' % (len(buf), n))
        buf += chunk
    return buf


def gateway_exchange(token, gw_ip, gw_port, timeout=15):
    """连前置登录服换登录凭据。返回 (game_ip, game_port, userId_8B, loginId_4B)。

    0201 = size(i32)+cmd(2)+param(1)+ts(4)+reserve(4)+version(1999)
    0202 = size(i32)+cmd(2)+param(2)+ts(4)+toklen(i16)+token
    0204 = userId(8)+loginId(4)+domain(65)+port(2)   （0203 = 网关拒绝）
    """
    if isinstance(token, unicode):
        token = token.encode('utf-8')
    pkt0201 = struct.pack('<ibbiii', 14, 2, 1, 0, 0, 1999)
    inner_size = 1 + 1 + 4 + 2 + len(token)
    pkt0202 = struct.pack('<ibbi', inner_size, 2, 2, 0) + struct.pack('<h', len(token)) + token

    _log('gateway connect %s:%d (token len=%d)' % (gw_ip, gw_port, len(token)))
    sock = socket.create_connection((gw_ip, gw_port), timeout)
    try:
        sock.settimeout(timeout)
        sock.sendall(pkt0201 + pkt0202)
        size = struct.unpack('<i', _recv_exact(sock, 4))[0]
        if size < 6 or size > 65536:
            raise GatewayError(u'网关应答长度异常: %d' % size)
        rest = _recv_exact(sock, size - 4)
    finally:
        try:
            sock.close()
        except Exception:
            pass

    cmd = ord(rest[0])
    param = ord(rest[1])
    if cmd != 2:
        raise GatewayError(u'网关应答 cmd=%d（期望 2）' % cmd)
    if param == 3:
        raise GatewayError(u'网关拒绝(0203)：token 过期或无效，请重新抓取渠道登录串')
    if param != 4:
        raise GatewayError(u'网关应答 param=%d（期望 4=0204）' % param)
    payload = rest[6:]
    if len(payload) < 79:
        raise GatewayError(u'0204 载荷过短: %d' % len(payload))
    uid8 = payload[0:8]
    lid4 = payload[8:12]
    game_ip = payload[12:77].rstrip('\x00')
    game_port = struct.unpack('<H', payload[77:79])[0]
    _log('gateway ok: game=%s:%d userId=%s' % (game_ip, game_port, uid8.encode('hex')))
    return game_ip, game_port, uid8, lid4


# ---- requests 钩子 ----------------------------------------------------------

class LocalResp(object):
    """最小 requests.Response 桩（probe_stage19 验证过的接口面）。"""

    def __init__(self, text, url=''):
        self.status_code = 200
        self.text = text
        if isinstance(text, unicode):
            self.content = text.encode('utf-8')
        else:
            self.content = text
        self.url = url
        self.headers = {}
        self.encoding = 'utf-8'

    def json(self):
        return json.loads(self.content)

    def raise_for_status(self):
        pass


def _is_author_url(url):
    try:
        for host in AUTHOR_HOSTS:
            if host in url:
                return True
    except Exception:
        pass
    return False


def _extract_data(args, kw):
    if 'data' in kw and kw['data'] is not None:
        return kw['data']
    if args:
        return args[0]
    return None


def _handle_author(url, args, kw):
    """作者服务器 URL 的本地应答。"""
    if LOGIN_MARK in url:
        body = _extract_data(args, kw)
        creds = decrypt_request(body)
        token = resolve_token(creds)
        if not token:
            return local_error(u'未配置渠道登录串(token)：请在 config.ini [login] 填 '
                               u'token=<appid=...&sign=... 完整串>，或 token_{区号}=')
        gw_ip, gw_port = resolve_gateway(creds)
        game_ip, game_port, uid8, lid4 = gateway_exchange(token, gw_ip, gw_port)
        resp = build_login_response(creds, game_ip, game_port, uid8, lid4)
        _log('login ok: gw=%s:%d game=%s:%d token=%s' %
             (gw_ip, gw_port, game_ip, game_port, _mask_token(token)))
        return LocalResp(resp, url)
    # 其余作者服务器端点（check.php/new_version.json/排行榜/热码等）：无害空应答
    _log('benign: %s' % url)
    return LocalResp('{}' if '.json' in url else '', url)


def _dispatch(real_func, url, args, kw):
    try:
        if _is_author_url(url):
            return _handle_author(url, args, kw)
    except GatewayError as e:
        return local_error(unicode(e))
    except Exception:
        _log('dispatch error on %s:\n%s' % (url, traceback.format_exc()))
        if _is_author_url(url):
            return local_error(u'本地授权层内部错误（详见 log/local_auth.log）')
        # 非作者服务器请求不该进这里；兜底原样放行
    return real_func(url, *args, **kw)


def _post(url, *args, **kw):
    return _dispatch(_real_post, url, args, kw)


def _get(url, *args, **kw):
    return _dispatch(_real_get, url, args, kw)


def install():
    """幂等安装钩子。必须在 import game 之前调用。"""
    global _installed, _real_post, _real_get
    if _installed:
        return
    _real_post = requests.post
    _real_get = requests.get
    requests.post = _post
    requests.get = _get
    _installed = True
    _log('installed (local auth layer active, author server %s bypassed)' %
         ','.join(AUTHOR_HOSTS))
