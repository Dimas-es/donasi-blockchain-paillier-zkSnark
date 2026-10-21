import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
for i in [8, 9, 10, 12, 13, 14, 16, 17]:
    p = doc.paragraphs[i]
    print(f'=== P{i} ({p.text[:40]}) ===')
    pPr = p._p.pPr
    if pPr is not None:
        for ch in pPr:
            print(f'  tag: {ch.tag.split("}")[-1]}, attrib: {ch.attrib}')
