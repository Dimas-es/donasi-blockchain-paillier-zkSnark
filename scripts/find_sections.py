import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
print('Num sections:', len(doc.sections))
for idx, sec in enumerate(doc.sections):
    print(f'Section {idx}: start_type={sec.start_type}')

# Check where sectPr appears in body
body = doc._body._element
for i, el in enumerate(body):
    if el.tag.endswith('p'):
        # Check if p has sectPr
        pPr = el.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
        if pPr is not None:
            sectPr = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sectPr')
            if sectPr is not None:
                p_text = ''.join([t.text for t in el.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')])
                print(f'Paragraph {i} has sectPr! Text: "{p_text[:50]}"')
    elif el.tag.endswith('sectPr'):
        print(f'Body element {i} is sectPr (end of document)')
