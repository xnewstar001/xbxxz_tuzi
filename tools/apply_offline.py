# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))            # fuzhu_project/tools
PROJ = os.path.dirname(ROOT)                                 # fuzhu_project
SRC = os.path.join(PROJ, 'src')
RUN = os.path.join(PROJ, 'run')
RES = os.path.join(PROJ, 'resources')
# RSA 公钥（等长替换 game.pyd 内嵌公钥用；优先仓库内 keys/，回退本地工作目录 analysis/）
KEY_B64_REPO = os.path.join(ROOT, 'keys', 'pub_spki.b64')
KEY_B64_LOCAL = os.path.join(os.path.abspath(os.path.join(PROJ, '..', 'analysis')),
                             'mykey_pub_spki.b64')
KEY_B64 = KEY_B64_REPO if os.path.exists(KEY_B64_REPO) else KEY_B64_LOCAL

HELPER = os.path.join(SRC, 'xbxxz_helper.py')

HOOK_ANCHOR = ('from browser import BrowserDialog\n'
               'import qt_main, icon, xbxxz_pb2, game, op\n')
HOOK_PATCH = ('from browser import BrowserDialog\n'
              'import local_auth\n'
              'local_auth.install()   # 本地授权层：拦截作者服务器请求，脱离 211.159.180.131（见 docs/07）\n'
              'import qt_main, icon, xbxxz_pb2, game, op\n'
              'local_auth.patch_game(game)   # 本地授权状态：覆写 make_self_obj（到期检查，见 docs/07 §9）\n')

ERR_ANCHOR = ("                elif d == 'notime':\n"
              "                    self.signal.emit(a, 90, True)\n"
              "                    self.signal.emit(u'登录失败，原因【辅助到期】，可加美女QQ：158855054 联系试用。', 1, True)\n"
              "                    return\n")
ERR_PATCH = (ERR_ANCHOR +
             "                elif d == 'local_error':\n"
             "                    self.signal.emit(a, 1, True)\n"
             "                    return\n")

BARE_ANCHOR = ("            except:\n"
               "                self.signal.emit(u'登录出现问题，10分钟后再次尝试', 1, True)\n"
               "                time.sleep(600)\n")
BARE_PATCH = ("            except:\n"
              "                try:\n"
              "                    tb = traceback.format_exc()\n"
              "                    if not os.path.isdir('log'):\n"
              "                        os.makedirs('log')\n"
              "                    f = open(os.path.join('log', 'gui_error.log'), 'a')\n"
              "                    f.write('[%s]\\n%s\\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), tb))\n"
              "                    f.close()\n"
              "                    tip = u'登录出现问题，10分钟后再次尝试（原因:%s，详见 log\\\\gui_error.log）' % tb.splitlines()[-1]\n"
              "                except Exception:\n"
              "                    tip = u'登录出现问题，10分钟后再次尝试'\n"
              "                self.signal.emit(tip, 1, True)\n"
              "                time.sleep(600)\n")


def patch_helper(path):
    with open(path, 'rb') as f:
        data = f.read().decode('utf-8')
    changed = False
    if 'local_auth.install()' not in data:
        if HOOK_ANCHOR not in data:
            sys.exit('[x] 钩子安装锚点未找到（xbxxz_helper.py 结构变了？）')
        data = data.replace(HOOK_ANCHOR, HOOK_PATCH, 1)
        changed = True
        print('[src] 已插入 local_auth 安装点（import game 之前）')
    else:
        print('[src] local_auth 安装点已存在')
    if 'local_auth.patch_game(game)' not in data:
        # 分两步补：老版本可能只有 install 没有 patch_game
        anchor2 = 'import qt_main, icon, xbxxz_pb2, game, op\n'
        ins2 = 'local_auth.patch_game(game)   # 本地授权状态：覆写 make_self_obj（到期检查，见 docs/07 §9）\n'
        if anchor2 not in data:
            sys.exit('[x] patch_game 锚点未找到')
        data = data.replace(anchor2, anchor2 + ins2, 1)
        changed = True
        print('[src] 已插入 patch_game 调用（import game 之后）')
    else:
        print('[src] patch_game 调用已存在')
    if "gui_error.log" not in data:
        if BARE_ANCHOR not in data:
            sys.exit('[x] 裸 except 锚点未找到（xbxxz_helper.py 结构变了？）')
        data = data.replace(BARE_ANCHOR, BARE_PATCH, 1)
        changed = True
        print('[src] 已为登录兜底 except 增加诊断日志（log/gui_error.log）')
    else:
        print('[src] 兜底 except 诊断已存在')
    if "elif d == 'local_error':" not in data:
        if ERR_ANCHOR not in data:
            sys.exit('[x] local_error 分支锚点未找到（xbxxz_helper.py 结构变了？）')
        data = data.replace(ERR_ANCHOR, ERR_PATCH, 1)
        changed = True
        print('[src] 已插入 d==local_error 分支（GameThread.run）')
    else:
        print('[src] local_error 分支已存在')
    if changed:
        with open(path, 'wb') as f:
            f.write(data.encode('utf-8'))
    return changed


def ensure_pyd_patched(path):
    """确保 game.pyd 的内嵌 RSA 公钥已替换为我们自己的（等长、幂等）。"""
    if not os.path.exists(path):
        print('[pyd] %s 不存在，跳过（先跑 build_runtime.py）' % path)
        return False
    if not os.path.exists(KEY_B64):
        print('[pyd] 找不到 %s，跳过公钥补丁' % KEY_B64)
        return False
    new_b64 = open(KEY_B64, 'rb').read().strip()
    data = open(path, 'rb').read()
    m = re.search(rb'(-----BEGIN PUBLIC KEY-----\n)([A-Za-z0-9+/=\r\n]+?)(-----END PUBLIC KEY-----)', data)
    if not m:
        print('[pyd] %s 内未找到公钥块，跳过' % path)
        return False
    body = m.group(2)
    flat = re.sub(rb'[\r\n]', b'', body)
    if flat == new_b64:
        print('[pyd] %s 已是补丁版' % path)
        return False
    if len(flat) != len(new_b64):
        sys.exit('[x] 公钥长度不一致：old=%d new=%d' % (len(flat), len(new_b64)))
    lines = [new_b64[i:i + 64] for i in range(0, len(new_b64), 64)]
    new_body = b'\n'.join(lines)
    if body.endswith(b'\n'):
        new_body += b'\n'
    assert len(body) == len(new_body)
    bak = path + '.orig.bak'
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
        print('[pyd] 原版已备份 -> %s' % bak)
    patched = data[:m.start(2)] + new_body + data[m.end(2):]
    assert len(patched) == len(data)
    with open(path, 'wb') as f:
        f.write(patched)
    print('[pyd] %s RSA 公钥已替换（等长）' % path)
    return True


def sync_to_run():
    n = 0
    for name in ('local_auth.py', 'xbxxz_helper.py'):
        s = os.path.join(SRC, name)
        d = os.path.join(RUN, name)
        shutil.copy2(s, d)
        print('[run] %s' % name)
        n += 1
    s = os.path.join(RES, 'config.ini.example')
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(RUN, 'config.ini.example'))
        print('[run] config.ini.example（不触碰用户 config.ini）')
        n += 1
    return n


def main():
    print('== apply_offline：脱离作者服务器改造固化 ==')
    if not os.path.exists(os.path.join(SRC, 'local_auth.py')):
        sys.exit('[x] src/local_auth.py 缺失（它随仓库交付，不应被删除）')
    patch_helper(HELPER)
    ensure_pyd_patched(os.path.join(RUN, 'game.pyd'))
    sync_to_run()
    print('== 完成。验证命令（在 run/ 下）：')
    print('   ..\\tools\\py27\\python.exe -m compileall -q ..\\src ..\\tools\\probe_stage38.py')
    print('   ..\\tools\\py27\\python.exe ..\\tools\\probe_stage38.py')
    print('   GUI: 双击 run\\启动辅助.bat（config.ini [login] 配 token 后点开始挂机）')


if __name__ == '__main__':
    main()
