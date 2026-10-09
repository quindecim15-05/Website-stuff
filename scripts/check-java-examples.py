"""Compile and run every Java Code Analysis question; expected failures are checked as well."""
import json, subprocess, tempfile
from pathlib import Path
questions=json.loads(Path('src/content/data.json').read_text(encoding='utf8'))['questions']
errors=[]
for q in [x for x in questions if x['type']=='code-analysis']:
 with tempfile.TemporaryDirectory() as tmp:
  path=Path(tmp)/'Main.java';path.write_text(q['code'])
  compiled=subprocess.run(['javac',str(path)],capture_output=True,text=True,timeout=20)
  output=('Compilation error' if compiled.returncode else subprocess.run(['java','-cp',tmp,'Main'],capture_output=True,text=True,timeout=20).stdout.strip())
  expected=next(o['text'] for o in q['options'] if o['id']==q['correctOptionId'])
  okay=output==expected or (output=='Compilation error' and expected.lower().startswith('compilation error'))
  print(('PASS' if okay else 'FAIL'),q['id'],'=>',output)
  if not okay:errors.append(q['id'])
print(f'Java Code Analysis: {len(questions) if False else len([x for x in questions if x["type"]=="code-analysis"])} checked, {len(errors)} failed')
if errors:raise SystemExit(1)
