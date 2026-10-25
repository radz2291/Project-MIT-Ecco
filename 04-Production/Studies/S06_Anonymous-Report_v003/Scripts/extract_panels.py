"""Extract anonymous report graphics. Never copy the full report into the deliverable."""
from pathlib import Path
import json,hashlib
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ContentStream,NameObject
import pypdfium2 as pdfium
import pdfplumber
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2]
source=next((ROOT/'01-Brief').glob('MIVU*.pdf'))
reader=PdfReader(source);page=reader.pages[2]
stream=ContentStream(page.get_contents(),reader)
ops=(b'Tj',b'TJ',b"'",b'"')
removed=sum(op in ops for args,op in stream.operations)
stream.operations=[(args,op) for args,op in stream.operations if op not in ops]
page[NameObject('/Contents')]=stream
writer=PdfWriter();writer.add_page(page)
clean=B/'Cache/text-free-page.pdf'
with clean.open('wb') as f:writer.write(f)
assert not PdfReader(clean).pages[0].extract_text().strip()
doc=pdfium.PdfDocument(str(clean));p=doc[0];w,h=p.get_size()
# Rectangles are page coordinates, top-left origin. Crop all headings, scales and footers.
regions={'shape':(318,272,415,500),'geometry':(426,272,515,500),'amplitude':(722,272,811,500),'sections':(195,205,309,450),'profile':(83,272,150,500)}
results=[]
for name,(x0,y0,x1,y1) in regions.items():
    im=p.render(scale=4,crop=(x0,h-y1,w-x1,y0)).to_pil().convert('RGB')
    path=B/f'Media/{name}.png';im.save(path)
    results.append({'panel':name,'crop_page_coordinates':[x0,y0,x1,y1],'size':list(im.size),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(B/'Records/crop-provenance.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_page_index':2,'text_show_operations_removed':removed,'stripped_pdf_text_empty':True,'panels':results,'authorization':'Direct owner Option C ending revision; anonymous graphic excerpts only; local review','same_dataset_as_illustrative_unfolding':False,'source_text_and_source_metadata_in_delivered_images':False},indent=2),encoding='utf-8')
print('Extracted',len(results),'graphic regions; stripped',removed,'text operations; text extraction empty')
