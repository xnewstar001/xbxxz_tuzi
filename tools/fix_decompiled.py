# -*- coding: utf-8 -*-
import io, os, re, sys

CODING = '# -*- coding: utf-8 -*-\n'
PAT = re.compile(r'\\u\s?0x([0-9a-fA-F]{4})')

def fix_text(text):
    n = [0]
    def rep(m):
        n[0] += 1
        return chr(int(m.group(1), 16))
    return PAT.sub(rep, text), n[0]

def strip_toplevel_return(text):
    lines = text.split('\n')
    while lines and lines[-1].strip() == '':
        lines.pop()
    if lines and lines[-1] == 'return':
        lines.pop()
        while lines and lines[-1].strip() == '':
            lines.pop()
    return '\n'.join(lines) + '\n'

def add_coding(text):
    lines = text.split('\n')
    if any('coding:' in l for l in lines[:3]):
        return text
    lines.insert(1, CODING.rstrip('\n'))
    return '\n'.join(lines)

def main():
    in_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    for name in sorted(os.listdir(in_dir)):
        if not name.endswith('.py'):
            continue
        raw = io.open(os.path.join(in_dir, name), 'r', encoding='utf-8').read()
        fixed, cnt = fix_text(raw)
        fixed = strip_toplevel_return(fixed)
        fixed = add_coding(fixed)
        io.open(os.path.join(out_dir, name), 'w', encoding='utf-8', newline='\n').write(fixed)
        print(f'{name}: fixed {cnt} escapes, {len(raw):,} -> {len(fixed):,} chars')

if __name__ == '__main__':
    main()
