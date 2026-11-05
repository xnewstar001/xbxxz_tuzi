# -*- coding: utf-8 -*-
"""
从 PYZ-00.pyz 提取指定模块并补 Python 2.7 pyc 头。
用法: python extract_pyz.py <PYZ路径> <输出目录> [模块名 ...]
默认模块: op qt_main browser icon xbxxz_pb2 Pic_rc
说明:
  - CArchive 中类型为 s/m 的条目与 PYZ 条目都是 marshal 后的 code object（无 pyc 头）。
  - PYZ 内条目是 zlib 压缩的 marshal 数据；CArchive 内 s/m 条目未压缩。
  - Python 2.7 pyc 头 = magic(4) + mtime(4) = b'\x03\xf3\x0d\x0a' + 4 字节。
"""
import struct, marshal, zlib, os, sys

PY27_MAGIC = b'\x03\xf3\x0d\x0a'
DEFAULTS = ['op', 'qt_main', 'browser', 'icon', 'xbxxz_pb2', 'Pic_rc']

def main():
    pyz_path, out = sys.argv[1], sys.argv[2]
    targets = sys.argv[3:] or DEFAULTS
    os.makedirs(out, exist_ok=True)
    pyz = open(pyz_path, 'rb').read()
    assert pyz[:4] == b'PYZ\0', 'not a PYZ archive'
    tocOff = struct.unpack('!i', pyz[8:12])[0]
    toc = marshal.loads(pyz[tocOff:])
    for item in toc:
        name, (typ, pos, length) = item
        if isinstance(name, bytes):
            name = name.decode()
        base = name.split('.')[-1]
        if base in targets:
            raw = pyz[pos:pos+length]
            if raw[:2] in (b'x\x9c', b'x\xda', b'x\x01'):
                raw = zlib.decompress(raw)
            fp = os.path.join(out, base + '.pyc')
            open(fp, 'wb').write(PY27_MAGIC + b'\x00\x00\x00\x00' + raw)
            print(f'{base}: {len(raw):,} bytes -> {fp}')

if __name__ == '__main__':
    main()
