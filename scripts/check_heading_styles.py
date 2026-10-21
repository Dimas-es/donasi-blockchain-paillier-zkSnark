import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
h1_style = doc.styles['Heading 1']
h2_style = doc.styles['Heading 2']

print('Heading 1 style pPr XML:')
if h1_style._element.pPr is not None:
    print(h1_style._element.pPr.xml)
else:
    print('None')

print('\nHeading 2 style pPr XML:')
if h2_style._element.pPr is not None:
    print(h2_style._element.pPr.xml)
else:
    print('None')
