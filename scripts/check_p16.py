import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
p16 = doc.paragraphs[16]
print('P16 text raw:', repr(p16.text))
print('P16 xml:', p16._p.xml)
