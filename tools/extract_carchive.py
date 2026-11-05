# -*- coding: utf-8 -*-
"""
从 PyInstaller onefile exe 中提取 CArchive 全部条目。
用法: python extract_carchive.py <exe路径> <输出目录>
产出: <输出目录>/ 下所有条目（.pyc 需后续补头, 见 extract_pyz.py 顶部说明）
"""
import zlib, struct, os, sys

def main():
    exe, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    data = open(exe, 'rb').read()
    n = len(data)

    MAGIC = b'MEI\014\013\012\013\016'
    pos = data.rfind(MAGIC)
    if pos < 0:
        sys.exit('not a PyInstaller CArchive exe')
    magic, lengthofPackage, toc, tocLen, pyvers = struct.unpack_from('!8sIIII', data, pos)
    pylib = data[pos+24:pos+24+64].rstrip(b'\0')
    archiveStart = n - lengthofPackage
    tocData = data[archiveStart+toc: archiveStart+toc+tocLen]
    print(f'pylib={pylib} entries tocLen={tocLen}')

    entries = []
    p = 0
    while p < tocLen:
        entryLen, = struct.unpack_from('!I', tocData, p)
        entryPos, csz, usz, cflag, typ = struct.unpack_from('!IIIBc', tocData, p+4)
        name = tocData[p+18:p+entryLen].rstrip(b'\0').decode('utf-8', 'replace')
        entries.append((entryPos, csz, cflag, typ.decode(), name))
        p += entryLen

    for entryPos, csz, cflag, typ, name in entries:
        raw = data[archiveStart+entryPos: archiveStart+entryPos+csz]
        if cflag == 1:
            raw = zlib.decompress(raw)
        safe = name.replace('\\', '__').replace('/', '__').replace(':', '__')
        fp = os.path.join(out, safe)
        if os.path.exists(fp):
            fp += '.' + typ
        open(fp, 'wb').write(raw)
        print(f'[{typ}] {name} -> {fp} ({len(raw):,} bytes)')

if __name__ == '__main__':
    main()
