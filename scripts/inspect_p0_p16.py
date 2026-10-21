import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
for i in range(17):
    p = doc.paragraphs[i]
    print(f'P{i} [{p.style.name}]: text="{p.text}"')
    print(f'   align={p.alignment}, left={p.paragraph_format.left_indent}, right={p.paragraph_format.right_indent}, first_line={p.paragraph_format.first_line_indent}, ls={p.paragraph_format.line_spacing}, sb={p.paragraph_format.space_before}, sa={p.paragraph_format.space_after}')
    runs_info = [(r.text[:20], r.font.name, r.font.size.pt if r.font.size else None, r.bold, r.italic, r.font.superscript, r.font.color.rgb if r.font.color else None) for r in p.runs[:5]]
    print(f'   runs: {runs_info}')
