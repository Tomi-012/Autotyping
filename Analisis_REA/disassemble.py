import marshal, dis, types, sys
from pathlib import Path
p = Path(sys.argv[1])
with p.open('rb') as f:
    f.read(16)
    code = marshal.load(f)
def walk(c):
    print('\n' + '=' * 80)
    print('FUNCTION:', c.co_qualname, 'SOURCE LINE:', c.co_firstlineno)
    dis.dis(c, depth=0)
    for item in c.co_consts:
        if isinstance(item, types.CodeType):
            walk(item)
walk(code)
