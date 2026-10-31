"""Fix relocated active runtime Python only. Default dry run; --apply after moves.

--source-preview validates proposed transformations against pre-move sources.
No Blender imports, native writes, metadata rewrites, or historical report edits.
"""
import argparse,ast,hashlib,io,json,os,re,tokenize
from pathlib import Path

def find_root(start):
 for p in [start,*start.parents]:
  if (p/'04-Production').is_dir():return p
 raise RuntimeError('Cannot discover repository root')

ROOT=find_root(Path(__file__).resolve().parent)
BASE=ROOT/'04-Production/Records/Tasks/T-051/Reorganization'
ASSETS='04-Production/Shared/Assets/'
ROOT_HELPER='''\ndef _ecco_repo_root():
    from pathlib import Path
    for candidate in Path(__file__).resolve().parents:
        if (candidate / '04-Production').is_dir():
            return candidate
    raise RuntimeError('ECCO repository root not found')
'''

def insert_helpers(text,helper):
 parsed=ast.parse(text);lines=text.splitlines(keepends=True);at=0
 if parsed.body and isinstance(parsed.body[0],ast.Expr) and isinstance(parsed.body[0].value,ast.Constant) and isinstance(parsed.body[0].value.value,str):at=parsed.body[0].end_lineno
 # Preserve future-import placement, if a helper ever gains one.
 for item in parsed.body:
  if isinstance(item,ast.ImportFrom) and item.module=='__future__':at=item.end_lineno
 lines.insert(at,'\n'+helper+'\n');return ''.join(lines)

def literal_map(text,mapping):
 tokens=[]
 for tok in tokenize.generate_tokens(io.StringIO(text).readline):
  if tok.type==tokenize.STRING:
   try:value=ast.literal_eval(tok.string)
   except (ValueError,SyntaxError):value=None
   if isinstance(value,str) and '\n' not in value:
    normalized=value.replace('\\','/')
    if normalized in mapping:
     tok=tokenize.TokenInfo(tok.type,repr(mapping[normalized]),tok.start,tok.end,tok.line)
  tokens.append(tok)
 return tokenize.untokenize(tokens)

def patch(text,entry,plan):
 original=text;maps={}
 if entry['old'].endswith('Acoustics/Scripts/build_sensing_v001.py'):
  text=text.replace('ROOT=HERE.parents[4]', "ROOT=next(p for p in HERE.parents if (p / '04-Production').is_dir())").replace("DEST=A/'Acoustics'", 'DEST=HERE.parent')
 if '# ECCO_RUNTIME_PATH_MIGRATION_20261031' in text:
  ast.parse(text,filename=entry['new']);return text,False
 for row in plan:
  maps[row['old']]=row['new']
  if row['old'].startswith(ASSETS):maps[row['old'][len(ASSETS):]]=os.path.relpath(row['new'],'04-Production/Shared/Assets').replace('\\','/')
 # Mixed integration API uses old helper directories; preserve its legacy imports.
 maps['CasedHole/Scripts']='Environment/Borehole/Scripts'
 maps['Acoustics/Scripts']='../Archive/2026-10-31/Assets/Acoustics/Scripts'
 text=literal_map(text,maps)
 name=Path(entry['new']).name
 needed={}
 if name=='world_controls.py':
  old="env=load(asset_dir/('WellAssembly/World_environment_'+environment_version+'.blend'),list(specs))"
  new="env=load(_ecco_asset_path(asset_dir,'WellAssembly/World_environment_'+environment_version+'.blend'),list(specs))"
  old2="hw=load(asset_dir/('BHA/BHA_film_'+hardware_version+'.blend'),['WORLD_HARDWARE'])"
  new2="hw=load(_ecco_asset_path(asset_dir,'BHA/BHA_film_'+hardware_version+'.blend'),['WORLD_HARDWARE'])"
  if '_ecco_asset_path' not in text:
   assert old in text and old2 in text,'world_controls dynamic expressions drifted'
   text=text.replace(old,new).replace(old2,new2)
   needed={r['old'][len(ASSETS):]:r['new'] for r in plan if r['old'].startswith(ASSETS) and re.search(r'/(?:World_environment|BHA_film)_v\d+\.blend$',r['old'])}
 elif name=='cased_controls_v001.py' and '_ecco_asset_path' not in text:
  old="p=Path(asset_dir)/'CasedHole'/('CasedHole_'+version+'.blend')"
  assert old in text,'cased_controls dynamic expression drifted'
  text=text.replace(old,"p=_ecco_asset_path(asset_dir,'CasedHole/CasedHole_'+version+'.blend')")
  needed={r['old'][len(ASSETS):]:r['new'] for r in plan if r['old'].startswith(ASSETS+'CasedHole/') and r['old'].endswith('.blend')}
 if needed:
  helper=ROOT_HELPER+'''\ndef _ecco_asset_path(asset_root, legacy_relative):
    # Exact immutable versions from migration map; never substitute newer geometry.
    routes = '''+repr(needed)+'''
    if legacy_relative not in routes:
        raise ValueError('Unmapped ECCO legacy asset version: '+legacy_relative)
    from pathlib import Path
    # Preserve API caller's checkout, including independent test copies.
    for candidate in [Path(asset_root).resolve(), *Path(asset_root).resolve().parents]:
        if (candidate / '04-Production').is_dir():
            return candidate / routes[legacy_relative]
    raise RuntimeError('ECCO asset_root does not resolve inside a repository')
'''
  text=insert_helpers(text,helper)
 if re.search(r'Path\(__file__\)\.resolve\(\)\.parents\[\d+\]',text):
  text=re.sub(r'Path\(__file__\)\.resolve\(\)\.parents\[\d+\]','_ecco_repo_root()',text)
  if 'def _ecco_repo_root()' not in text:text=insert_helpers(text,ROOT_HELPER)
 if text!=original:text='# ECCO_RUNTIME_PATH_MIGRATION_20261031\n'+text
 ast.parse(text,filename=entry['new'])
 return text, text!=original

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--apply',action='store_true');ap.add_argument('--source-preview',action='store_true');args=ap.parse_args()
 if args.apply and args.source_preview:ap.error('--apply cannot be combined with --source-preview')
 plan=json.loads((BASE/'move-plan.json').read_text(encoding='utf-8-sig'));entries=[r for r in plan if (r['kind']=='active' and r['new'].endswith('.py'))];changes=[];pending=[]
 for entry in entries:
  path=ROOT/(entry['old'] if args.source_preview else entry['new'])
  if not path.is_file():raise FileNotFoundError(path)
  raw=path.read_bytes();text=raw.decode('utf-8-sig');updated,changed=patch(text,entry,plan)
  changes.append({'path':entry['new'],'changed':changed,'before_sha256':hashlib.sha256(raw).hexdigest(),'after_sha256':hashlib.sha256(updated.encode('utf-8')).hexdigest(),'syntax_valid':True})
  if changed:pending.append((entry,path,raw,updated))
 # All inputs and syntax validated before the first write.
 if args.apply:
  for entry,path,raw,updated in pending:
   backup=BASE/'Backup/Runtime'/entry['new'];backup.parent.mkdir(parents=True,exist_ok=True)
   if not backup.exists():backup.write_bytes(raw)
   path.write_text(updated,encoding='utf-8',newline='\n')
  (BASE/'runtime-path-fixes.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
 print(json.dumps({'mode':'apply' if args.apply else ('source-preview' if args.source_preview else 'dry-run'),'checked':len(entries),'changed':len(pending),'files':changes},indent=2))

if __name__=='__main__':main()
