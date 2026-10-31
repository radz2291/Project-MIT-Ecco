"""Sparse byte-exact rollback data; pure in-memory functions, no native writes."""
import ctypes,base64,hashlib,json
from blend_path_bytes import Zstd
def sha(b):return hashlib.sha256(b).hexdigest()
def frames(data):
 z=Zstd();buf=ctypes.create_string_buffer(data);p=0;logical=0;out=[]
 while p<len(data):
  ptr=ctypes.byref(buf,p);n=z.checked(z.lib.ZSTD_findFrameCompressedSize(ptr,len(data)-p));size=z.lib.ZSTD_getFrameContentSize(ptr,n)
  if size>=2**64-2:raise ValueError('Unknown zstd frame content size')
  out.append({'offset':p,'length':n,'decoded_offset':logical,'decoded_length':size});p+=n;logical+=size
 return out
def create_delta(original,patched,proof):
 d={'version':1,'container':proof['container'],'original_sha256':sha(original),'patched_sha256':sha(patched),'original_bytes':len(original),'patched_bytes':len(patched),'changes':[]}
 if d['container']=='zstd':
  a=frames(original);b=frames(patched);assert len(a)==len(b);d['frame_count']=len(a)
  for i,(x,y) in enumerate(zip(a,b)):
   assert x['decoded_length']==y['decoded_length'];old=original[x['offset']:x['offset']+x['length']];new=patched[y['offset']:y['offset']+y['length']]
   if old!=new:d['changes'].append({'frame_index':i,'original_offset':x['offset'],'patched_offset':y['offset'],'original_length':len(old),'patched_length':len(new),'original_header_hex':old[:18].hex(),'patched_header_hex':new[:18].hex(),'patched_frame_sha256':sha(new),'original_frame_base64':base64.b64encode(old).decode()})
 elif d['container']=='raw':
  for start,end in proof['authorized_ranges']:
   if original[start:end]!=patched[start:end]:d['changes'].append({'offset':start,'length':end-start,'patched_region_sha256':sha(patched[start:end]),'original_region_base64':base64.b64encode(original[start:end]).decode()})
 else:d['whole_original_base64']=base64.b64encode(original).decode()
 assert restore(patched,d)==original,'Delta exact restoration failed';return d
def restore(patched,d):
 assert sha(patched)==d['patched_sha256'],'Unexpected changed file; do not overwrite newer edits'
 if d['container']=='zstd':
  f=frames(patched);assert len(f)==d['frame_count'];changes={x['frame_index']:x for x in d['changes']};out=[]
  for i,item in enumerate(f):
   block=patched[item['offset']:item['offset']+item['length']]
   if i in changes:
    x=changes[i];assert item['offset']==x['patched_offset'] and len(block)==x['patched_length'] and sha(block)==x['patched_frame_sha256'];block=base64.b64decode(x['original_frame_base64']);assert len(block)==x['original_length'] and block[:18].hex()==x['original_header_hex']
   out.append(block)
  result=b''.join(out)
 elif d['container']=='raw':
  result=bytearray(patched)
  for x in d['changes']:
   a=x['offset'];z=a+x['length'];assert sha(patched[a:z])==x['patched_region_sha256'];result[a:z]=base64.b64decode(x['original_region_base64'])
  result=bytes(result)
 else:result=base64.b64decode(d['whole_original_base64'])
 assert len(result)==d['original_bytes'] and sha(result)==d['original_sha256'];return result
def budget(original,container,ranges):
 if container=='zstd':
  chosen=[x for x in frames(original) if any(a<x['decoded_offset']+x['decoded_length'] and z>x['decoded_offset'] for a,z in ranges)];raw=sum(x['length'] for x in chosen);return {'original_payload_bytes_upper':raw,'delta_json_bytes_upper':((raw+2)//3)*4+len(chosen)*700+4096,'selected_frames_upper':len(chosen)}
 raw=len(original) if container=='gzip' else sum(z-a for a,z in ranges);return {'original_payload_bytes_upper':raw,'delta_json_bytes_upper':((raw+2)//3)*4+len(ranges)*300+4096,'selected_frames_upper':0}
