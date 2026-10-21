import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
for i in [0, 3, 5, 8, 9, 10, 12, 13, 14, 16, 17]:
    p = doc.paragraphs[i]
    print(f'=== P{i} ({p.text[:30]}) ===')
    if p._p.pPr is not None:
        print(p._p.pPr.xml)
    print('Runs font & rPr:')
    for r in p.runs[:3]:
        rPr_xml = r._r.rPr.xml if r._r.rPr is not None else 'None'
        print(f'   run "{r.text[:20]}": {rPr_xml}')
