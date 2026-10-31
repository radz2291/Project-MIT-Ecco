"""Read-only CLI SDNA path inventory; patch_bytes returns bytes and proof, never writes.
Uses Blender's installed official header parser. No Blender scene load/resave.
"""
import pathlib,sys,io,struct,re,gzip,ctypes,hashlib,json,argparse
sys.path.insert(0,r'C:/Program Files/Blender Foundation/Blender 5.2/5.2/scripts/modules')
from _blendfile_header import BlendFileHeader,BlockHeader
ZSTD_DLL=pathlib.Path(r'C:/Users/RZ1/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/mingw64/bin/libzstd.dll')
class Zstd:
 def __init__(self):
  self.lib=ctypes.CDLL(str(ZSTD_DLL))
  for n,args,ret in [('ZSTD_findFrameCompressedSize',[ctypes.c_void_p,ctypes.c_size_t],ctypes.c_size_t),('ZSTD_getFrameContentSize',[ctypes.c_void_p,ctypes.c_size_t],ctypes.c_ulonglong),('ZSTD_decompress',[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_size_t],ctypes.c_size_t),('ZSTD_compressBound',[ctypes.c_size_t],ctypes.c_size_t),('ZSTD_compress',[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_int],ctypes.c_size_t),('ZSTD_isError',[ctypes.c_size_t],ctypes.c_uint)]:
   f=getattr(self.lib,n);f.argtypes=args;f.restype=ret
 def checked(self,n):
  if self.lib.ZSTD_isError(n):raise ValueError('zstd error')
  return n
 def decode_frames(self,data):
  out=[];p=0;source=ctypes.create_string_buffer(data)
  while p<len(data):
   buf=ctypes.byref(source,p);n=self.checked(self.lib.ZSTD_findFrameCompressedSize(buf,len(data)-p));size=self.lib.ZSTD_getFrameContentSize(buf,n)
   if size>=2**64-2:raise ValueError('Unknown zstd content size: use Blender fallback; no guessing allocation')
   dest=ctypes.create_string_buffer(size);got=self.checked(self.lib.ZSTD_decompress(dest,size,buf,n));assert got==size;out.append((data[p:p+n],dest.raw[:got]));p+=n
  return out
 def encode(self,data):
  source=ctypes.create_string_buffer(data);cap=self.lib.ZSTD_compressBound(len(data));dest=ctypes.create_string_buffer(cap);n=self.checked(self.lib.ZSTD_compress(dest,cap,source,len(data),3));return dest.raw[:n]
def decode(data):
 if data.startswith(b'BLENDER'):return data,('raw',None)
 if data.startswith(b'\x1f\x8b'):return gzip.decompress(data),('gzip',None)
 if data.startswith(b'\x28\xb5\x2f\xfd'):
  frames=Zstd().decode_frames(data);return b''.join(x[1] for x in frames),('zstd',frames)
 raise ValueError('Unknown .blend container')
def encode(raw,container):
 kind,frames=container
 if kind=='raw':return raw
 if kind=='gzip':return gzip.compress(raw,mtime=0)
 out=[];p=0;z=Zstd()
 for packed,unpacked in frames:
  part=raw[p:p+len(unpacked)];out.append(packed if part==unpacked else z.encode(part));p+=len(unpacked)
 assert p==len(raw);return b''.join(out)
class Blend:
 def __init__(self,data):
  self.raw,self.container=decode(data);f=io.BytesIO(self.raw);self.header=BlendFileHeader(f);hs=self.header.create_block_header_struct();self.blocks=[]
  while f.tell()<len(self.raw):
   h=BlockHeader(f,hs);offset=f.tell()
   if h.code==b'ENDB':break
   assert h.size>=0 and offset+h.size<=len(self.raw);self.blocks.append((h,offset));f.seek(h.size,1)
  dna=next(self.raw[o:o+h.size] for h,o in self.blocks if h.code==b'DNA1');self.parse_dna(dna)
 def parse_dna(self,d):
  p=0;end='<' if self.header.is_little_endian else '>'
  def tag(v):
   nonlocal p
   assert d[p:p+4]==v,(p,v,d[p:p+4]);p+=4
  def num(fmt):
   nonlocal p
   n=struct.unpack_from(end+fmt,d,p)[0];p+=struct.calcsize(fmt);return n
  def strings(n):
   nonlocal p
   a=[]
   for _ in range(n):e=d.index(0,p);a.append(d[p:e].decode('ascii'));p=e+1
   p=(p+3)&~3;return a
  tag(b'SDNA');tag(b'NAME');names=strings(num('I'));tag(b'TYPE');types=strings(num('I'));tag(b'TLEN');sizes=[num('H') for _ in types];p=(p+3)&~3;tag(b'STRC');self.structs=[];self.bytype={}
  for _ in range(num('I')):
   typ=num('H');count=num('H');fields=[];offset=0
   for _ in range(count):
    ft=num('H');fn=num('H');name=names[fn];dims=[int(x) for x in re.findall(r'\[(\d+)\]',name)];mult=1
    for n in dims:mult*=n
    pointer='*' in name;size=(self.header.pointer_size if pointer else sizes[ft])*mult;fields.append({'type':types[ft],'name':name,'offset':offset,'size':size,'array':mult,'dims':dims,'pointer':pointer});offset+=size
   item={'name':types[typ],'size':sizes[typ],'computed_size':offset,'fields':fields};self.structs.append(item);self.bytype[item['name']]=item
  self.cache={}
 def leaves(self,name,seen=()):
  if name in self.cache:return self.cache[name]
  if name in seen:return []
  st=self.bytype[name]
  if st['computed_size']!=st['size']:raise ValueError('SDNA layout mismatch '+name)
  out=[]
  for f in st['fields']:
   if f['pointer']:continue
   if f['type']=='char' and f['array']>1:
    assert f['size']==f['array'],'Unsupported char width'
    width=f['dims'][-1]
    for row in range(f['array']//width):out.append((f['name']+(' row'+str(row) if f['array']!=width else ''),f['offset']+row*width,width))
   elif f['type'] in self.bytype:
    child=self.bytype[f['type']]
    for i in range(f['array']):
     for n,o,z in self.leaves(f['type'],seen+(name,)):out.append((f['name']+'.'+n,f['offset']+i*child['size']+o,z))
  self.cache[name]=out;return out
 def paths(self):
  result=[]
  for h,o in self.blocks:
   if h.code==b'DNA1' or h.sdna_index<0 or h.sdna_index>=len(self.structs):continue
   st=self.structs[h.sdna_index]
   if h.count<=0 or st['size']*h.count>h.size:continue
   leaves=self.leaves(st['name'])
   if not leaves:continue
   for i in range(h.count):
    for field,off,cap in leaves:
     at=o+i*st['size']+off;b=self.raw[at:at+cap].split(b'\0',1)[0]
     if not b:continue
     try:value=b.decode('utf8')
     except UnicodeDecodeError:continue
     library=st['name']=='Library' and field.split('[')[0] in ('name','filepath','filepath_abs')
     looks=bool(value.startswith('//') or re.match(r'^[A-Za-z]:[/\\]',value) or value.startswith('/') or ('/' in value or '\\' in value) and re.search(r'\.[A-Za-z0-9]{1,8}$',value))
     external=st['name'] in ('Image','VFont','bSound','MovieClip','CacheFile','Volume','AlembicCache','MeshCacheModifierData','OceanModifierData','FluidDomainSettings','NodeTexImage','Sequence','Strip','StripElem') and '.' not in field and any(x in field.lower() for x in ('name','file','path','dir'))
     if library or looks or external:result.append({'struct':st['name'],'field':field,'offset':at,'capacity':cap,'value':value,'library':library,'block':h.code.decode('ascii',errors='replace'),'block_address':h.addr_old,'external_candidate':external})
  return result
def patch_bytes(data,replacements):
 """replacements: exact offset→new UTF8 string, inventory offsets only. No disk writes."""
 b=Blend(data);known={x['offset']:x for x in b.paths()};patched=bytearray(b.raw);ranges=[]
 for offset,value in replacements.items():
  offset=int(offset);item=known[offset];v=value.encode('utf8');cap=item['capacity'];assert b'\0' not in v and len(v)<cap,'Path overflow or NUL'
  before=bytes(patched[offset:offset+cap]);after=v+b'\0'+before[len(v)+1:];patched[offset:offset+cap]=after;ranges.append((offset,offset+cap))
 # Every decoded changed byte must be inside a selected, validated SDNA field.
 cursor=0
 for a,z in sorted(ranges):
  assert a>=cursor,'Overlapping path fields'
  assert b.raw[cursor:a]==patched[cursor:a];cursor=z
 assert b.raw[cursor:]==patched[cursor:]
 assert len(patched)==len(b.raw);encoded=encode(bytes(patched),b.container);check=Blend(encoded);assert check.raw==bytes(patched)
 return encoded,{'container':b.container[0],'decoded_length':len(b.raw),'changed_fields':len(ranges),'authorized_ranges':ranges,'decoded_original_sha256':hashlib.sha256(b.raw).hexdigest(),'decoded_patched_sha256':hashlib.sha256(check.raw).hexdigest(),'only_authorized_path_bytes_changed':True}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('blend');args=ap.parse_args();p=pathlib.Path(args.blend);b=Blend(p.read_bytes());print(json.dumps({'path':str(p),'container':b.container[0],'header_format':b.header.file_format_version,'version':b.header.version,'paths':b.paths()},indent=2))
