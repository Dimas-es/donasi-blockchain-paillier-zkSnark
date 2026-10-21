import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
sec = doc.sections[0]
print('sec.different_first_page_header_footer:', sec.different_first_page_header_footer)
print('sec.header.is_linked_to_previous:', sec.header.is_linked_to_previous)
print('sec.first_page_header.is_linked_to_previous:', sec.first_page_header.is_linked_to_previous)

# Inspect sectPr XML in detail
import xml.etree.ElementTree as ET
root = ET.fromstring(sec._sectPr.xml)
for child in root:
    print('sectPr child:', child.tag, child.attrib)
