import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
sec = doc.sections[0]
print('sectPr XML:')
print(sec._sectPr.xml)
