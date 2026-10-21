import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
for i in range(18):
    p = doc.paragraphs[i]
    pPr = p._p.pPr
    spacing = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}spacing') if pPr is not None else None
    ind = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ind') if pPr is not None else None
    jc = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}jc') if pPr is not None else None
    
    sp_before = spacing.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}before') if spacing is not None else None
    sp_after = spacing.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}after') if spacing is not None else None
    line = spacing.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}line') if spacing is not None else None
    
    ind_left = ind.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left') if ind is not None else None
    ind_right = ind.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}right') if ind is not None else None
    ind_fl = ind.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}firstLine') if ind is not None else None
    ind_hang = ind.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hanging') if ind is not None else None
    
    align = jc.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if jc is not None else None
    
    words = len(p.text.split())
    print(f'P{i:2d} | words={words:3d} | style={p.style.name:15} | align={align} | line={line} | sb={sp_before} | sa={sp_after} | ind=(L:{ind_left}, R:{ind_right}, FL:{ind_fl}, H:{ind_hang}) | text="{p.text[:45]}"')
