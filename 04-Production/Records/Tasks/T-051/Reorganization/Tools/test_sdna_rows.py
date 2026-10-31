import struct,json,pathlib
from blend_path_bytes import Blend,patch_bytes
def align(b):return b+b'\0'*((-len(b))%4)
names=align(b'name[2][16]\0filepath[16]\0');types=align(b'char\0Library\0');dna=b'SDNANAME'+struct.pack('<I',2)+names+b'TYPE'+struct.pack('<I',2)+types+b'TLEN'+struct.pack('<HH',1,48)+b'STRC'+struct.pack('<IHHHHHH',1,1,2,0,0,0,1)
def block(code,body,addr):return struct.pack('<4siQii',code,len(body),addr,0,1)+body
data=b'BLENDER-v300'+block(b'LI\0\0',b'//one\0'.ljust(16,b'\0')+b'//two\0'.ljust(16,b'\0')+b'//three\0'.ljust(16,b'\0'),4096)+block(b'DNA1',dna,8192)+struct.pack('<4siQii',b'ENDB',0,0,0,0)
b=Blend(data);paths=b.paths();assert [x['capacity'] for x in paths]==[16,16,16];patched,proof=patch_bytes(data,{paths[0]['offset']:'//changed'});after=Blend(patched).paths();assert [x['value'] for x in after]==['//changed','//two','//three']
try:patch_bytes(data,{paths[0]['offset']:'X'*16})
except AssertionError:overflow=True
else:overflow=False
assert overflow
result={'legacy_header_pass':True,'one_dimensional_char_array_pass':True,'two_dimensional_rows_independent':True,'row_overflow_rejected':overflow,'patch_proof':proof,'native_files_written':0};(pathlib.Path(__file__).parent.parent/'sdna-row-tests.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
