import random, sys, importlib
sys.path.insert(0,'.')
m=importlib.import_module(sys.argv[1])
out="<body style='display:grid;grid-template-columns:1fr 1fr;gap:8px;width:1200px'>"
names=[f.__name__ for fl in m.BY_SKILL.values() for f in fl]
for name in names:
    f=getattr(m,name)
    for l in (0,2):
        q=None;errs=set()
        for sd in range(150):
            try: q=f(random.Random(l+sd),l);break
            except Exception as e: errs.add(type(e).__name__+':'+str(e)[:60])
        if q is None:
            print('FAIL',name,l,errs);continue
        out+=f"<div style='border:1px solid #999'><small>{name} L{l}: {q['q'][:80]} → {q['o'][0]} | {q['o'][1:3]}</small>{q['svg'] or '(sin figura)'}</div>"
open('/tmp/claude-0/sheet.html','w').write(out)
