import docx
from docx.shared import Pt, Cm

doc = docx.Document('assets/jurnal/JURNAL_SIMASI_TRUSTGIVE.docx')

for i, p in enumerate(doc.paragraphs):
    if any(k in p.text for k in ['METODE PENELITIAN', '1. Arsitektur Hibrida', 'Penelitian ini dilaksanakan']):
        pf = p.paragraph_format
        left = pf.left_indent.pt if pf.left_indent else 'default (0)'
        fl = pf.first_line_indent.pt if pf.first_line_indent else 'default (0)'
        # Also check style indent
        s_ind = p.style._element.pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ind') if p.style._element.pPr is not None else None
        s_left = s_ind.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left') if s_ind is not None else 'None'
        print(f'P{i:2d} [{p.style.name:12}]: left={left}, fl={fl}, style_left={s_left} | text="{p.text[:40]}"')
