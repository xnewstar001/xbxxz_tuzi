# -*- coding: utf-8 -*-
"""
语义校验（须用 Python 2.7 运行，如 tools/py27/python.exe）:
把还原的 op.py 真实执行，与原始 op.pyc 反序列化出的模块逐变量对比。
用法: <py27> verify_op_py27.py
结论输出: identical: N, different: M —— 期望 M=0
"""
import sys, marshal

def P(s):
    if isinstance(s, unicode):
        sys.stdout.write(s + u'\n')
    else:
        sys.stdout.write(unicode(s, 'utf-8') + u'\n')

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pyc = open(os.path.join(ROOT, 'original_bytecode', 'op.pyc'), 'rb').read()
code = marshal.loads(pyc[8:])

src = open(os.path.join(ROOT, 'src', 'op.py'), 'rb').read()
g = {'__builtins__': __builtins__, '__name__': 'op_orig'}
exec code in g

h = {'__builtins__': __builtins__, '__name__': 'op_restored'}
exec compile(src, 'op_restored.py', 'exec') in h

names_pyc = set(k for k in g if not k.startswith('__'))
names_src = set(k for k in h if not k.startswith('__'))
P('pyc names: %d, src names: %d' % (len(names_pyc), len(names_src)))
P('only in pyc: %s' % sorted(names_pyc - names_src)[:20])
P('only in src: %s' % sorted(names_src - names_pyc)[:20])

diff = []
same = 0
for k in sorted(names_pyc & names_src):
    if g[k] == h[k]:
        same += 1
    else:
        diff.append(k)
P('identical: %d, different: %d' % (same, len(diff)))
for k in diff[:20]:
    a, b = g[k], h[k]
    P('--- %s %s' % (k, type(a).__name__))
    P('  pyc: %s' % repr(a)[:200])
    P('  src: %s' % repr(b)[:200])
