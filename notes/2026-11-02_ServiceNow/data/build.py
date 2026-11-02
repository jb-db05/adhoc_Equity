import sys,html
D,S=sys.argv[1],sys.argv[2]
t=open(f'{D}/note.template.html').read()
disc=''.join(f'<p>{html.escape(l.strip())}</p>' for l in open(f'{S}/disclaimer.txt') if l.strip())
t=t.replace('DISCLAIMER',disc).replace('SOURCE_LINE','Yahoo Finance')
for i in range(1,5): t=t.replace(f'url(NUNITO{i})',f'url(file://{S}/fonts/nunito{i}.ttf)')
open(f'{D}/note.html','w').write(t)
