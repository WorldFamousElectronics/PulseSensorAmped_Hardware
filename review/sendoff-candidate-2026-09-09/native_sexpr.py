import re,json
def parse(text):
 stack=[];root=None
 for m in re.finditer(r'"(?:\\.|[^"\\])*"|[()]|[^()\s]+',text):
  t=m.group()
  if t=='(':
   n={'start':m.start(),'items':[]}
   if stack:stack[-1]['items'].append(n)
   else:root=n
   stack.append(n)
  elif t==')':stack.pop()['end']=m.end()
  else:stack[-1]['items'].append(json.loads(t) if t.startswith('"') else t)
 return root
def children(n,kind):return [x for x in n['items'] if isinstance(x,dict) and x['items'][0]==kind]
def apply(text,edits):
 for a,b,v in sorted(edits,reverse=True):text=text[:a]+v+text[b:]
 return text
