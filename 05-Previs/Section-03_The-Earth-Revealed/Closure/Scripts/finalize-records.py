from pathlib import Path
R=Path(__file__).resolve().parents[2]
for name in ['render-review.py','render-chunk.py']:
 p=R/'v036/Scripts'/name
 text=p.read_text(encoding='utf-8-sig')
 text=text.replace(",'storage_recovery':'Final96frames resumed with20MiB guard: one overwritten PNG, small h264 chunk, final stream-copy assembly; existing blocks decoded and reused.'",'')
 p.write_text(text.rstrip()+'\n',encoding='utf-8')
