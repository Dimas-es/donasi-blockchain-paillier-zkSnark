import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
body = doc._body._element
sdt = body[148]
for p in sdt.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    text = ''.join(p.itertext())
    print(f'Bib entry: "{text[:80]}"')
    pPr = p.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
    if pPr is not None:
        ind = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ind')
        spacing = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}spacing')
        print('  ind:', ind.attrib if ind is not None else None)
        print('  spacing:', spacing.attrib if spacing is not None else None)
