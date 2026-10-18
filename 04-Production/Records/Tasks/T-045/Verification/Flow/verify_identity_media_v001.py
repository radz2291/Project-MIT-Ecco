"""Independent exact-candidate identity, evidence timing and full video decode."""
from pathlib import Path
import subprocess,json,hashlib,re
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[6];OUT=Path(__file__).resolve().parent
SHA='974f138a9634965254dd58ca8a6cb30fb623bfde'
def digest(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
files=git('ls-tree','-r','--name-only',SHA,'04-Production/Shared/Assets/Hydraulics','04-Production/Records/Tasks/T-048').decode().splitlines()
checks=[]
for name in files:
    committed=git('show',SHA+':'+name);local=(ROOT/name).read_bytes()
    # Git may normalize working-tree text line endings; compare canonical content too.
    exact=local==committed;normalized=local.replace(b'\r\n',b'\n')==committed.replace(b'\r\n',b'\n')
    assert exact or normalized,name
    checks.append(dict(path=name,committed_sha256=digest(committed),local_sha256=digest(local),byte_equal=exact,line_endings_only=not exact and normalized))
manifest=json.loads((ROOT/'04-Production/Shared/Assets/Hydraulics/manifest_v002.json').read_text())
hashes=[]
for rec in manifest['native']+manifest['dependencies']+manifest['approval_images']+[manifest['behavior_demo']]:
    p=ROOT/rec['path'];sha=digest(p.read_bytes());assert sha==rec['sha256'] and p.stat().st_size==rec['bytes'],rec['path']
    hashes.append(dict(path=rec['path'],bytes=p.stat().st_size,sha256=sha))
task=ROOT/'04-Production/Records/Tasks/T-048'
benchmark=json.loads((task/'Evidence/benchmark_v007.json').read_text());batch=json.loads((task/'Evidence/batch_B_v007.json').read_text())
assert len(benchmark['renders'])==6 and len(batch['renders'])==96
assert [x['frame'] for x in batch['renders']]==list(range(1,97))
for rec in benchmark['renders']+batch['renders']:
    assert 0<rec['seconds']<5 and rec['under_5'];assert digest((ROOT/rec['output']).read_bytes())==rec['sha256']
video=ROOT/manifest['behavior_demo']['path']
ff=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
probe=subprocess.run([str(ff),'-hide_banner','-i',str(video)],capture_output=True).stderr.decode(errors='replace')
result=subprocess.run([str(ff),'-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True)
assert not result.stderr,result.stderr
size=1280*720*3;assert len(result.stdout)==96*size
frames=[result.stdout[i*size:(i+1)*size] for i in range(96)]
raw_hashes=[digest(x) for x in frames];assert len(set(raw_hashes))==96
assert all(s in probe for s in ['1280x720','24 fps','h264','yuv420p','00:00:04.00']) and 'Audio:' not in probe
sheet=Image.new('RGB',(1280,810),(14,18,22));d=ImageDraw.Draw(sheet)
for i,f in enumerate([1,13,25,37,49,61,73,85,96]):
    im=Image.frombytes('RGB',(1280,720),frames[f-1]);im.thumbnail((422,238));x=(i%3)*426;y=(i//3)*270
    sheet.paste(im,(x,y+24));d.text((x+5,y+5),f'Encoded Flow B / frame {f:03d}',fill='white')
sheet.save(OUT/'decoded-chronology_v001.jpg',quality=94)
for f in [1,48,96]:Image.frombytes('RGB',(1280,720),frames[f-1]).save(OUT/f'decoded_B_{f:03d}_v001.png')
report=dict(candidate_sha=SHA,head=git('rev-parse','HEAD').decode().strip(),origin_main=git('rev-parse','origin/main').decode().strip(),fresh_remote=git('ls-remote','origin','refs/heads/main').decode().strip(),tracked_candidate_file_count=len(checks),tracked_working_copy_checks=checks,manifest_hashes=hashes,
    benchmark=dict(count=6,min_s=min(x['seconds'] for x in benchmark['renders']),max_s=max(x['seconds'] for x in benchmark['renders']),source_claim='recorded executor full-write operations, independently checked records+exact output hashes; no fresh render',cache=benchmark['cache'],known_limit=benchmark['known_limit']),
    batch=dict(count=96,min_s=min(x['seconds'] for x in batch['renders']),max_s=max(x['seconds'] for x in batch['renders']),summed_s=sum(x['seconds'] for x in batch['renders']),all_output_hashes_match=True),
    decode=dict(video_sha256=digest(video.read_bytes()),complete_error_free=True,frames=96,dimensions=[1280,720],fps=24,duration_s=4,codec='h264',pixel_format='yuv420p',audio=False,distinct_raw_frames=len(set(raw_hashes)),raw_frame_sha256=raw_hashes,probe=probe))
(OUT/'identity-media-check_v001.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(pass_checks=True,tracked=len(checks),manifest_files=len(hashes),decoded_frames=96,timings=[report['batch']['min_s'],report['batch']['max_s']])))
