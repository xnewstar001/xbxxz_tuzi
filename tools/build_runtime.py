# -*- coding: utf-8 -*-
"""
组装可运行目录 run/：
  - exe CArchive 的二进制运行时（Qt DLL、PyQt4/sip/Crypto 的 .pyd、CRT、qt4_plugins、cacert.pem）
  - PYZ 中的第三方纯 Python 包（PyQt4/__init__、Crypto、google.protobuf、requests、chardet、certifi、idna、backports、configparser）
  - src/ 还原源码 + resources/ 运行数据
用法: python build_runtime.py  （在项目根执行）
"""
import os, struct, marshal, zlib, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(ROOT, '..', '..', 'fuzhu', u'修真辅助v8.5.exe')
SRC = os.path.join(ROOT, '..', 'src')
RES = os.path.join(ROOT, '..', 'resources')
RUN = os.path.join(ROOT, '..', 'run')

PYZ_PKGS = ['PyQt4', 'Crypto', 'google', 'requests', 'chardet', 'certifi', 'idna', 'backports', 'configparser', 'urllib3', 'six', 'netbios']
CRT_DLLS = ['msvcr90.dll', 'msvcp90.dll', 'msvcm90.dll']

def parse_carchive(data):
    MAGIC = b'MEI\014\013\012\013\016'
    pos = data.rfind(MAGIC)
    _, lengthofPackage, toc, tocLen, pyvers = struct.unpack_from('!8sIIII', data, pos)
    start = len(data) - lengthofPackage
    tocData = data[start+toc: start+toc+tocLen]
    entries = []
    p = 0
    while p < tocLen:
        entryLen, = struct.unpack_from('!I', tocData, p)
        entryPos, csz, usz, cflag, typ = struct.unpack_from('!IIIBc', tocData, p+4)
        name = tocData[p+18:p+entryLen].rstrip(b'\0').decode('utf-8', 'replace')
        entries.append((start+entryPos, csz, cflag, typ.decode(), name))
        p += entryLen
    return entries

def read_entry(data, e):
    off, csz, cflag, typ, name = e
    raw = data[off:off+csz]
    if cflag == 1:
        raw = zlib.decompress(raw)
    return raw, typ, name

def write_pyz_module(pyz, name, typ, pos, length, outdir):
    raw = pyz[pos:pos+length]
    if raw[:2] in (b'x\x9c', b'\xda', b'x\x01', b'x\xda'):
        raw = zlib.decompress(raw)
    rel = name.replace('.', '/')
    if typ == 1:  # package -> __init__
        fp = os.path.join(outdir, rel, '__init__.pyc')
    else:
        fp = os.path.join(outdir, rel + '.pyc')
    fp = os.path.abspath(fp)
    if not fp.startswith(os.path.abspath(outdir)):
        raise ValueError(name)
    d = os.path.dirname(fp)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with open(fp, 'wb') as f:
        f.write(b'\x03\xf3\x0d\x0a\x00\x00\x00\x00' + raw)
    return fp

def main():
    if os.path.isdir(RUN):
        shutil.rmtree(RUN)
    os.makedirs(RUN)
    data = open(EXE, 'rb').read()
    entries = parse_carchive(data)
    pyz_raw = None
    pyz_entry = None

    # 1) 二进制运行时
    for e in entries:
        raw, typ, name = read_entry(data, e)
        if typ == 'z':
            pyz_raw, pyz_entry = raw, e
            continue
        if typ in ('s', 'm', 'o'):   # 主脚本/模块/manifest: 用还原源码
            continue
        if typ == 'x':               # 数据文件
            if name == 'certifi\\cacert.pem':
                fp = os.path.join(RUN, 'certifi', 'cacert.pem')
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                open(fp, 'wb').write(raw)
            continue
        # typ == 'b': dll/pyd/manifest 等
        rel = name.replace('\\', os.sep).replace('/', os.sep)
        # PyInstaller 用点分名存包内扩展: PyQt4.QtCore.pyd -> PyQt4/QtCore.pyd
        stem, ext = os.path.splitext(rel)
        if ext in ('.pyd', '.dll') and (stem.startswith('PyQt4.') or stem.startswith('Crypto.')):
            rel = stem.replace('.', os.sep) + ext
        fp = os.path.join(RUN, rel)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, 'wb').write(raw)

    # 2) PYZ 第三方包
    assert pyz_raw and pyz_raw[:4] == b'PYZ\0'
    tocOff = struct.unpack('!i', pyz_raw[8:12])[0]
    toc = marshal.loads(pyz_raw[tocOff:])
    n_pyz = 0
    for item in toc:
        nm, (typ, pos, length) = item
        if isinstance(nm, bytes):
            nm = nm.decode()
        top = nm.split('.')[0]
        if top in PYZ_PKGS:
            write_pyz_module(pyz_raw, nm, typ, pos, length, RUN)
            n_pyz += 1

    # 3) Qt DLL 复制进 PyQt4/（pyd 以 LOAD_WITH_ALTERED_SEARCH_PATH 加载时优先搜自己目录）
    pyqt4_dir = os.path.join(RUN, 'PyQt4')
    for dll in os.listdir(RUN):
        if dll.startswith('Qt') and dll.endswith('.dll'):
            shutil.copy(os.path.join(RUN, dll), os.path.join(pyqt4_dir, dll))
        if dll in ('sip.pyd',):
            pass  # sip.pyd 在顶层即可

    # 4) CRT 复制到 python 解释器目录，保证 tools/py27 自包含
    py27_dir = os.path.join(ROOT, 'py27')
    for dll in CRT_DLLS:
        srcp = os.path.join(RUN, dll)
        if os.path.exists(srcp):
            shutil.copy(srcp, os.path.join(py27_dir, dll))

    # 5) 还原源码 + 资源
    for f in os.listdir(SRC):
        shutil.copy(os.path.join(SRC, f), os.path.join(RUN, f))
    for f in os.listdir(RES):
        s = os.path.join(RES, f)
        d = os.path.join(RUN, f)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy(s, d)

    print(f'run/ 组装完成: CArchive 条目 {len(entries)}, PYZ 模块 {n_pyz}')
    print('顶层内容:', sorted(os.listdir(RUN))[:40])

if __name__ == '__main__':
    main()
