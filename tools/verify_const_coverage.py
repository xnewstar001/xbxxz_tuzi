# -*- coding: utf-8 -*-
"""
常量覆盖校验（Python 3 运行，依赖 xdis）:
检查 pyc 内全部 CJK unicode 常量是否都出现在还原源码中。
用法: python verify_const_coverage.py
"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from xdis.load import load_module

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYC_DIR = os.path.join(ROOT, 'original_bytecode')
SRC_DIR = os.path.join(ROOT, 'src')

for name in ['xbxxz_helper', 'qt_main', 'xbxxz_pb2', 'icon', 'browser', 'op']:
    pyc_path = os.path.join(PYC_DIR, name + '.pyc')
    src_path = os.path.join(SRC_DIR, name + '.py')
    if not os.path.exists(pyc_path) or not os.path.exists(src_path):
        continue
    ver, ts, magic, code, is_pypy, source_size, sip_hash = load_module(pyc_path)
    src = io.open(src_path, encoding='utf-8').read()

    consts = []
    def collect(co):
        for c in co.co_consts:
            if hasattr(c, 'co_consts'):
                collect(c)
            else:
                consts.append(c)
    collect(code)

    total, missing = 0, []
    for c in consts:
        s = None
        if type(c).__name__ == 'UnicodeForPython3':
            s = str(c)
        elif isinstance(c, str):
            try:
                s = c.decode('utf8')
                if not any(0x4e00 <= ord(ch) <= 0x9fff for ch in s):
                    s = None
            except Exception:
                s = None
        if s:
            total += 1
            probe = s.replace('\r', '\\r').replace('\n', '\\n').replace('\t', '\\t')
            if s not in src and probe not in src:
                missing.append(s)
    print(f'{name}: CJK consts={total}, missing={len(missing)}')
    for m in missing[:5]:
        print('   MISSING:', m[:70])
