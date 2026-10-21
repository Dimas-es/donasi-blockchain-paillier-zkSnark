import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')

print('=== PARAGRAPHS 0 to 22 IN TEMPLATE ===')
for i in range(23):
    p = doc.paragraphs[i]
    print(f'\n--- P{i} [Style: {p.style.name}] ---')
    print(f'Text: "{p.text}"')
    pPr = p._p.pPr
    pPr_xml = pPr.xml if pPr is not None else 'None'
    print(f'align={p.alignment}, left={p.paragraph_format.left_indent}, right={p.paragraph_format.right_indent}, first_line={p.paragraph_format.first_line_indent}, ls={p.paragraph_format.line_spacing}, sb={p.paragraph_format.space_before}, sa={p.paragraph_format.space_after}')
    for r_idx, r in enumerate(p.runs):
        color = r.font.color.rgb if r.font.color else 'None'
        print(f'   run {r_idx}: text="{r.text}", font={r.font.name}, sz={r.font.size.pt if r.font.size else None}, bold={r.bold}, italic={r.italic}, sup={r.font.superscript}, color={color}')
