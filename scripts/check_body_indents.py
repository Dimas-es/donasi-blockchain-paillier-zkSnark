import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
for i in [17, 18, 19, 24, 26, 28, 30, 32]:
    p = doc.paragraphs[i]
    pPr = p._p.pPr
    ind = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ind') if pPr is not None else None
    spacing = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}spacing') if pPr is not None else None
    
    ind_left = ind.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left') if ind is not None else None
    ind_right = ind.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}right') if ind is not None else None
    ind_fl = ind.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}firstLine') if ind is not None else None
    
    line = spacing.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}line') if spacing is not None else None
    
    print(f'P{i:2d} | ind=(L:{ind_left}, R:{ind_right}, FL:{ind_fl}) | line={line} | text="{p.text[:40]}"')
