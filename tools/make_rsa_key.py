# -*- coding: utf-8 -*-
"""生成 RSA-2048 密钥对（py2 + PyCrypto）— 简化版

输出到 tools/keys/：
  mykey_priv.pem    私钥（**绝不入库/绝不外传**，.gitignore 已排除 keys/ 下的私钥）
  mykey_pub_spki.b64 公钥 SPKI base64（apply_offline.py 用它等长替换 game.pyd 内嵌公钥）
  mykey.json        密钥参数备份
注意：重新生成密钥后必须重跑 apply_offline.py 重打 pyd 公钥补丁。
"""
import os, sys, json, time, threading, base64

threading.Timer(120, lambda: os._exit(7)).start()
sys.path.insert(0, os.getcwd())

from Crypto.PublicKey import RSA

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys')
if not os.path.isdir(OUTDIR):
    os.makedirs(OUTDIR)

t0 = time.time()
key = RSA.generate(2048)
print('key generated in %.1fs' % (time.time() - t0))

open(os.path.join(OUTDIR, 'mykey_priv.pem'), 'wb').write(key.exportKey('PEM', pkcs=8))

pub = key.publickey()
spki_der = pub.exportKey('DER')          # PyCrypto 公钥 DER = SubjectPublicKeyInfo
b64 = base64.b64encode(spki_der)
print('SPKI DER len:', len(spki_der), 'b64 len:', len(b64))
open(os.path.join(OUTDIR, 'mykey_pub_spki.b64'), 'wb').write(b64)

json.dump({'n': format(key.n, 'x'), 'e': format(key.e, 'x'),
           'd': format(key.d, 'x'), 'p': format(key.p, 'x'), 'q': format(key.q, 'x')},
          open(os.path.join(OUTDIR, 'mykey.json'), 'w'))
print('saved to', OUTDIR)
os._exit(0)
