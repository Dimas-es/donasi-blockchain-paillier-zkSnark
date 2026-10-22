import os
import sys
import docx
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=50, bottom=50, left=70, right=70):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for border_name, border_style in borders.items():
        if border_style:
            el = OxmlElement(f'w:{border_name}')
            for k, v in border_style.items():
                el.set(qn(f'w:{k}'), str(v))
            tcBorders.append(el)
        else:
            el = OxmlElement(f'w:{border_name}')
            el.set(qn('w:val'), 'none')
            tcBorders.append(el)
    tcPr.append(tcBorders)

def force_black_color(run):
    run.font.color.rgb = RGBColor(0, 0, 0)
    rPr = run._r.get_or_add_rPr()
    color_el = rPr.find(qn('w:color'))
    if color_el is not None:
        color_el.set(qn('w:val'), 'auto')
    else:
        new_color = OxmlElement('w:color')
        new_color.set(qn('w:val'), 'auto')
        rPr.append(new_color)

def force_no_italic(run):
    run.font.italic = False
    rPr = run._r.get_or_add_rPr()
    i_el = rPr.find(qn('w:i'))
    if i_el is not None:
        i_el.set(qn('w:val'), '0')
    else:
        new_i = OxmlElement('w:i')
        new_i.set(qn('w:val'), '0')
        rPr.append(new_i)
    ics_el = rPr.find(qn('w:iCs'))
    if ics_el is not None:
        ics_el.set(qn('w:val'), '0')
    else:
        new_ics = OxmlElement('w:iCs')
        new_ics.set(qn('w:val'), '0')
        rPr.append(new_ics)

def build_manuscript():
    template_path = 'assets/template/TEMPLATE SIMASI CONTOH.docx'
    output_path = 'assets/jurnal/JURNAL_SIMASI_TRUSTGIVE.docx'
    
    doc = docx.Document(template_path)
    
    # 1. Section Setup (Margins: exactly 2.54 cm all sides - Letter size)
    # Clean template example dummy text from native headers while preserving formatting
    for sec in doc.sections:
        sec.top_margin = Cm(2.54)
        sec.bottom_margin = Cm(2.54)
        sec.left_margin = Cm(2.54)
        sec.right_margin = Cm(2.54)
        for p in sec.header.paragraphs:
            if "Vol." in p.text:
                p.text = "Jurnal Simasi : Jurnal Ilmiah Sistem Informasi\tVol. [x], No. [x], [Tahun] hal. 1-17"
                if p.runs:
                    p.runs[0].font.name = "Times New Roman"
                    p.runs[0].font.size = Pt(8)
            elif "DOI Issue" in p.text:
                p.text = "DOI Issue : [Diisi oleh Pengelola Jurnal]\tDOI Article : [Diisi oleh Pengelola Jurnal]"
                if p.runs:
                    p.runs[0].font.name = "Times New Roman"
                    p.runs[0].font.size = Pt(8)
    
    # 2. Preserve Table 0 (Kop table), delete all other body elements
    body = doc._body._element
    elements_to_remove = []
    for i in range(1, len(body)):
        child = body[i]
        if child.tag.endswith('sectPr'):
            continue
        elements_to_remove.append(child)
        
    for el in elements_to_remove:
        body.remove(el)
        
    print(f"Preserved Table 0 Kop. Removed {len(elements_to_remove)} old template elements.")
    
    # Preserve Table 0 (Kop Header) exactly as formatted in template
    t0 = doc.tables[0]
    t0.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # 3. Helper functions strictly mirroring TEMPLATE SIMASI CONTOH.docx
    def add_title(text):
        p = doc.add_paragraph(style='Title')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.right_indent = Pt(4.75) # 95 dxa as in template
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.bold = True
        force_black_color(r)
        return p

    def add_authors(author_list):
        p = doc.add_paragraph(style='Heading 2')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.right_indent = Pt(4.75)
        
        for i, (name, sup) in enumerate(author_list):
            r_name = p.add_run(name)
            r_name.font.name = 'Times New Roman'
            r_name.font.size = Pt(10)
            r_name.bold = True
            force_black_color(r_name)
            
            r_sup = p.add_run(sup)
            r_sup.font.name = 'Times New Roman'
            r_sup.font.size = Pt(10)
            r_sup.bold = True
            r_sup.font.superscript = True
            force_black_color(r_sup)
            
            if i < len(author_list) - 1:
                r_sep = p.add_run(", ")
                r_sep.font.name = 'Times New Roman'
                r_sep.font.size = Pt(10)
                r_sep.bold = True
                force_black_color(r_sep)
        return p

    def add_affiliation(text):
        p = doc.add_paragraph(style='Body Text')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.right_indent = Pt(4.75)
        
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        force_black_color(r)
        return p

    def add_email_formatted():
        p = doc.add_paragraph(style='Body Text')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.right_indent = Pt(4.75)
        
        r0 = p.add_run("Email: ")
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        force_black_color(r0)
        
        r1 = p.add_run("dimaasadjy@gmail.com")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        force_black_color(r1)
        
        s1 = p.add_run("1")
        s1.font.name = 'Times New Roman'
        s1.font.size = Pt(10)
        s1.font.superscript = True
        force_black_color(s1)
        
        r2 = p.add_run(", ")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        force_black_color(r2)
        
        r3 = p.add_run("alam@unsil.ac.id")
        r3.font.name = 'Times New Roman'
        r3.font.size = Pt(10)
        force_black_color(r3)
        
        s2 = p.add_run("2")
        s2.font.name = 'Times New Roman'
        s2.font.size = Pt(10)
        s2.font.superscript = True
        force_black_color(s2)
        return p

    def add_blank(space_pt=3):
        p = doc.add_paragraph(style='Body Text')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_pt)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.first_line_indent = Cm(0)
        return p

    def add_abstract_header(text, is_italic=False):
        # In template: align=CENTER, bold, italic for EN, normal for ID, ind=(L:426, R:146, H:33)
        p = doc.add_paragraph(style='Normal')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.left_indent = Pt(21.3)   # 426 dxa
        p.paragraph_format.right_indent = Pt(7.3)   # 146 dxa
        p.paragraph_format.first_line_indent = Pt(-1.65) # 33 dxa hanging
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.bold = True
        force_black_color(r)
        if is_italic:
            r.italic = True
        else:
            force_no_italic(r)
        return p

    def add_abstract_body(text, is_italic=False):
        # In template: align=JUSTIFY, ind=(L:426, R:146, H:33)
        p = doc.add_paragraph(style='Normal')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Pt(21.3)   # 426 dxa
        p.paragraph_format.right_indent = Pt(7.3)   # 146 dxa
        p.paragraph_format.first_line_indent = Pt(-1.65) # 33 dxa hanging
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        force_black_color(r)
        if is_italic:
            r.italic = True
        else:
            force_no_italic(r)
        return p

    def add_keywords(label, kw_text, is_italic=False):
        p = doc.add_paragraph(style='Normal')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Pt(21.3)
        p.paragraph_format.right_indent = Pt(7.3)
        p.paragraph_format.first_line_indent = Pt(-1.65)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.0
        
        r1 = p.add_run(label + ' ')
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        r1.bold = True
        force_black_color(r1)
        if is_italic:
            r1.italic = True
        else:
            force_no_italic(r1)
            
        r2 = p.add_run(kw_text)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        force_black_color(r2)
        if is_italic:
            r2.italic = True
        else:
            force_no_italic(r2)
        return p

    def add_h1(text):
        # Main section headings in template: Heading 1, 12pt Bold, Left-aligned, ALL CAPS, sb=162 dxa (8pt)
        p = doc.add_paragraph(style='Heading 1')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Pt(26.5)       # 530 dxa (align with template body text)
        p.paragraph_format.right_indent = Pt(31.8)      # 637 dxa
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Cm(0)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        force_black_color(r)
        force_no_italic(r)
        return p

    def add_h2(text):
        # Subheadings in template: Heading 2, 12pt Bold Title Case, Left-aligned
        p = doc.add_paragraph(style='Heading 2')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Pt(26.5)       # 530 dxa (flush with Heading 1 and Body Text)
        p.paragraph_format.right_indent = Pt(31.8)      # 637 dxa
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Cm(0)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        force_black_color(r)
        force_no_italic(r)
        return p

    def parse_markdown_runs(text):
        runs = []
        i = 0
        n = len(text)
        buf = ''
        while i < n:
            if text[i:i+3] == '***':
                if buf:
                    runs.append((buf, False, False))
                    buf = ''
                end = text.find('***', i+3)
                if end != -1:
                    runs.append((text[i+3:end], True, True))
                    i = end + 3
                    continue
            elif text[i:i+2] == '**':
                if buf:
                    runs.append((buf, False, False))
                    buf = ''
                end = text.find('**', i+2)
                if end != -1:
                    runs.append((text[i+2:end], True, False))
                    i = end + 2
                    continue
            elif text[i] == '*':
                if buf:
                    runs.append((buf, False, False))
                    buf = ''
                end = text.find('*', i+1)
                if end != -1:
                    runs.append((text[i+1:end], False, True))
                    i = end + 1
                    continue
            buf += text[i]
            i += 1
        if buf:
            runs.append((buf, False, False))
        return runs

    def add_body_p(text):
        # Body text in template: Body Text, Justified, 1.5 line spacing (line=360),
        # ind=(L:530 dxa, R:637 dxa, FL:676 dxa), sb=137 dxa (~7 pt)
        p = doc.add_paragraph(style='Body Text')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Pt(26.5)       # 530 dxa
        p.paragraph_format.right_indent = Pt(31.8)      # 637 dxa
        p.paragraph_format.first_line_indent = Pt(33.8) # 676 dxa
        p.paragraph_format.space_before = Pt(6)         # 137 dxa
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.5
        
        runs = parse_markdown_runs(text)
        for t, is_bold, is_italic in runs:
            r = p.add_run(t)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            force_black_color(r)
            if is_bold:
                r.bold = True
            if is_italic:
                r.italic = True
            else:
                force_no_italic(r)
        return p

    def add_list_item(num_prefix, text, level=1):
        # List items in template: List Paragraph, hanging indent, 1.5 line spacing
        p = doc.add_paragraph(style='List Paragraph')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Pt(40.7 if level == 1 else 54.9) # Base 26.5 pt + 14.2 pt hanging
        p.paragraph_format.right_indent = Pt(31.8)
        p.paragraph_format.first_line_indent = Pt(-14.2)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.5
            
        r_num = p.add_run(num_prefix + ' ')
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(12)
        r_num.bold = False
        force_black_color(r_num)
        force_no_italic(r_num)
        
        runs = parse_markdown_runs(text)
        for t, is_bold, is_italic in runs:
            r = p.add_run(t)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            force_black_color(r)
            if is_bold:
                r.bold = True
            if is_italic:
                r.italic = True
            else:
                force_no_italic(r)
        return p

    def add_figure(img_rel_path, caption_text, width_cm=14.0):
        # Figure in template: Centered image, followed by Centered 12pt Caption below image
        if os.path.exists(img_rel_path):
            p_img = doc.add_paragraph(style='Body Text')
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.first_line_indent = Cm(0)
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.line_spacing = 1.0
            p_img.paragraph_format.keep_with_next = True
            r = p_img.add_run()
            r.add_picture(img_rel_path, width=Cm(width_cm))
            
            p_cap = doc.add_paragraph(style='Caption')
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(3)
            p_cap.paragraph_format.space_after = Pt(8)
            p_cap.paragraph_format.line_spacing = 1.15
            p_cap.paragraph_format.first_line_indent = Cm(0)
            
            dot_idx = caption_text.find('.')
            if dot_idx != -1 and caption_text[:dot_idx].lower().startswith('gambar'):
                bold_prefix = caption_text[:dot_idx+1]
                norm_desc = caption_text[dot_idx+1:]
                
                r_bold = p_cap.add_run(bold_prefix)
                r_bold.font.name = 'Times New Roman'
                r_bold.font.size = Pt(12)
                r_bold.bold = True
                force_black_color(r_bold)
                force_no_italic(r_bold)
                
                r_norm = p_cap.add_run(norm_desc)
                r_norm.font.name = 'Times New Roman'
                r_norm.font.size = Pt(12)
                r_norm.bold = False
                force_black_color(r_norm)
                force_no_italic(r_norm)
            else:
                r_cap = p_cap.add_run(caption_text)
                r_cap.font.name = 'Times New Roman'
                r_cap.font.size = Pt(12)
                r_cap.bold = True
                force_black_color(r_cap)
                force_no_italic(r_cap)
        else:
            print(f"WARNING: Image not found: {img_rel_path}")

    def add_custom_table(caption_text, headers, rows_data, col_widths=None, aligns=None, font_size_pt=9.5):
        # Table in template: Centered Caption ABOVE table in 12pt (Tabel X. Bold), Plain Table 2 (Clean black borders, NO grey fill)
        p_cap = doc.add_paragraph(style='Caption')
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(8)
        p_cap.paragraph_format.space_after = Pt(3)
        p_cap.paragraph_format.line_spacing = 1.15
        p_cap.paragraph_format.first_line_indent = Cm(0)
        p_cap.paragraph_format.keep_with_next = True
        
        dot_idx = caption_text.find('.')
        if dot_idx != -1 and caption_text[:dot_idx].lower().startswith('tabel'):
            bold_prefix = caption_text[:dot_idx+1]
            norm_desc = caption_text[dot_idx+1:]
            
            r_bold = p_cap.add_run(bold_prefix)
            r_bold.font.name = 'Times New Roman'
            r_bold.font.size = Pt(12)
            r_bold.bold = True
            force_black_color(r_bold)
            force_no_italic(r_bold)
            
            r_norm = p_cap.add_run(norm_desc)
            r_norm.font.name = 'Times New Roman'
            r_norm.font.size = Pt(12)
            r_norm.bold = False
            force_black_color(r_norm)
            force_no_italic(r_norm)
        else:
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(12)
            r_cap.bold = True
            force_black_color(r_cap)
            force_no_italic(r_cap)
            
        num_rows = len(rows_data) + 1
        num_cols = len(headers)
        
        table = doc.add_table(rows=num_rows, cols=num_cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Plain Table 2 Style: Clean APA/scientific lines (top border, header-bottom border, table-bottom border)
        border_top = {'val': 'single', 'sz': '8', 'space': '0', 'color': '000000'}
        border_mid = {'val': 'single', 'sz': '8', 'space': '0', 'color': '000000'}
        border_bot = {'val': 'single', 'sz': '8', 'space': '0', 'color': '000000'}
        
        # Header Row
        hdr_row = table.rows[0]
        hdr_row._tr.get_or_add_trPr().append(parse_xml(r'<w:tblHeader xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))
        for col_idx, h_text in enumerate(headers):
            cell = hdr_row.cells[col_idx]
            cell.text = h_text
            p = cell.paragraphs[0]
            p.alignment = aligns[col_idx] if aligns and col_idx < len(aligns) else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.first_line_indent = Cm(0)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(font_size_pt)
                r.bold = True
                force_black_color(r)
                force_no_italic(r)
            set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
            set_cell_borders(cell, top=border_top, bottom=border_mid)
            
        # Data Rows
        for row_idx, r_data in enumerate(rows_data):
            row = table.rows[row_idx + 1]
            is_last = (row_idx == len(rows_data) - 1)
            for col_idx, cell_value in enumerate(r_data):
                cell = row.cells[col_idx]
                cell.text = ''
                p = cell.paragraphs[0]
                p.alignment = aligns[col_idx] if aligns and col_idx < len(aligns) else WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(1.5)
                p.paragraph_format.space_after = Pt(1.5)
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.first_line_indent = Cm(0)
                
                runs = parse_markdown_runs(str(cell_value))
                for t, is_bold, is_italic in runs:
                    r = p.add_run(t)
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(font_size_pt - 0.5)
                    force_black_color(r)
                    if is_bold:
                        r.bold = True
                    if is_italic:
                        r.italic = True
                    else:
                        force_no_italic(r)
                set_cell_margins(cell, top=30, bottom=30, left=50, right=50)
                if is_last:
                    set_cell_borders(cell, bottom=border_bot)
                else:
                    set_cell_borders(cell)
                    
        for row in table.rows:
            row._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))

        if col_widths:
            for row in table.rows:
                for idx, w in enumerate(col_widths):
                    if idx < len(row.cells):
                        row.cells[idx].width = w

    print("Assembling revised manuscript content strictly following SIMASI template...")
    
    # 4. Add Title, Authors, Affiliation, Email
    p_t1 = doc.add_paragraph(style='Title')
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(6)
    p_t1.paragraph_format.space_after = Pt(0)
    p_t1.paragraph_format.line_spacing = 1.15
    p_t1.paragraph_format.first_line_indent = Cm(0)
    p_t1.paragraph_format.right_indent = Pt(4.75)
    r1 = p_t1.add_run("STUDI DESAIN DAN EVALUASI KINERJA PROTOTIPE SISTEM DONASI TERDESENTRALISASI HIBRIDA")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(14)
    r1.bold = True
    force_black_color(r1)

    p_t2 = doc.add_paragraph(style='Title')
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.space_before = Pt(0)
    p_t2.paragraph_format.space_after = Pt(4)
    p_t2.paragraph_format.line_spacing = 1.15
    p_t2.paragraph_format.first_line_indent = Cm(0)
    p_t2.paragraph_format.right_indent = Pt(4.75)
    r2 = p_t2.add_run("MENGGUNAKAN PAILLIER DAN ZK-SNARK GROTH16 (TRUSTGIVE)")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)
    r2.bold = True
    force_black_color(r2)
    
    add_authors([
        ("Dimas Setiawan", "1"),
        ("Alam Rahmatulloh", "2")
    ])
    
    add_affiliation("1,2 Program Studi Informatika, Fakultas Teknik, Universitas Siliwangi, Tasikmalaya, Indonesia")
    add_email_formatted()
    add_blank(space_pt=3)
    
    # 5. Abstract (English) - Exactly ~140 words to fit Page 1 perfectly
    add_abstract_header("ABSTRACT", is_italic=True)
    add_abstract_body(
        "Public philanthropic platforms face a persistent tension between public auditability and donors' financial privacy. "
        "While blockchain ledgers offer tamper-resistant donation records, publishing plaintext donation amounts triggers "
        "financial profiling and deanonymization risks. This paper presents the design and empirical evaluation of TrustGive, "
        "a hybrid decentralized donation prototype integrating Paillier Additive Homomorphic Encryption (AHE), Groth16 zk-SNARK, "
        "and Ethereum smart contracts. Individual donations are encrypted off-chain via Paillier and aggregated through modular multiplication, "
        "while range validity is verified on-chain via zero-knowledge proofs over the BN254 curve without exposing plaintext values. "
        "Empirical evaluations on the prototype show that standalone Groth16 verification consumes 225,035 gas, while on-chain recording under "
        "the current decimal string payload consumes 1,481,734 gas (959,465 gas for binary and 613,627 gas for compact payloads, reduced to "
        "382,632 gas via the implemented event-log hash storage optimization). Off-chain addition takes 0.013 ms (~79,100 op/s) and in-process Groth16 proof generation requires 212.18 ms (median 189.56 ms, steady-state 194.58 ms), achieving a responsive in-process sequential end-to-end "
        "latency of ~240.5 ms (steady-state median, <0.25 s; ~248.8 ms mean) under a delegated honest-but-curious server model.",
        is_italic=True
    )
    add_keywords("Keywords:", "Decentralized Donation, Paillier Homomorphic Encryption, zk-SNARK, Groth16, Smart Contract, Blockchain Privacy, Threat Model.", is_italic=True)
    add_blank(space_pt=2)
    
    # 6. Abstrak (Bahasa Indonesia) - Exactly ~138 words to fit Page 1 perfectly
    add_abstract_header("ABSTRAK", is_italic=False)
    add_abstract_body(
        "Platform filantropi publik menghadapi ketegangan antara transparansi audit publik dan privasi finansial donatur. "
        "Pencatatan transaksi pada blockchain publik menyediakan auditabilitas permanen, namun memublikasikan nominal donasi secara "
        "terbuka (plaintext) memicu risiko pemrofilan finansial dan deanonimisasi. Penelitian ini menyajikan perancangan dan evaluasi kinerja "
        "TrustGive, prototipe sistem donasi terdesentralisasi hibrida yang mengintegrasikan Additive Homomorphic Encryption (AHE) Paillier, "
        "zk-SNARK Groth16, dan kontrak pintar Ethereum. Nilai donasi dienkripsi secara off-chain dengan Paillier dan diakumulasikan melalui "
        "perkalian modular, sedangkan keabsahan nominal diverifikasi secara on-chain menggunakan bukti ZK pada kurva BN254 tanpa membocorkan "
        "nilai rahasia. Pengujian empiris pada prototipe menunjukkan verifikasi Groth16 mandiri mengonsumsi 225.035 gas, sedangkan pencatatan on-chain "
        "dengan muatan string desimal saat ini memerlukan 1.481.734 gas (959.465 gas untuk muatan biner dan 613.627 gas untuk muatan ringkas, "
        "dan terpangkas menjadi 382.632 gas melalui optimasi penyimpanan hash dan event log). Agregasi off-chain memerlukan 0,013 ms (~79.100 op/detik) dan pembentukan bukti ZK in-process memerlukan 212,18 ms (median 189,56 ms, kondisi stabil 194,58 ms), menghasilkan "
        "estimasi latensi sekuensial end-to-end responsif sebesar ~240,5 ms (median kondisi stabil, <0,25 detik; ~248,8 ms rata-rata) di bawah model server terdelegasi honest-but-curious.",
        is_italic=False
    )
    add_keywords("Kata kunci:", "Donasi Terdesentralisasi, Enkripsi Homomorfik Paillier, zk-SNARK, Groth16, Kontrak Pintar, Privasi Blockchain, Model Ancaman.", is_italic=False)
    add_blank(space_pt=3)
    
    # 7. PENDAHULUAN - Paragraph 1 begins on Page 1!
    add_h1("PENDAHULUAN")
    add_body_p(
        "Aktivitas filantropi dan penggalangan dana publik (*crowdfunding*) berbasis digital telah berkembang pesat sebagai instrumen "
        "redistribusi sumber daya sosial ekonomi masyarakat modern (Unsal, 2025). Kendati demikian, sektor filantropi konvensional secara konsisten "
        "menghadapi krisis kepercayaan publik (*trust deficit*) yang diakibatkan oleh kurangnya transparansi pencatatan, tingginya biaya perantara "
        "administratif, serta kerentanan manipulasi pelaporan keuangan oleh entitas pengelola terpusat (Nairi dkk., 2024). Munculnya teknologi buku "
        "besar terdistribusi (*distributed ledger technology* / blockchain) menawarkan paradigma baru dalam akuntabilitas donasi digital, di mana "
        "setiap transaksi dicatat secara permanen, dapat diaudit oleh publik, dan dieksekusi secara deterministik oleh kontrak pintar (*smart contracts*) "
        "tanpa bergantung pada perantara tunggal (Almaghrabi & Alhogail, 2022; Saraswat dkk., 2022)."
    )
    
    add_body_p(
        "Namun demikian, transparansi absolut yang inheren pada jaringan blockchain publik memicu paradoks privasi yang serius. "
        "Setiap data transaksi finansial yang dipublikasikan secara terbuka (*plaintext*) ke dalam buku besar publik memungkinkan pihak ketiga "
        "melakukan analisis grafik transaksi, penelusuran identitas (*deanonymization*), hingga pemrofilan status ekonomi donatur secara tidak etis "
        "(Bünz dkk., 2020). Donatur yang menyumbangkan dana dalam nominal besar rentan menjadi target eksploitasi finansial dan kejahatan siber, "
        "sementara donatur yang menyumbang dalam jumlah kecil dapat merasa enggan berpartisipasi akibat stigma sosial dan ketimpangan eksposur finansial "
        "(Zhou dkk., 2024). Di samping itu, prinsip perlindungan data pribadi seperti yang digariskan dalam *General Data Protection Regulation* (GDPR) (Babel & Sedlmeir, 2023) "
        "maupun regulasi nasional di Indonesia, yaitu **Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP)** (Republik Indonesia, 2022), "
        "mendorong penerapan prinsip minimisasi data (*data minimization*) terhadap publikasi data finansial yang tidak perlu. Dalam konteks blockchain publik di mana "
        "data bersifat permanen dan transparan, arsitektur sistem informasi filantropi modern terdorong untuk mengeksplorasi batas kompromi antara auditabilitas "
        "komitmen donasi dan perlindungan kerahasiaan nominal donasi individual dari pengamatan publik terbuka (Wang dkk., 2023)."
    )
    
    add_body_p(
        "Untuk menjawab tantangan tersebut, berbagai penelitian mengusulkan teknik kriptografi privasi seperti enkripsi homomorfik (*Homomorphic Encryption* / HE) "
        "dan pembuktian tanpa pengetahuan (*Zero-Knowledge Proofs* / ZKP) (Lavin dkk., 2024; Sameera dkk., 2024; Burgos & Alchieri, 2025). Kriptosistem Paillier "
        "merupakan skema enkripsi asimetris dengan sifat homomorfik aditif (*Additive Homomorphic Encryption* / AHE), di mana perkalian antara dua *ciphertext* "
        "pada ruang modulus n² secara matematis menghasilkan enkripsi dari penjumlahan nilai *plaintext*-nya tanpa membuka isi pesan (Paillier, 1999; Yang dkk., 2023; Damle dkk., 2021). "
        "Sifat ini memungkinkan akumulasi saldo donasi kampanye secara inkremental tanpa mendekripsi masing-masing sumbangan. Sementara itu, zk-SNARK protokol Groth16 "
        "(Groth, 2016) memungkinkan pembuktian keabsahan suatu pernyataan komputasi—seperti nominal donasi berakar pada rentang positif dan tidak melampaui pagu kampanye—secara "
        "ringkas (*succinct*) dan terverifikasi secara on-chain tanpa membocorkan nilai rahasia (Christ dkk., 2024; Morais dkk., 2020)."
    )
    
    add_body_p(
        "Kombinasi antara HE dan zk-SNARK pada kontrak pintar telah dieksplorasi secara teoretis dalam beberapa literatur, seperti protokol ZeeStar (Steffen dkk., 2022) "
        "dan Cloak (Ren dkk., 2021). Namun, implementasi praktis sistem donasi terdesentralisasi yang mengintegrasikan kedua teknik ini pada arsitektur perangkat lunak "
        "dunia nyata menghadapi sejumlah tantangan berat:"
    )
    
    add_list_item("1.", "**Beban Komputasi On-Chain:** Mengeksekusi pembuktian dan agregasi seutuhnya di atas EVM (*fully on-chain*) sangat mahal dalam konsumsi gas dan latensi (Habib, 2025; Quintero-Narvaez dkk., 2023).")
    add_list_item("2.", "**Kegagalan Konsistensi Data (Dual-Write Problem):** Memindahkan beban komputasi ke ranah off-chain menimbulkan risiko desinkronisasi antara status basis data relasional dan status transaksi blockchain saat terjadi gangguan jaringan (*RPC timeout* atau kegagalan transaksi) (Zhang dkk., 2019).")
    add_list_item("3.", "**Kesenjangan Pengikatan Kriptografis (Binding Gap):** Paillier dengan modulus 2048-bit memiliki ukuran modulus yang besar sehingga memerlukan dekomposisi non-native field pada sirkuit SNARK berbasis kurva BN254. Mengintegrasikan bukti ZK dengan *ciphertext* Paillier secara terpisah rentan menyisakan celah substitusi nilai jika tidak diikat secara kriptografis (Chaliasos dkk., 2024).")
    
    add_body_p(
        "Beberapa sistem donasi berbasis blockchain terdahulu telah diusulkan dalam literatur, antara lain UpHaaR (Saraswat dkk., 2022), Astraea (Li dkk., 2023), "
        "He dkk. (2024), Eisdspa (Zhou dkk., 2024), dan ZeeStar (Steffen dkk., 2022). Tabel 1 merangkum perbandingan komparatif berbasis properti teknis antara sistem-sistem tersebut dengan prototipe TrustGive."
    )
    
    # Table 1: Comparative Table
    tbl1_headers = ["Sistem / Literatur", "Kerahasiaan Nominal Operator", "Verifikasi Publik Total", "Anonimitas Donatur On-Chain", "Kelas Beban Gas EVM (Kualitatif)", "Asumsi Kepercayaan / Setup", "Metodologi Evaluasi Gas & Rujukan"]
    tbl1_rows = [
        ["**UpHaaR**", "Tidak (Plaintext)", "Ya (On-chain state)", "Rendah (Alamat wallet publik)", "Minimal (<50.000 gas)", "Konsorsium semi-tepercaya; IPFS hash", "Saraswat dkk. (2022), hal. 103245 (Geth private network)"],
        ["**Astraea**", "Ya (Relayer ZK)", "Ya (Kontrak privat)", "Tinggi (Linkable ring signature)", "Sangat Tinggi (>1.200.000 gas)", "Trusted setup SNARK; relayer pool", "Li dkk. (2023), hal. 3008 (Geth v1.9.25)"],
        ["**He dkk.**", "Ya (SE index)", "Tidak (Rekonstruksi server)", "Sedang (Tersamarkan indeks)", "Sedang (~120.000 gas)", "Server indeks pencarian tepercaya", "He dkk. (2024), hal. 2980 (Rinkeby testnet)"],
        ["**Eisdspa**", "Ya (Pedersen)", "Ya (Penjumlahan homomorfik)", "Tinggi (Linkable ring signature)", "Tinggi (~650.000 gas)", "Kurva eliptik standar; tanpa trusted setup", "Zhou dkk. (2024), hal. 7502 (Geth v1.10.2)"],
        ["**ZeeStar**", "Ya (ElGamal)", "Terbatas (BSGS ≤ 2⁴⁰)", "Rendah / Standar (Pseudonim EVM)", "Sedang (~339.000 gas)", "Circuit-specific CRS setup (Groth16); ZK verifier", "Steffen dkk. (2022), hal. 949 (EVM Istanbul)"],
        ["**TrustGive** *(Prototipe ini)*", "Tidak (Delegated Prover)", "Terbatas (Opening (M, R) teruji di modul; persistensi DB dirancang)", "Relayer Server (Terselubung off-chain)", "Sedang s.d. Tinggi (382.632 – 1.481.734 gas)", "Single-party Groth16 setup; server HbC", "Penelitian ini (Hardhat EVM Cancun ^0.8.28; 225k pairing check + SSTORE muatan; 382k via event log)"]
    ]
    tbl1_widths = [Cm(1.8), Cm(2.1), Cm(2.0), Cm(2.2), Cm(2.3), Cm(2.8), Cm(3.2)]
    tbl1_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    add_custom_table("Tabel 1. Tinjauan Komparatif Properti Sistem Donasi Terdesentralisasi Terkait", tbl1_headers, tbl1_rows, tbl1_widths, tbl1_aligns, font_size_pt=8.0)
    
    add_body_p(
        "*Catatan Metodologis: Perbandingan biaya gas disajikan secara kualitatif-komparatif berdasarkan kelas beban eksekusi on-chain yang dilaporkan pada masing-masing literatur dengan versi simpul/testbed yang berbeda (UpHaaR: private network; Astraea: Geth v1.9.25; He dkk.: Rinkeby; Eisdspa: Geth v1.10.2; ZeeStar: EVM Istanbul). Angka TrustGive merupakan hasil pengukuran empiris deterministik pada EVM Hardhat (Solidity ^0.8.28).*"
    )
    
    add_body_p(
        "Berdasarkan latar belakang dan identifikasi masalah di atas, penelitian ini merumuskan tiga pertanyaan penelitian (*research questions*):"
    )
    add_list_item("1.", "**RQ1:** Bagaimana merancang arsitektur hibrida yang membagi beban komputasi privasi donasi antara *off-chain* (Paillier AHE) dan *on-chain* (zk-SNARK Groth16) secara efisien pada EVM?")
    add_list_item("2.", "**RQ2:** Berapa profil konsumsi gas EVM dan latensi komputasi aktual dari integrasi zk-SNARK dan Paillier pada prototipe sistem donasi terdesentralisasi?")
    add_list_item("3.", "**RQ3:** Bagaimana formulasi dan implementasi fungsi pembuktian pembukaan (*opening verification*) (M, R) terhadap *ciphertext* akumulasi Paillier dapat memfasilitasi audit publik atas total saldo tanpa mengekspos nominal individual di bawah model server terdelegasi?")
    
    add_body_p(
        "Sejalan dengan rumusan masalah tersebut, penelitian ini bertujuan untuk merancang, mengimplementasikan, dan mengevaluasi kinerja prototipe sistem donasi terdesentralisasi "
        "hibrida (*TrustGive*) yang memadukan enkripsi homomorfik Paillier dan zk-SNARK Groth16 guna mencapai efisiensi biaya gas on-chain, menjamin integritas rentang donasi, "
        "serta memetakan batasan keamanan dan privasi arsitektur secara transparan. Kontribusi penelitian ini terfokus pada: (1) perancangan arsitektur hibrida 3-layer yang "
        "membagi beban komputasi antara backend Go, basis data PostgreSQL dengan pola *transactional idempotency & reconciliation worker*, dan kontrak pintar Solidity EVM; "
        "(2) evaluasi empiris konsumsi gas dan latensi komputasi terukur pada mesin terdedikasi; serta (3) pemetaan batasan keamanan dan privasi prototipe secara transparan "
        "(model server *honest-but-curious*, celah *proof-to-ciphertext binding gap*, dan ketergantungan relayer) beserta implementasi algoritmik dan pengujian fungsional modul pembuktian pembukaan total agregat (M, R). Kontribusi utama penelitian ini berfokus pada rekayasa sistem (*systems engineering*) dan evaluasi empiris, bukan pengembangan primitif kriptografis teoritis baru."
    )
    
    # 8. METODE PENELITIAN
    add_h1("METODE PENELITIAN")
    add_body_p(
        "Penelitian ini dilaksanakan menggunakan metode rekayasa perangkat lunak eksperimental (*experimental systems engineering*) "
        "yang terstruktur dalam lima tahapan: perancangan arsitektur hibrida dan model ancaman formal, justifikasi dan formulasi kriptografi Paillier AHE vs alternatif, "
        "perancangan sirkuit ZK-SNARK Groth16, perancangan kontrak pintar Solidity EVM, serta perancangan model data relasional (ERD) dan alur bisnis."
    )
    
    add_h2("1. Arsitektur Hibrida Sistem dan Model Ancaman Formal")
    add_body_p(
        "Arsitektur TrustGive dirancang dalam tiga lapisan komputasi (*3-layer hybrid architecture*) untuk mendistribusikan beban komputasi secara optimal "
        "antara ranah *client*, *off-chain*, dan *on-chain*, sebagaimana disajikan pada Gambar 1."
    )
    add_figure("assets/gambar/gambar1_arsitektur_sistem.png", "Gambar 1. Arsitektur Hibrida 3-Layer Sistem Donasi TrustGive", width_cm=13.5)
    
    add_list_item("1.", "**Lapisan Antarmuka Klien (Frontend Web):** Dibangun menggunakan antarmuka Single Page Application (SPA) berbasis React 19, Vite, dan Tailwind CSS, berfungsi sebagai antarmuka donatur untuk memilih kampanye, memasukkan nominal donasi, dan memantau status donasi serta ringkasan verifikasi secara transparan tanpa membebani perangkat klien dengan komputasi kriptografis berat.")
    add_list_item("2.", "**Lapisan Logika Bisnis & Komputasi Kriptografis (Backend Go & PostgreSQL):** Dibangun menggunakan bahasa Go dengan kerangka kerja Gin (Gin Web Framework) yang mengelola logika bisnis, autentikasi berbasis JWT dengan *Role-Based Access Control* (RBAC), modul enkripsi asimetris dan akumulasi homomorfik Paillier, pendelegasian pembentukan saksi dan bukti ZK (*delegated prover*) via SnarkJS/Wasm, serta basis data relasional PostgreSQL 15 yang menerapkan pola *transactional idempotency* dan *reconciliation worker* untuk menjamin konsistensi data.")
    add_list_item("3.", "**Lapisan Konsensus & Audit Terdistribusi (Smart Contracts EVM):** Terdiri dari dua kontrak pintar Solidity (dikompilasi dengan compiler Solidity ^0.8.28): *Groth16Verifier.sol* (memverifikasi bukti ZK rentang donasi on-chain) dan *DonationRegistry.sol* (bertindak murni sebagai registri komitmen audit desentralisasi dan penyimpan *ciphertext* Paillier terenkripsi serta memancarkan event audit permanen, tanpa mengeksekusi transfer likuiditas moneter on-chain).")
    
    add_body_p(
        "Model ancaman formal dirumuskan untuk mendefinisikan batas keamanan dan asumsi kepercayaan sistem, sebagaimana dipetakan pada Tabel 2."
    )
    tbl2_headers = ["Entitas Penyerang", "Asumsi Kepercayaan", "Potensi Ancaman Keamanan / Privasi", "Mekanisme Pertahanan / Mitigasi", "Status Mitigasi"]
    tbl2_rows = [
        ["**Donatur Jahat**", "Untrusted", "Mengirimkan nominal donasi bernilai negatif (v ≤ 0) atau melampaui pagu (v > max) untuk merusak integritas keuangan", "Validasi batas rentang nominal pada API backend Go sebelum saksi dibangkitkan; sirkuit Groth16 membatasi 0 < v ≤ max (komparator 64-bit mengasumsikan input terjangkau tanpa konstrain Num2Bits(64) eksplisit di sirkuit); transaksi ditolak jika pairing gagal", "TERMITIGASI SEBAGIAN (Bergantung pada Validasi Backend)"],
        ["**Donatur / Pihak Ketiga Jahat**", "Untrusted", "Memodifikasi bukti via rerandomisasi (*malleability intrinsik Groth16*) atau memakai ulang bukti ZK antar-kampanye (*replay*)", "Kontrak mencocokkan pubSignals[0] == campaignMaxDonation[campaignId] dan pubSignals[1] == uint256(commitment); PostgreSQL memvalidasi keunikan komitmen dan Idempotency-Key", "TERMITIGASI SEBAGIAN (Relasional & Pagu; Proteksi Penuh Butuh Nullifier On-chain)"],
        ["**Pengamat Publik Blockchain**", "Untrusted", "Mengamati nominal donasi individual dan melacak identitas donatur dari buku besar publik", "Nominal donasi individual disimpan dalam ciphertext Paillier 2048-bit; nilai saksi dilindungi oleh properti Zero-Knowledge kurva BN254; submitter on-chain adalah akun relayer server", "TERMITIGASI"],
        ["**Server Backend (Reguler)**", "Honest-but-Curious", "Mengamati nominal plaintext donatur selama pendelegasian pembentukan saksi dan bukti ZK", "Server mengeksekusi komputasi aljabar Paillier dan witness secara tepat, namun tetap dapat membaca nominal input (privasi terhadap operator belum terisolasi)", "BATASAN ARSITEKTUR (Memerlukan Client-Side Prover)"],
        ["**Server Backend (Aktif/Compromised)**", "Malicious / Compromised", "Mengganti ciphertext Paillier dengan nominal yang berbeda dari saksi yang dibuktikan di sirkuit Groth16", "Ciphertext Paillier dan komitmen Poseidon belum terikat secara kriptografis di dalam sirkuit SNARK kurva BN254 (*proof-to-ciphertext binding gap*)", "BATASAN PROTOTIPE (Memerlukan Skema SAVER)"],
        ["**Penyelenggara Kampanye**", "Semi-trusted", "Memanipulasi total saldo akhir yang didekripsi ke publik", "Verifikasi terbuka pasangan (M, R) di mana publik dapat menguji kongruensi c_agg ≟ (1+Mn)R^n mod n² tanpa kunci privat, asalkan nilai R dirilis jujur oleh server", "TERMITIGASI SEBAGIAN (Bergantung Kejujuran Faktor Acak Server)"],
        ["**Pihak Setup Parameter ZK**", "Untrusted / Single-Party", "Menyimpan parameter rahasia (*toxic waste*) dari fase setup untuk membangkitkan bukti ZK palsu", "Prototipe menggunakan setup lokal SnarkJS untuk kebutuhan studi kelayakan; implementasi produksi wajib menggunakan seremoni MPC multi-partai publik", "BATASAN PROTOTIPE (Memerlukan Seremoni MPC Publik)"]
    ]
    tbl2_widths = [Cm(2.6), Cm(2.4), Cm(4.0), Cm(5.0), Cm(2.5)]
    tbl2_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]
    add_custom_table("Tabel 2. Matriks Model Ancaman Formal Sistem Donasi TrustGive", tbl2_headers, tbl2_rows, tbl2_widths, tbl2_aligns, font_size_pt=8.5)
    
    add_body_p(
        "**Nilai Tambah Pembuktian ZK pada Arsitektur Terdelegasi:** Meskipun pada prototipe awal ini saksi ZK dibangkitkan secara terdelegasi di server backend, "
        "penyertaan zk-SNARK Groth16 tetap memberikan nilai tambah mendasar yang esensial: (1) Jaminan integritas evaluasi pairing on-chain tanpa mengekspos nominal plaintext ke publik "
        "(dengan catatan soundness sirkuit terhadap field wrapping saat ini masih bergantung pada validasi input backend sebelum penambahan Num2Bits(64) eksplisit); "
        "(2) Pencegahan manipulasi komitmen donasi pada buku besar publik; dan (3) Fondasi arsitektural menuju pembuktian di sisi klien (*client-side prover*) di masa depan."
    )
    
    add_h2("2. Formulasi Kriptografi Paillier AHE dan Analisis Komparatif")
    add_body_p(
        "Tiga kandidat skema kriptografi homomorfik dievaluasi untuk sistem donasi terdesentralisasi: "
        "(1) **Exponential ElGamal:** Menghasilkan enkripsi homomorfik aditif pada kurva eliptik (c = (g^r, h^r g^m)). Namun, proses dekripsi memerlukan pemecahan logaritma diskrit "
        "(BSGS). Batas komputasi BSGS praktis sebesar 2⁴⁰ langkah setara dengan kapasitas representasi angka ≈ 1,099 × 10¹² unit nilai, atau **Rp 1,1 Triliun per kampanye**. "
        "Kendala Exponential ElGamal terletak pada kebutuhan memori tabel prekomputasi BSGS (~8 GB) dan latensi pencarian hash pada server. "
        "(2) **Pedersen Commitment:** Komitmen C = g^m h^r sangat ramah sirkuit SNARK, namun bersifat non-extractable commitment murni (bukan enkripsi), sehingga jika faktor pembuka "
        "hilang, saldo akhir tidak dapat dipulihkan secara matematis oleh pengelola sistem tanpa koordinasi interaktif tambahan. "
        "(3) **Paillier AHE:** Mendukung ruang pesan bilangan bulat moneter tanpa batas atas diskrit dan proses dekripsi instan melalui karakteristik Carmichael. "
        "Pemilihan Paillier pada prototipe TrustGive didasarkan pada kebutuhan penanganan akumulasi saldo donasi berskala besar secara off-chain tanpa hambatan batas atas BSGS "
        "dan tanpa menuntut koordinasi interaktif donatur."
    )
    add_body_p(
        "Skema Paillier didefinisikan melalui algoritma pembangkitan kunci, enkripsi c = g^m · r^n mod n² = (1 + m · n) · r^n mod n², akumulasi homomorfik c_agg = c₁ · c₂ mod n², "
        "dan dekripsi m = L(c^λ mod n²) · μ mod n (Paillier, 1999). Untuk memungkinkan publik mengaudit total hasil dekripsi tanpa memberikan kunci privat Paillier kepada publik, "
        "TrustGive menerapkan skema pembuktian terbuka (*zero-knowledge opening*). Misalkan terdapat k donasi dengan akumulasi c_agg = (1 + M · n) R^n mod n², di mana M = ∑ m_i dan R = ∏ r_i mod n. "
        "Saat kampanye berakhir, backend mempublikasikan pasangan plaintext (M, R), sehingga publik dapat memverifikasi keabsahan total M dengan memeriksa kongruensi c_agg ≟ (1 + M · n) · R^n mod n² tanpa kunci privat."
    )
    add_body_p(
        "Fungsi verifikasi pembukaan publik ini diimplementasikan secara konkret pada modul Go backend melalui fungsi `VerifyOpening(cAgg, m, r)` dan `EncryptWithRandomness(m, r)` "
        "pada paket `backend/internal/crypto/paillier/paillier.go`, serta didukung oleh CLI verifikator independen pada `backend/cmd/verify-opening/main.go`. "
        "Evaluasi soundness melalui unit test `TestZeroKnowledgeOpeningVerification` membuktikan bahwa pasangan sah (M, R) terverifikasi sukses (true), "
        "sedangkan pemalsuan nominal—baik saldo didongkrak (M + 1.000), disunat (M - 50.000), maupun faktor keacakan diubah (R + 1)—menghasilkan evaluasi false secara deterministik. "
        "Meskipun modul kriptografi ini telah teruji penuh, skema basis data operasional saat ini (`campaign_aggregates`) baru mencatat `encrypted_total`, sehingga otomatisasi persistensi faktor R terdistribusi pada pipeline basis data dirumuskan sebagai agenda rekayasa lanjutan."
    )
    
    add_h2("3. Perancangan Sirkuit ZK-SNARK dan Soundness Komparator")
    add_body_p(
        "Sirkuit ZK dirancang menggunakan bahasa Circom (kompatibel pragma circom 2.2.0) (Muñoz-Tapia dkk., 2022) dan dikompilasi ke dalam sistem pembuktian Groth16 (Groth, 2016) di atas kurva BN254. "
        "Sirkuit DonationProof.circom menghasilkan **655 constraints** (374 non-linear constraints dan 281 linear constraints). "
        "Sirkuit membuktikan bahwa nilai donasi amount berada pada rentang positif (amount > 0) via GreaterThan(64) dan tidak melampaui pagu kampanye (amount ≤ campaign_max) "
        "via LessEqThan(64), dengan kedua syarat diwajibkan serentak via konstrain perkalian `isPositive.out * isWithinLimit.out === 1`. "
        "Komitmen dihitung menggunakan fungsi hash spons Poseidon publik 2-input (Grassi dkk., 2021): commitment = Poseidon(amount, secret)."
    )
    add_body_p(
        "**Analisis Soundness dan Batasan 64-Bit Komparator:** Komparator GreaterThan(64) dan LessEqThan(64) mengandalkan dekomposisi bit Num2Bits(65) internal Circom yang mengasumsikan "
        "input berada pada rentang < 2⁶⁴. Pada prototipe ini, sanitasi nilai nominal dan pagu ditegakkan pada lapisan backend Go sebelum saksi dibangkitkan. "
        "Untuk implementasi produksi, batasan bit eksplisit Num2Bits(64) wajib ditambahkan langsung ke sinyal input privat sirkuit guna menjamin soundness di tingkat kurva tanpa bergantung pada verifikasi eksternal. "
        "Setup parameter Groth16 dieksekusi secara lokal menggunakan SnarkJS dengan fase 1 Powers of Tau BN254 standar dan fase 2 khusus sirkuit DonationProof. Seluruh berkas sirkuit .circom, .zkey, dan verifier Solidity disimpan secara terbuka pada repositori penelitian (https://github.com/Dimas-es/donasi-blockchain-paillier-zkSnark, rilis tag v1.0.0-benchmark)."
    )
    
    add_h2("4. Perancangan Kontrak Pintar Solidity EVM")
    add_body_p(
        "Kontrak pintar diimplementasikan menggunakan Solidity versi ^0.8.28. Kontrak bertindak murni sebagai **registri komitmen audit donasi dan verifikasi bukti kriptografis** "
        "(*donation commitment & audit registry*), bukan penyalur likuiditas keuangan fiat atau kustodian saldo token (tidak memuat fungsi payable maupun transfer dana on-chain): "
        "(1) *Groth16Verifier.sol*: Mengimplementasikan antarmuka IGroth16Verifier dengan fungsi verifikasi bukti non-interaktif verifyProof() menggunakan operasi pairing kurva eliptik BN254 pada precompiled contract EVM (alamat 0x08). "
        "(2) *DonationRegistry.sol*: Mengelola pemetaan pagu donasi kampanye dan rekaman donasi terverifikasi melalui fungsi setCampaignMaxDonation(), recordDonation(), getDonation(), dan getDonationCount()."
    )
    
    add_h2("5. Perancangan Model Data Relasional (ERD) dan Alur Bisnis")
    add_body_p(
        "Model data off-chain diimplementasikan pada PostgreSQL 15 (Gambar 2). Skema ERD terdiri dari 4 entitas utama: `users` (identitas dan RBAC), `campaigns` (inisiatif donasi dan pagu), "
        "`donations` (rekaman donasi, komitmen Poseidon, ciphertext Paillier, proof JSON, tx_hash, dan kolom `idempotency_key` dengan UNIQUE INDEX parsial), serta `campaign_aggregates` "
        "(akumulasi homomorfik off-chain yang dikunci via row-level locking `SELECT FOR UPDATE` saat donasi dikonfirmasi), ditambah 1 tabel `donations_duplicate_archive`."
    )
    add_figure("assets/gambar/gambar2_erd_database.png", "Gambar 2. Diagram Relasi Entitas (ERD) Model Data Sistem", width_cm=13.5)
    
    add_body_p(
        "Alur transaksi donasi end-to-end, siklus hidup kampanye, dan pola rekonsiliasi state diilustrasikan berturut-turut pada Gambar 3, Gambar 4, dan Gambar 5. "
        "Pada alur transaksi donasi (Gambar 3), donatur hanya memasukkan nominal donasi v pada antarmuka web, sementara pembangkitan faktor acak blinding, pembentukan saksi Poseidon, komputasi bukti Groth16, dan enkripsi Paillier didelegasikan ke modul server sebelum memanggil transaksi on-chain `recordDonation(campaignId, commitment, encryptedAmount, proof)`. "
        "Pada siklus hidup kampanye (Gambar 4), implementasi operasional basis data sistem saat ini mengelola dua status utama, yaitu 'active' (menerima donasi terverifikasi ZK dan agregasi homomorfik Paillier) dan 'closed' (penerimaan donasi ditutup permanen). Tahapan registrasi pagu on-chain via setCampaignMaxDonation(), penutupan kampanye, dekripsi agregat total M oleh pengelola kunci privat, serta verifikasi pembukaan publik (M, R) via fungsi VerifyOpening merepresentasikan alur tata kelola siklus hidup kampanye secara end-to-end. "
        "Untuk mengatasi kendala desinkronisasi data antara basis data relasional PostgreSQL dan blockchain EVM (*dual-write problem*), TrustGive menerapkan pola desain *Transactional Idempotency & Reconciliation Worker*. "
        "Setiap permintaan donasi wajib menyertakan header `Idempotency-Key` unik berupa identifier UUID v4. Jika permintaan dengan kunci identik dikirimkan ulang akibat transmisi ulang jaringan atau pemanggilan paralel, "
        "backend Go mengenali rekaman donasi yang telah ada dan secara aman mengembalikan representasi respon tersimpan (*safe replay*) dengan status **HTTP 200 OK** (sedangkan permintaan pertama menghasilkan HTTP 201 Created) tanpa memicu komputasi ZK ulang maupun transaksi on-chain ganda. "
        "Secara asinkron, pekerja latar belakang (*reconciliation worker*) berjalan secara berkala memanggil `ReconcilePendingDonations` untuk memindai transaksi berstatus PENDING atau FAILED guna menyelaraskan status akhir menjadi CONFIRMED setelah simpul RPC kembali normal."
    )
    add_figure("assets/gambar/gambar3_workflow_donasi.png", "Gambar 3. Diagram Alur Transaksi Donasi End-to-End", width_cm=14.0)
    add_figure("assets/gambar/gambar7_lifecycle_kampanye.png", "Gambar 4. Siklus Hidup Status Kampanye Donasi (Status Operasional Sistem dan Alur Rekonsiliasi Audit)", width_cm=13.0)
    add_figure("assets/gambar/gambar5_alur_idempotensi_recovery.png", "Gambar 5. Alur Logika Idempotensi dan Rekonsiliasi State Transaksi", width_cm=13.5)
    
    # 9. HASIL DAN PEMBAHASAN
    add_h1("HASIL DAN PEMBAHASAN")
    add_body_p(
        "Evaluasi empiris dilakukan pada lingkungan pengujian terdedikasi tunggal dengan spesifikasi: prosesor **Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz (4 Cores, 8 Threads)**, "
        "RAM 8 GB DDR4, SSD NVMe, sistem operasi **Microsoft Windows 11 Pro 64-bit**, node blockchain lokal Hardhat (Solidity 0.8.28, block gas limit 30.000.000 gas, 0 gwei basefee), "
        "Go versi 1.27.1 (kompatibel go.mod 1.25), Node.js v24.21.0, SnarkJS v0.7.6, dan Circom pragma 2.2.0. Seluruh data mentah benchmark per-iterasi, berkas pengujian gas, dan skrip analisis disimpan dan dapat direproduksi secara mandiri "
        "pada direktori repositori `assets/benchmark/` (mencakup berkas CSV mentah `benchmark_paillier_raw.csv`, `benchmark_zk_raw.csv`, `benchmark_gas_raw.csv`, `benchmark_onchain_raw.csv`, dan ringkasan terstruktur `benchmark_summary.json`) "
        "yang terikat pada repositori terbuka GitHub (https://github.com/Dimas-es/donasi-blockchain-paillier-zkSnark, rilis tag `v1.0.0-benchmark` tertanggal 22 Oktober 2026)."
    )
    
    add_h2("1. Profil Konsumsi Gas Kontrak Pintar pada EVM dan Rekonsiliasi Storage")
    add_body_p(
        "Pengukuran konsumsi bahan bakar (*gas consumption*) pada EVM dievaluasi secara empiris menggunakan Hardhat testbed dengan hasil pada Tabel 3 dan visualisasi pada Gambar 6. "
        "Verifikasi pairing Groth16 mandiri memerlukan 225.035 gas. Transaksi pencatatan donasi lengkap on-chain membutuhkan 613.627 gas (muatan ringkas 22B) hingga 959.465 gas (muatan biner Paillier 512B), "
        "dan mencapai 1.481.734 gas pada muatan string desimal 1.233B (perilaku Go backend saat ini). Berdasarkan implementasi empiris recordDonationOptimized via event log, konsumsi gas berhasil dipangkas secara substansial menjadi 382.632 gas (penghematan 60,1% vs biner dan 74,2% vs desimal). "
        "Kompromi Desain dan Ketersediaan Data: Pada varian recordDonationOptimized, pemangkasan gas dicapai dengan memancarkan ciphertext Paillier ke event log blockchain (DonationRecordedOptimized), dengan storage hanya mempertahankan komitmen, ID kampanye, dan digest keccak256. Akibatnya, verifikasi audit publik atas pasangan pembukaan total (M, R) memerlukan akses riwayat log peristiwa via simpul arsip (archive node) atau middleware pengindeks (seperti The Graph atau backend event indexer)."
    )
    
    tbl3_headers = ["Operasi Kontrak Pintar", "Metode Eksekusi", "Konsumsi Gas (Actual)", "Gas Limit EVM", "% Batas Blok", "Rincian Alokasi Komputasi / Storage"]
    tbl3_rows = [
        ["**Deploy Verifier Groth16**", "Contract Creation", "391.827", "30.000.000", "1,31%", "Inisialisasi konstanta pairing IC[], curve precompile"],
        ["**Deploy DonationRegistry**", "Contract Creation", "1.598.894", "30.000.000", "5,33%", "Inisialisasi alamat verifier, owner, dan setup storage array"],
        ["**Konfigurasi Pagu Kampanye**", "`setCampaignMaxDonation()`", "45.908", "30.000.000", "0,15%", "Transaksi dasar (21k) + SSTORE pagu baru + Event"],
        ["**Groth16 Verify Only**", "`verifyProof()`", "225.035", "30.000.000", "0,75%", "Precompile staticcall: 4 pairing checks kurva BN254"],
        ["**Pencatatan Donasi (Dummy 22B)**", "`recordDonation()`", "613.627", "30.000.000", "2,05%", "Pairing check (225k) + SSTORE ~18 slot struct + Event"],
        ["**Pencatatan Donasi (Biner 512B)**", "`recordDonation()`", "959.465", "30.000.000", "3,20%", "Pairing + SSTORE 15 slot ciphertext Paillier + Calldata"],
        ["**Pencatatan Donasi (String 1233B)**", "`recordDonation()`", "1.481.734", "30.000.000", "4,94%", "Perilaku Go backend: SSTORE 38 slot string desimal Paillier"],
        ["**Pencatatan Teroptimasi (Biner 512B)**", "`recordDonationOptimized()`", "382.632", "30.000.000", "1,28%", "Empiris: pairing (~200k) + SSTORE 6 slot struct terkemas (uint96) + LOG3"]
    ]
    tbl3_widths = [Cm(3.0), Cm(2.4), Cm(1.9), Cm(1.9), Cm(1.4), Cm(5.4)]
    tbl3_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.LEFT]
    add_custom_table("Tabel 3. Profil Konsumsi Gas Kontrak Pintar pada EVM Hardhat (Terukur dan Terproyeksi)", tbl3_headers, tbl3_rows, tbl3_widths, tbl3_aligns, font_size_pt=8.5)
    add_figure("assets/gambar/grafik_konsumsi_gas.png", "Gambar 6. Profil Konsumsi Gas Kontrak Pintar pada EVM Hardhat", width_cm=14.0)
    
    add_h2("2. Evaluasi Waktu Komputasi Kriptografi dan Latensi End-to-End")
    add_body_p(
        "Evaluasi waktu komputasi kriptografis dilakukan melalui pengujian berulang empiris terstandarisasi pada lingkungan pengujian referensi terdedikasi (Intel Core i5-8250U 1.60GHz, RAM 8 GB DDR4, Windows 11 Pro 64-bit). "
        "Untuk menegakkan integritas dan reliabilitas pelaporan statistik: "
        "(1) **Standarisasi Beban Uji dan Pembangkitan Blinding:** Evaluasi menggunakan beban kerja representatif terstandarisasi (v = 5.000 dengan pagu = 50.000 dan nilai blinding Poseidon s heksadesimal konstan untuk pengujian Groth16; serta v = 50.000 dan v = 75.000 untuk uji homomorfik Paillier). Pada Paillier, faktor blinding acak r ∈ Z*_n dibangkitkan segar via CSPRNG (crypto/rand) pada setiap iterasi enkripsi, dengan durasi komputasi yang didominasi oleh eksponensiasi modular r^n mod n² pada dimensi modulus n = 2048 bit (bukan magnitudo skalar v). Sedangkan pada Groth16, jumlah konstrain R1CS dan durasi pembuktian bersifat invarian secara struktural terhadap nilai skalar sinyal numerik; "
        "(2) **Spesifikasi Jenis Simpangan Baku:** Seluruh simpangan baku yang dilaporkan adalah **Sample Standard Deviation** (s, dihitung dengan koreksi Bessel ddof=1); "
        "(3) **Penyajian Metrik Robust (Median dan P95):** Tabel 4 menyajikan nilai **Median dan P95** di samping rata-rata parametrik (Mean ± s) guna mengantisipasi skewness data; dan "
        "(4) **Pemisahan Fase Cold-Start (Warm-Up):** Lonjakan inisialisasi awal (cold start) dipisahkan secara transparan dari kinerja kondisi stabil (steady-state)."
    )
    
    tbl4_headers = ["No", "Komponen Operasi Kriptografi", "Algoritma / Lingkungan", "Sampel (N)", "Mean ± s (ms)", "Median (P95) [ms]", "Min – Maks (ms)", "Karakteristik & Catatan Statistik"]
    tbl4_rows = [
        ["1", "**KeyGen (512-bit)**", "Paillier (Go)", "N=50", "6,43 ± 2,91", "6,13 (11,61)", "0,00 – 12,97", "Prima 256-bit; 1 sampel 0,00 ms akibat timer Windows (N=49 non-zero: 6,56 ± 2,79 ms)"],
        ["2", "**KeyGen (2048-bit)**", "Paillier (Go)", "N=30", "278,22 ± 119,18", "269,21 (510,11)", "74,23 – 528,01", "Pencarian prima 1024-bit acak (CV 42,8%)"],
        ["3", "**Enkripsi Nominal**", "Paillier Cryptosystem", "N=100", "20,19 ± 6,71", "19,15 (33,52)", "8,24 – 54,08", "Eksponensiasi modular r^n mod n² (sampling blinding r CSPRNG)"],
        ["4", "**Penjumlahan Homomorfik**", "Paillier AHE", "N=100", "0,013 ± 0,004", "0,012 (0,021)", "0,004 – 0,024", "Perkalian modular BigInt (~79.300 op/detik throughput)"],
        ["5", "**Dekripsi Total Agregat**", "Paillier Cryptosystem", "N=100", "17,96 ± 3,98", "18,24 (23,39)", "10,14 – 29,46", "Eksponensiasi Carmichael c^λ mod n² (27 alokasi)"],
        ["6", "**Pembangkitan Bukti ZK**", "Groth16 WASM (In-Process)", "N=30", "212,18 ± 98,75", "189,56 (249,20)", "169,48 – 722,63", "Cold-start iterasi 1: 722,63 ms; steady-state (N=29): 194,58 ± 21,73 ms (median 189,39 ms)"],
        ["7", "**Verifikasi Bukti In-Process**", "SnarkJS Verifier (JS)", "N=30", "19,84 ± 2,98", "18,95 (24,41)", "16,19 – 32,02", "Evaluasi 4 pairing kurva BN254 in-process"],
        ["8", "**Verifikasi Bukti Subprocess**", "Subprocess `npx snarkjs`", "N=30", "1.935,30 ± 107,78", "1.922,22 (2.095,76)", "1.784,26 – 2.185,51", "Overhead startup eksternal Node.js/npx CLI wrapper"],
        ["9", "**Verifikasi Pairing On-Chain**", "EVM Precompile 0x08", "N=30", "4,15 ± 0,31", "4,05 (4,65)", "3,72 – 4,77", "Pairing precompile 0x08 Hardhat (225.035 gas deterministik)"],
        ["10", "**Eksekusi Transaksi On-Chain**", "recordDonation() Tx", "N=30", "14,14 ± 2,12", "13,05 (18,11)", "11,96 – 18,62", "Penambangan blok automine Hardhat (CSV mentah)"]
    ]
    tbl4_widths = [Cm(0.8), Cm(2.7), Cm(2.4), Cm(1.3), Cm(2.3), Cm(2.1), Cm(2.1), Cm(3.2)]
    tbl4_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    add_custom_table("Tabel 4. Evaluasi Waktu Komputasi Kriptografi Terstandarisasi", tbl4_headers, tbl4_rows, tbl4_widths, tbl4_aligns, font_size_pt=8.0)
    
    add_body_p(
        "Data pada Tabel 4 dan Gambar 7 memperlihatkan bahwa pada pembangkitan bukti ZK in-process, pengukuran iterasi pertama mencatatkan lonjakan cold-start sebesar 722,63 ms akibat inisialisasi WebAssembly dan kompilasi JIT runtime V8 Node.js. "
        "Setelah fase warm-up dilewati, performa steady-state (N=29) stabil pada rata-rata 194,58 ± 21,73 ms dengan **Median 189,39 ms** dan **P95 236,16 ms**. "
        "Berdasarkan nilai median steady-state, latensi transaksi end-to-end terproyeksi turun menjadi ~240,5 ms (<0,25 detik, rincian: Paillier 19,2 ms + Groth16 prove 189,4 ms + verifikasi lokal 18,9 ms + automine tx 13,1 ms), "
        "dan tetap di bawah 0,35 detik pada batas P95 (~312,2 ms). Berbeda dari latensi komputasi wall-clock, konsumsi gas pada EVM Hardhat bersifat deterministik secara arsitektural. "
        "Pengukuran ini dievaluasi pada lingkungan uji tunggal terdedikasi (Intel Core i5-8250U, RAM 8 GB, Windows 11), dan evaluasi multi-platform publik disarankan sebagai arah riset lanjutan."
    )
    add_figure("assets/gambar/grafik_latensi_e2e.png", "Gambar 7. Distribusi Komponen Latensi End-to-End Transaksi Donasi Sekuensial", width_cm=14.0)
    
    add_h2("3. Matriks Pengujian Fungsional, Keandalan, dan Pemetaan Keterbatasan")
    add_body_p(
        "Tabel 5 menyajikan hasil evaluasi pengujian fungsional, keandalan, dan pemetaan batasan keamanan prototipe. "
        "Seluruh skenario pengujian keandalan dan keamanan pada Tabel 5 dapat direproduksi secara mandiri oleh pembaca melalui rangkaian uji otomatis yang disediakan pada repositori: "
        "(1) pengujian unit backend Go untuk validasi input rentang nominal donasi, replay idempotensi HTTP 200 OK dengan 5 request paralel ber-kunci UUID, serta transisi mesin status rekonsiliasi dapat dijalankan via perintah `go test -v -run TestTable5 ./internal/donation/...`; "
        "(2) pengujian sirkuit Circom untuk penolakan saksi (witness rejection) pada batasan komparator dapat direproduksi via skrip mandiri `node zk/scripts/test_table5_circom.js`; "
        "(3) pengujian kontrak pintar EVM Hardhat untuk penolakan substitusi sinyal publik dan pembuktian soundness ZK dapat dijalankan via perintah `npx hardhat test`; serta "
        "(4) pengujian konkurensi end-to-end multi-request paralel via skrip `backend/scripts/concurrent_idempotency.sh`."
    )
    tbl5_headers = ["No", "Kategori", "Skenario Uji", "Perilaku yang Diharapkan", "Hasil Pengamatan Empiris", "Status Evaluasi"]
    tbl5_rows = [
        ["1", "Fungsional", "**Registrasi Kampanye Donasi Baru**", "Transaksi on-chain sukses, pagu tersimpan di kontrak", "Pagu tersimpan di kontrak pintar dan basis data", "BERHASIL"],
        ["2", "Fungsional", "**Donasi Valid (0 < v ≤ pagu)**", "Bukti ZK valid, transaksi on-chain sukses, saldo teragregasi", "Bukti diverifikasi on-chain, event dipancarkan, agregat bertambah", "BERHASIL"],
        ["3", "Keamanan ZK", "**Donasi Negatif atau Nol (v ≤ 0)**", "Ditolak pada validasi input API backend dan sirkuit ZK menolak saksi", "API backend mengembalikan HTTP 400 Bad Request (`amount must be greater than zero`); pembentukan saksi Circom melempar error `Error: Error: Assert Failed.` pada konstrain GreaterThan(64) (`test_table5_circom.js`)", "BERHASIL (Uji Otomatis Go & Circom)"],
        ["4", "Keamanan ZK", "**Donasi Melampaui Pagu (v > pagu)**", "Ditolak pada validasi bisnis API backend dan sirkuit ZK menolak saksi", "API backend mengembalikan HTTP 400 Bad Request (`amount exceeds campaign maximum donation`); pembentukan saksi Circom melempar error `Error: Error: Assert Failed.` pada konstrain LessEqThan(64) (`test_table5_circom.js`)", "BERHASIL (Uji Otomatis Go & Circom)"],
        ["5", "Keamanan ZK", "**Pemalsuan Bukti / Modifikasi Saksi**", "Kontrak pintar menolak transaksi via pairing check jika saksi atau bukti dimodifikasi", "Transaksi revert: pairing check EVM gagal (`invalid zk proof`); membuktikan soundness terhadap bukti palsu (proteksi rerandomisasi malleability butuh nullifier on-chain)", "BERHASIL (Uji Soundness Bukti Hardhat)"],
        ["6", "Keamanan ZK", "**Substitusi Sinyal Publik On-Chain**", "Kontrak pintar menolak transaksi jika sinyal publik tidak cocok dengan pagu kontrak atau komitmen", "Transaksi revert deterministik di EVM: revert `\"invalid campaign max\"` jika pagu dimanipulasi, revert `\"invalid commitment\"` jika komitmen dimanipulasi, dan revert `\"invalid zk proof\"` jika verifier pairing gagal", "BERHASIL (Uji Otomatis Hardhat)"],
        ["7", "Reliabilitas", "**Konkurensi 5 Donasi Simultan**", "5 request paralel diproses tertib tanpa tabrakan deadlock atau inkonsistensi saldo", "5 request paralel (`concurrent_idempotency.sh`) sukses diproses via connection pool; baris agregat kampanye terlindungi oleh row-level locking SELECT FOR UPDATE", "BERHASIL (Uji Skrip Paralel N=5)"],
        ["8", "Reliabilitas", "**Idempotensi Kunci Duplikat (UUID)**", "Menolak eksekusi ganda dan mengembalikan respon tersimpan (*safe replay*) untuk Idempotency-Key sama", "Request awal menghasilkan HTTP 201 Created; 4 request transmisi ulang dengan UUID Idempotency-Key sama mengembalikan HTTP 200 OK (replay aman, bukan 409) dengan ID donasi identik tanpa re-eksekusi on-chain", "BERHASIL (Uji Otomatis Go & Skrip)"],
        ["9", "Reliabilitas", "**Kegagalan RPC Blockchain (Failover & Rekonsiliasi)**", "Transaksi tersimpan aman di basis data saat RPC terputus dan status diselaraskan otomatis saat jaringan pulih", "Transaksi berstatus PENDING atau FAILED berhasil diselaraskan menjadi CONFIRMED oleh pekerja latar belakang (*reconciliation worker*) setelah simpul RPC kembali normal tanpa kehilangan data", "BERHASIL (Uji Transisi Status & Worker)"],
        ["10", "Auditabilitas", "**Verifikasi Mandiri Akumulasi Ciphertext**", "Perkalian modular seluruh ciphertext sama dengan total agregat", "Nilai ∏ c_i mod n² identik dengan c_agg basis data", "BERHASIL"],
        ["11", "Auditabilitas", "**Verifikasi Pembukaan Publik (M, R) (Soundness)**", "Fungsi VerifyOpening menerima (M, R) sah dan menolak manipulasi nominal M atau R tanpa kunci privat", "Unit test Go membuktikan soundness: pasangan sah sukses (true), manipulasi M+1000, M-50000, dan R+1 ditolak (false); CLI mandiri berfungsi", "BERHASIL (Tingkat Modul Kriptografi; Persistensi DB Dirancang)"],
        ["12", "Privasi", "**Perlindungan Nominal thd Server Backend**", "Server tidak dapat melihat nominal plaintext donatur", "Server backend menerima nominal plaintext untuk pendelegasian ZK", "KETERBATASAN ARSITEKTUR (Model Server HbC)"],
        ["13", "Keamanan", "**Proteksi Substitusi Ciphertext (Binding Gap)**", "Sirkuit ZK mengikat ciphertext Paillier dengan saksi nominal", "Sirkuit belum memverifikasi enkripsi Paillier (hanya Poseidon)", "KETERBATASAN PROTOTIPE (Celah Binding Gap)"],
        ["14", "Keamanan", "**Pencegahan Replay Lintas Kampanye Serupa**", "Bukti ZK terikat secara on-chain ke ID kampanye spesifik", "Sirkuit hanya mengikat nilai pagu; pencegahan saat ini ada pada DB", "TERMITIGASI SEBAGIAN (Tingkat Relasional)"]
    ]
    tbl5_widths = [Cm(0.8), Cm(2.0), Cm(3.2), Cm(3.8), Cm(4.7), Cm(2.0)]
    tbl5_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]
    add_custom_table("Tabel 5. Matriks Hasil Pengujian Fungsional, Keandalan, dan Pemetaan Keterbatasan Sistem", tbl5_headers, tbl5_rows, tbl5_widths, tbl5_aligns, font_size_pt=8.5)
    
    add_h2("4. Analisis Keamanan, Batas Privasi, dan Diskusi Literatur")
    add_body_p(
        "Berdasarkan temuan empiris pada Tabel 5 dan perbandingan komparatif pada Tabel 1, arsitektur hibrida TrustGive memiliki posisi komparatif yang unik: "
        "(1) **Trade-off terhadap Sistem Berbasis Relayer Penuh (Astraea & ZeeStar):** Astraea mengadopsi privasi penuh terhadap operator menggunakan multi-relayer pool dan enkripsi privat dengan biaya gas masif (>1.200.000 gas). ZeeStar (Steffen dkk., 2022) mengombinasikan ZK dan enkripsi homomorfik dengan biaya ~339.000 gas, namun dibatasi oleh kapasitas logaritma diskret BSGS (≤ 2⁴⁰) dan kebutuhan CRS spesifik sirkuit. TrustGive memangkas konsumsi gas on-chain menjadi 225.035 gas untuk verifikasi pairing mandiri (dan 382.632 gas untuk pencatatan donasi teroptimasi) dengan mengeksekusi agregasi homomorfik Paillier secara off-chain tanpa batasan BSGS. "
        "(2) **Trade-off terhadap Sistem Berbasis Pedersen Commitment (Eisdspa):** Eisdspa memanfaatkan Pedersen commitment yang non-extractable, menyulitkan pemulihan total saldo jika donatur tidak aktif. "
        "TrustGive mengatasi hal ini melalui sifat asimetris Paillier dan protokol pembuktian terbuka (*zero-knowledge opening*) (M, R), di mana total saldo kampanye dapat dipulihkan secara deterministik oleh pengelola dan diverifikasi keabsahannya oleh publik secara terbuka tanpa memerlukan kustodian multi-pihak. Algoritma VerifyOpening telah diimplementasikan dan divalidasi pada modul Go, membuktikan bahwa manipulasi nominal M ditolak seketika oleh pemeriksaan kongruensi. Namun, pengintegrasian akumulasi faktor acak R terdistribusi ke dalam skema basis data operasional campaign_aggregates dan evaluasi sirkuit verifikasi on-chain pembukaan mandiri menjadi fokus agenda penelitian lanjutan (*future work*). "
        "(3) **Pemetaan Batas Privasi Prototipe:** Dua batasan utama prototipe ini adalah status server backend sebagai *honest-but-curious* dan celah *proof-to-ciphertext binding gap*, "
        "yang menjadi fokus agenda penyempurnaan sistem masa depan."
    )
    
    # 10. KESIMPULAN
    add_h1("KESIMPULAN")
    add_body_p(
        "Penelitian ini telah menyajikan studi desain dan evaluasi kinerja empiris prototipe sistem donasi terdesentralisasi hibrida TrustGive yang memadukan kriptosistem "
        "*Additive Homomorphic Encryption* (AHE) Paillier, zk-SNARK Groth16, dan kontrak pintar Ethereum Virtual Machine (EVM). Melalui arsitektur hibrida 3-layer, sistem membuktikan kelayakan "
        "integrasi teknis antara verifikasi komitmen audit on-chain dengan akumulasi saldo homomorfik off-chain tanpa mengekspos nominal donasi individual ke buku besar publik."
    )
    
    add_body_p(
        "Hasil evaluasi empiris menunjukkan bahwa verifikasi pairing Groth16 mandiri memerlukan 225.035 gas, sedangkan transaksi pencatatan donasi on-chain dengan muatan string desimal saat ini memerlukan 1.481.734 gas (959.465 gas untuk muatan biner dan 613.627 gas untuk muatan ringkas, dan terpangkas menjadi 382.632 gas melalui optimasi penyimpanan hash dan event log). "
        "Agregasi homomorfik Paillier off-chain berlangsung sangat efisien dalam 0,013 milidetik (~79.100 operasi/detik), sementara komputasi pembuktian ZK in-process memerlukan 212,18 milidetik (median 189,56 ms, kondisi stabil 194,58 ms), menghasilkan latensi transaksi end-to-end in-process yang responsif sebesar ~240,5 ms (<0,25 detik pada kondisi stabil median). "
        "Analisis profil latensi membuktikan bahwa komputasi kriptografi inti bukanlah bottleneck sistem; latensi multi-detik pada eksekusi eksternal semata-mata dipicu oleh overhead startup runtime Node.js (~1,94 detik), sehingga integrasi pustaka native menjadi rekomendasi kunci implementasi produksi. "
        "Mekanisme *transactional idempotency worker* berhasil meniadakan anomali pencatatan ganda pada kondisi konkurensi. "
        "Formulasi dan pengujian fungsi aljabar pembukaan publik (*opening verification*) (M, R) pada modul kriptografi membuktikan kelayakan verifikasi independen atas total saldo tanpa kustodian kunci privat, dengan evaluasi unit test yang menolak secara deterministik manipulasi saldo palsu, sementara integrasi persistensi faktor R pada pipeline basis data relasional dirumuskan sebagai agenda pengembangan lanjutan."
    )
    
    add_body_p(
        "**Implikasi Praktis dan Teoretis:** Temuan penelitian ini mengindikasikan bahwa kombinasi komputasi off-chain Paillier dan verifikasi zk-SNARK on-chain membuka arah pendekatan "
        "yang menjanjikan dalam eksplorasi pemenuhan prinsip minimisasi data (*data minimization*) pada buku besar publik Web3—sebagaimana diamanatkan dalam instrumen regulasi seperti "
        "Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) (Republik Indonesia, 2022)—meskipun kedaulatan privasi donatur secara penuh masih memerlukan "
        "pengalihan modul pembuktian saksi ke sisi peramban (*client-side prover*)."
    )
    
    add_body_p(
        "**Agenda Penelitian Lanjutan:** Pengembangan prototipe ini menuju kesiapan produksi difokuskan pada tiga arah utama: "
        "(1) Pengimplementasian skema *verifiable encryption* SAVER (Lee dkk., 2020) untuk mengikat secara kriptografis saksi ZK dengan ciphertext Paillier guna menutup celah *binding gap*; "
        "(2) Penguatan keamanan kontrak pintar melalui penambahan pemetaan status `usedCommitments` dan pengikatan sinyal `campaign_id` ke dalam sirkuit guna mencegah serangan replay; serta "
        "(3) Migrasi modul pembuktian ZK sepenuhnya ke sisi peramban donatur (*client-side prover*) menggunakan WebAssembly dan SnarkJS browser build; dan (4) Integrasi persistensi faktor acak agregat R = ∏ r_i mod n pada skema basis data operasional serta evaluasi sirkuit verifikasi on-chain pembukaan total (M, R) pada kontrak pintar."
    )
    
    # 11. DAFTAR PUSTAKA
    add_h1("DAFTAR PUSTAKA")
    
    references = [
        "Almaghrabi, A., & Alhogail, A. (2022). Blockchain-based donations traceability framework. *Journal of King Saud University – Computer and Information Sciences*, 34(10), 9442–9454. https://doi.org/10.1016/j.jksuci.2022.09.021",
        "Babel, M., & Sedlmeir, J. (2023). Bringing data minimization to digital wallets at scale with general-purpose zero-knowledge proofs. *arXiv preprint arXiv:2301.00823*. https://doi.org/10.48550/arXiv.2301.00823",
        "Bünz, B., Agrawal, S., Zamani, M., & Boneh, D. (2020). Zether: Towards privacy in a smart contract world. *Financial Cryptography and Data Security (FC 2020)*, LNCS 12059, 423–443. https://doi.org/10.1007/978-3-030-51280-4_14",
        "Burgos, A., & Alchieri, E. (2025). Privacy-preserving smart contracts for permissioned blockchains: A zk-SNARK-based recipe part-1. *arXiv preprint arXiv:2501.03391*. https://doi.org/10.48550/arXiv.2501.03391",
        "Chaliasos, S., Ernstberger, J., Wong, D., Jovanovic, P., & Livshits, B. (2024). SoK: What don't we know? Understanding security vulnerabilities in SNARKs. *Proceedings of the 33rd USENIX Security Symposium (USENIX Security 24)*, 494–511.",
        "Christ, M., Baldimtsi, F., Chalkias, K., & Roy, A. (2024). SoK: Zero-knowledge range proofs. *6th Conference on Advances in Financial Technologies (AFT 2024)*, LIPIcs 316, 8:1–8:24. https://doi.org/10.4230/LIPIcs.AFT.2024.8",
        "Damle, S., Gujar, S., & Moti, M. H. (2021). FASTEN: Fair and secure distributed voting using smart contracts. *arXiv preprint arXiv:2102.10594*. https://doi.org/10.48550/arXiv.2102.10594",
        "Grassi, L., Khovratovich, D., Rechberger, C., Roy, A., & Schofnegger, M. (2021). Poseidon: A new hash function for zero-knowledge proof systems. *Proceedings of the 30th USENIX Security Symposium (USENIX Security 21)*, 519–535.",
        "Groth, J. (2016). On the size of pairing-based non-interactive arguments. *Advances in Cryptology – EUROCRYPT 2016*, LNCS 9666, 305–326. https://doi.org/10.1007/978-3-662-49896-5_11",
        "Habib, M. A. (2025). Analyzing performance bottlenecks in zero-knowledge proof based rollups on Ethereum. *arXiv preprint arXiv:2503.22709*. https://doi.org/10.48550/arXiv.2503.22709",
        "He, B., Feng, T., Fang, J., Liu, C., & Su, C. (2024). A secure and efficient charitable donation system based on Ethereum blockchain and searchable encryption. *IEEE Transactions on Consumer Electronics*, 70(1), 2977–2987. https://doi.org/10.1109/TCE.2023.3323356",
        "Lavin, R., Liu, X., Mohanty, H., de la Rocha, A. S., & Xu, M. (2024). A survey on the applications of zero-knowledge proofs. *arXiv preprint arXiv:2408.00243*. https://doi.org/10.48550/arXiv.2408.00243",
        "Lee, J., Choi, H., Kim, J., & Oh, H. (2020). SAVER: SNARK-friendly, additively-homomorphic, and verifiable encryption with rerandomization. *Advances in Cryptology – PKC 2020*, LNCS 12111, 97–123. https://doi.org/10.1007/978-3-030-45388-6_4",
        "Li, M., Chen, Y., Zhu, L., Zhang, Z., Ni, J., & Conti, M. (2023). Astraea: Anonymous and secure auditing based on private smart contracts for donation systems. *IEEE Transactions on Dependable and Secure Computing*, 20(4), 3002–3018. https://doi.org/10.1109/TDSC.2022.3204287",
        "Morais, E., Koens, T., van Wijk, C., & Koren, A. (2020). A survey on zero knowledge range proofs and applications. *arXiv preprint arXiv:1907.06381*. https://doi.org/10.48550/arXiv.1907.06381",
        "Muñoz-Tapia, J. L., Bellés-Muñoz, M., Isabel, M., & Rubio, A. (2022). CIRCOM: A robust and scalable language for building complex zero-knowledge circuits. *TechRxiv*, preprint. https://doi.org/10.36227/techrxiv.19374986.v1",
        "Nairi, C., Cicioğlu, M., & Çalhan, A. (2024). Smart blockchain networks: Revolutionizing donation tracking in the Web 3.0. *Computer Communications*, 228, 107981. https://doi.org/10.1016/j.comcom.2024.08.012",
        "Paillier, P. (1999). Public-key cryptosystems based on composite degree residuosity classes. *Advances in Cryptology – EUROCRYPT '99*, LNCS 1592, 223–238. https://doi.org/10.1007/3-540-48910-X_16",
        "Quintero-Narvaez, C. E., et al. (2023). Zero-knowledge proofs for questionnaire result verification in smart contracts. *arXiv preprint arXiv:2310.13618*. https://doi.org/10.48550/arXiv.2310.13618",
        "Ren, J., et al. (2021). Cloak: Enabling confidential smart contract with multi-party transactions. *arXiv preprint arXiv:2106.13926*. https://doi.org/10.48550/arXiv.2106.13926",
        "Republik Indonesia. (2022). Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi. *Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196*. Jakarta: Sekretariat Negara.",
        "Sameera, K. M., Nicolazzo, S., Arazzi, M., Nocera, A., Vinod, P., & Conti, M. (2024). Privacy-preserving in blockchain-based federated learning systems: A survey. *Computer Communications*, 220, 150–166. https://doi.org/10.48550/arXiv.2401.03552",
        "Saraswat, D., Patel, F., Bhattacharya, P., Tanwar, S., et al. (2022). UpHaaR: Blockchain-based charity donation scheme to handle financial irregularities. *Journal of Information Security and Applications*, 70, 103245. https://doi.org/10.1016/j.jisa.2022.103245",
        "Steffen, S., Bichsel, B., Baumgartner, R., & Vechev, M. (2022). ZeeStar: Private smart contracts by homomorphic encryption and zero-knowledge proofs. *Proceedings of the 2022 IEEE Symposium on Security and Privacy (S&P 2022)*, 936–953. https://doi.org/10.1109/SP46214.2022.9833633",
        "Unsal, M. S. (2025). Blockchain and stablecoin integration for crowdfunding: A framework for enhanced efficiency, security, and liquidity. *arXiv preprint arXiv:2501.11145*. https://doi.org/10.48550/arXiv.2501.11145",
        "Wang, T., Lin, Z., Düdder, B., et al. (2023). Linking souls to humans: Blockchain accounts with credible anonymity for Web 3.0 decentralized identity. *arXiv preprint arXiv:2301.02102*. https://doi.org/10.48550/arXiv.2301.02102",
        "Yang, H., et al. (2023). Enhancing SCF with privacy-preserving and splitting-enabled e-bills on blockchain. *arXiv preprint arXiv:2308.10020*. https://doi.org/10.48550/arXiv.2308.10020",
        "Zhang, R., Xue, R., & Liu, L. (2019). Security and privacy on blockchain. *ACM Computing Surveys*, 52(3), 1–34. https://doi.org/10.1145/3316481",
        "Zhou, Y., Lei, H., & Bao, Z. (2024). Eisdspa: An efficient and secure blockchain-based donation scheme with privacy protection and auditability. *IEEE Open Journal of the Communications Society*, 5, 7498–7510. https://doi.org/10.1109/OJCOMS.2024.3504403"
    ]
    
    for ref in references:
        p_ref = doc.add_paragraph(style='Body Text')
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Pt(26.5 + 28.35) # 54.85 pt (hanging indent 1 cm inside text column)
        p_ref.paragraph_format.right_indent = Pt(31.8)        # 637 dxa
        p_ref.paragraph_format.first_line_indent = Pt(-28.35) # -1.0 cm, so first line starts at 26.5 pt flush with Heading 1
        p_ref.paragraph_format.space_before = Pt(1)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.15
        
        runs = parse_markdown_runs(ref)
        for t, is_bold, is_italic in runs:
            r = p_ref.add_run(t)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            force_black_color(r)
            if is_bold:
                r.bold = True
            if is_italic:
                r.italic = True
            else:
                force_no_italic(r)
                
    print(f"Saving final manuscript to {output_path}...")
    try:
        doc.save(output_path)
        print(f"SUCCESS: Manuscript saved to {output_path}")
    except PermissionError:
        alt_path = 'assets/jurnal/JURNAL_SIMASI_TRUSTGIVE_UPDATED.docx'
        print(f"NOTICE: {output_path} is currently locked by Word. Saving to {alt_path}...")
        doc.save(alt_path)
        print(f"SUCCESS: Manuscript saved to {alt_path}")

if __name__ == '__main__':
    build_manuscript()
