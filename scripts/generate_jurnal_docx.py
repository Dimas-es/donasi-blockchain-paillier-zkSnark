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
    # CRITICAL: Preserve native headers & footers from template! DO NOT CLEAR THEM!
    for sec in doc.sections:
        sec.top_margin = Cm(2.54)
        sec.bottom_margin = Cm(2.54)
        sec.left_margin = Cm(2.54)
        sec.right_margin = Cm(2.54)
    
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

    def add_email(text):
        p = doc.add_paragraph(style='Body Text')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.right_indent = Pt(4.75)
        
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        force_black_color(r)
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
    add_email("Email: dimaasadjy@gmail.com1, alam@unsil.ac.id2")
    add_blank(space_pt=3)
    
    # 5. Abstract (English) - Exactly ~140 words to fit Page 1 perfectly
    add_abstract_header("ABSTRACT", is_italic=True)
    add_abstract_body(
        "Public philanthropic platforms face a persistent tension between public auditability and donors' financial privacy. "
        "While blockchain ledgers offer tamper-resistant donation records, publishing plaintext donation amounts triggers "
        "financial profiling and deanonymization risks. This paper presents the design and empirical evaluation of TrustGive, "
        "a hybrid decentralized donation prototype integrating Paillier Additive Homomorphic Encryption (AHE), Groth16 zk-SNARK, "
        "and Ethereum smart contracts. Individual donations are encrypted off-chain via Paillier and aggregated through modular multiplication, "
        "while validity is verified on-chain via zero-knowledge range proofs over the BN254 curve without exposing plaintext values. "
        "Empirical evaluations demonstrate that Groth16 verification consumes 225,035 gas, while on-chain recording consumes 613,607 to "
        "959,421 gas (optimizable to ~270,000 gas via event logs). Off-chain addition takes 0.035 ms and proof generation requires 1.35 s, "
        "achieving an end-to-end latency of ~3.45 s under an honest-but-curious threat model.",
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
        "nilai rahasia. Pengujian empiris membuktikan verifikasi Groth16 mengonsumsi 225.035 gas, sedangkan pencatatan on-chain memerlukan "
        "613.607 hingga 959.421 gas (dapat dioptimasi ke ~270.000 gas via event log). Agregasi off-chain memerlukan 0,035 ms dan "
        "pembentukan bukti ZK 1,35 detik, menghasilkan latensi end-to-end ~3,45 detik di bawah model ancaman honest-but-curious.",
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
        "administratif, serta kerentanan manipulasi pelaporan keuangan oleh entitas pengelola terpusat (Nairi et al., 2024). Munculnya teknologi buku "
        "besar terdistribusi (*distributed ledger technology* / blockchain) menawarkan paradigma baru dalam akuntabilitas donasi digital, di mana "
        "setiap transaksi dicatat secara permanen, dapat diaudit oleh publik, dan dieksekusi secara deterministik oleh kontrak pintar (*smart contracts*) "
        "tanpa bergantung pada perantara tunggal (Almaghrabi & Alhogail, 2022; Saraswat et al., 2022)."
    )
    
    add_body_p(
        "Namun demikian, transparansi absolut yang inheren pada jaringan blockchain publik memicu paradoks privasi yang serius. "
        "Setiap data transaksi finansial yang dipublikasikan secara terbuka (*plaintext*) ke dalam buku besar publik memungkinkan pihak ketiga "
        "melakukan analisis grafik transaksi, penelusuran identitas (*deanonymization*), hingga pemrofilan status ekonomi donatur secara tidak etis "
        "(Bünz et al., 2020). Donatur yang menyumbangkan dana dalam nominal besar rentan menjadi target eksploitasi finansial dan kejahatan siber, "
        "sementara donatur yang menyumbang dalam jumlah kecil dapat merasa enggan berpartisipasi akibat stigma sosial dan ketimpangan eksposur finansial "
        "(Zhou et al., 2024). Di samping itu, regulasi perlindungan data pribadi global seperti *General Data Protection Regulation* (GDPR) (Babel & Sedlmeir, 2023) "
        "maupun regulasi nasional di Indonesia, yaitu Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP), secara tegas mewajibkan "
        "kepatuhan terhadap prinsip minimisasi data (*data minimization*) dan pelindungan data keuangan pribadi dari publikasi tanpa persetujuan. "
        "Akibatnya, arsitektur sistem informasi donasi modern dituntut untuk mampu menyelaraskan dua kebutuhan: menjamin auditabilitas komitmen donasi secara "
        "permanen di satu sisi, sekaligus melindungi kerahasiaan nominal donasi individual dari pengamatan publik (Wang et al., 2023)."
    )
    
    add_body_p(
        "Untuk menjawab tantangan tersebut, berbagai penelitian mengusulkan teknik kriptografi privasi seperti enkripsi homomorfik (*Homomorphic Encryption* / HE) "
        "dan pembuktian tanpa pengetahuan (*Zero-Knowledge Proofs* / ZKP) (Lavin et al., 2024; Sameera et al., 2024; Burgos & Alchieri, 2025). Kriptosistem Paillier "
        "merupakan skema enkripsi asimetris dengan sifat homomorfik aditif (*Additive Homomorphic Encryption* / AHE), di mana perkalian antara dua *ciphertext* "
        "pada ruang modulus n² secara matematis menghasilkan enkripsi dari penjumlahan nilai *plaintext*-nya tanpa membuka isi pesan (Paillier, 1999; Yang et al., 2023; Damle et al., 2021). "
        "Sifat ini memungkinkan akumulasi saldo donasi kampanye secara inkremental tanpa mendekripsi masing-masing sumbangan. Sementara itu, zk-SNARK protokol Groth16 "
        "(Groth, 2016) memungkinkan pembuktian keabsahan suatu pernyataan komputasi—seperti nominal donasi berakar pada rentang positif dan tidak melampaui pagu kampanye—secara "
        "ringkas (*succinct*) dan terverifikasi secara on-chain tanpa membocorkan nilai rahasia (Christ et al., 2024; Morais et al., 2020)."
    )
    
    add_body_p(
        "Kombinasi antara HE dan zk-SNARK pada kontrak pintar telah dieksplorasi secara teoretis dalam beberapa literatur, seperti protokol ZeeStar (Steffen et al., 2022) "
        "dan Cloak (Ren et al., 2021). Namun, implementasi praktis sistem donasi terdesentralisasi yang mengintegrasikan kedua teknik ini pada arsitektur perangkat lunak "
        "dunia nyata menghadapi sejumlah tantangan berat:"
    )
    
    add_list_item("1.", "**Beban Komputasi On-Chain:** Mengeksekusi pembuktian dan agregasi seutuhnya di atas EVM (*fully on-chain*) sangat mahal dalam konsumsi gas dan latensi (Habib Nayan, 2025; Quintero-Narvaez et al., 2023).")
    add_list_item("2.", "**Kegagalan Konsistensi Data (Dual-Write Problem):** Memindahkan beban komputasi ke ranah off-chain menimbulkan risiko desinkronisasi antara status basis data relasional dan status transaksi blockchain saat terjadi gangguan jaringan (*RPC timeout* atau kegagalan transaksi) (Zhang et al., 2019).")
    add_list_item("3.", "**Kesenjangan Pengikatan Kriptografis (Binding Gap):** Paillier dengan modulus 2048-bit memiliki ukuran modulus yang besar sehingga memerlukan dekomposisi non-native field pada sirkuit SNARK berbasis kurva BN254. Mengintegrasikan bukti ZK dengan *ciphertext* Paillier secara terpisah rentan menyisakan celah substitusi nilai jika tidak diikat secara kriptografis (Chaliasos et al., 2024).")
    
    add_body_p(
        "Berdasarkan latar belakang dan identifikasi masalah di atas, penelitian ini merumuskan tiga pertanyaan penelitian (*research questions*):"
    )
    add_list_item("1.", "**RQ1:** Bagaimana merancang arsitektur hibrida yang membagi beban komputasi privasi donasi antara *off-chain* (Paillier AHE) dan *on-chain* (zk-SNARK Groth16) secara efisien pada EVM?")
    add_list_item("2.", "**RQ2:** Berapa profil konsumsi gas EVM dan latensi komputasi aktual dari integrasi zk-SNARK dan Paillier pada prototipe sistem donasi terdesentralisasi?")
    add_list_item("3.", "**RQ3:** Bagaimana menjamin verifikasi audit publik atas total saldo terdekripsi tanpa mengekspos nominal individual donatur di bawah model ancaman terdelegasi?")
    
    add_body_p(
        "Sejalan dengan rumusan masalah tersebut, penelitian ini bertujuan untuk merancang, mengimplementasikan, dan mengevaluasi kinerja prototipe sistem donasi terdesentralisasi "
        "hibrida (*TrustGive*) yang memadukan enkripsi homomorfik Paillier dan zk-SNARK Groth16 guna mencapai efisiensi biaya gas on-chain, menjamin integritas rentang donasi, "
        "serta memetakan batasan keamanan dan privasi arsitektur secara transparan. Kontribusi penelitian ini terfokus pada: (1) perancangan arsitektur hibrida 3-layer yang "
        "membagi beban komputasi antara backend Go, basis data PostgreSQL dengan pola *transactional idempotency & reconciliation worker*, dan kontrak pintar Solidity EVM; "
        "(2) evaluasi empiris konsumsi gas dan latensi komputasi terukur pada mesin terdedikasi; serta (3) pemetaan batasan keamanan arsitektur saat ini (model server *honest-but-curious*, "
        "*proof-to-ciphertext binding gap*, dan kontrol akses) beserta rumusan verifikasi total agregat tanpa kustodian kunci."
    )
    
    add_body_p(
        "Beberapa sistem donasi berbasis blockchain terdahulu telah diusulkan dalam literatur, antara lain UpHaaR (Saraswat et al., 2022), Astraea (Li et al., 2023), "
        "He et al. (2024), Eisdspa (Zhou et al., 2024), dan ZeeStar (Steffen et al., 2022). Tabel 1 merangkum perbandingan komparatif berbasis properti teknis antara sistem-sistem tersebut dengan prototipe TrustGive."
    )
    
    # Table 1: Comparative Table
    tbl1_headers = ["Sistem / Literatur", "Kerahasiaan Nominal Operator", "Verifikasi Publik Total", "Anonimitas Donatur On-Chain", "Estimasi Biaya Gas EVM", "Asumsi Kepercayaan / Setup", "Sumber Rujukan"]
    tbl1_rows = [
        ["**UpHaaR**", "Tidak (Plaintext)", "Ya (On-chain state)", "Rendah (Alamat wallet publik)", "Rendah (~45.000 gas)", "Konsorsium semi-tepercaya; IPFS hash", "Saraswat et al. (2022)"],
        ["**Astraea**", "Ya (Relayer ZK)", "Ya (Kontrak privat)", "Tinggi (Linkable ring signature)", "Sangat Tinggi (>1.200.000 gas)", "Trusted setup SNARK; relayer pool", "Li et al. (2023)"],
        ["**He et al.**", "Ya (SE index)", "Tidak (Rekonstruksi server)", "Sedang (Tersamarkan indeks)", "Sedang (~120.000 gas)", "Server indeks pencarian tepercaya", "He et al. (2024)"],
        ["**Eisdspa**", "Ya (Pedersen)", "Ya (Penjumlahan homomorfik)", "Tinggi (Linkable ring signature)", "Tinggi (~650.000 gas)", "Kurva standar; tanpa trusted setup", "Zhou et al. (2024)"],
        ["**ZeeStar**", "Ya (ElGamal)", "Terbatas (BSGS ≤ 2⁴⁰)", "Sedang (Stealth address)", "Tinggi (>800.000 gas)", "Universal CRS setup; ZK verifier", "Steffen et al. (2022)"],
        ["**TrustGive** *(Prototipe ini)*", "Tidak (Delegated Prover)", "Ya (Verifikasi opening (M, R))", "Sedang (Pseudonim wallet)", "613.607 gas (Uji) / 959.421 gas (Biner)", "Single-party setup; server HbC", "Penelitian ini"]
    ]
    tbl1_widths = [Cm(2.0), Cm(2.2), Cm(2.1), Cm(2.3), Cm(2.4), Cm(2.8), Cm(2.2)]
    tbl1_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    add_custom_table("Tabel 1. Tinjauan Komparatif Properti Sistem Donasi Terdesentralisasi Terkait", tbl1_headers, tbl1_rows, tbl1_widths, tbl1_aligns, font_size_pt=8.5)
    
    # 8. METODE PENELITIAN
    add_h1("METODE PENELITIAN")
    add_body_p(
        "Penelitian ini dilaksanakan menggunakan metode rekayasa perangkat lunak eksperimental (*experimental systems engineering*) "
        "yang memadukan perancangan matematis kriptografi, rekayasa sirkuit zero-knowledge, implementasi kontrak pintar, dan benchmark empiris terdedikasi. "
        "Alur metodologi penelitian mencakup 5 tahapan utama: perancangan arsitektur dan pemodelan ancaman, formulasi kriptografi Paillier, sintesis sirkuit Groth16, "
        "implementasi kontrak pintar EVM, serta perancangan basis data relasional dengan mekanisme keandalan state."
    )
    
    add_h2("1. Arsitektur Hibrida Sistem dan Model Ancaman Formal")
    add_body_p(
        "TrustGive mengimplementasikan arsitektur komputasi terdistribusi hibrida 3-layer yang membagi tugas komputasi dan penyimpanan secara optimal: "
        "(1) *Client Layer* (Next.js) sebagai antarmuka donatur dan penggalang dana; (2) *Off-Chain Backend Layer* (Go Fiber, PostgreSQL, SnarkJS) "
        "yang menangani pembentukan saksi (*witness generation*), komputasi pembuktian bukti ZK secara terdelegasi (*delegated prover*), enkripsi Paillier, "
        "serta akumulasi homomorfik; dan (3) *On-Chain Blockchain Layer* (Hardhat EVM Localhost) yang mengeksekusi kontrak pintar verifikasi dan pencatatan. "
        "Arsitektur terintegrasi disajikan pada Gambar 1."
    )
    add_figure("assets/gambar/gambar1_arsitektur_sistem.png", "Gambar 1. Arsitektur Hibrida Sistem Donasi Terdesentralisasi TrustGive", width_cm=13.5)
    
    add_body_p(
        "Tabel 2 mendefinisikan model ancaman formal sistem, membedakan antara asumsi operasional normal (Honest-but-Curious) dan batas kerentanan arsitektural terhadap penyerang aktif (Malicious)."
    )
    tbl2_headers = ["Komponen / Entitas", "Model Ancaman Asumsi", "Kemampuan Serangan / Akses", "Mekanisme Mitigasi Arsitektur", "Keterbatasan Terbuka (Residual Risk)"]
    tbl2_rows = [
        ["**Server Backend**", "Honest-but-Curious", "Membaca memori proses, dekripsi nominal individual via private key", "Audit log terdistribusi, isolasi proses enkripsi", "Single point of trust untuk privasi nominal terhadap operator"],
        ["**Donatur Malicious**", "Active Adversary", "Mengirimkan nominal negatif, nominal di atas pagu, bukti ZK palsu", "Sirkuit Groth16 non-malleability, verifikasi on-chain EVM", "Kerahasiaan terjamin selama soundess BN254 terpenuhi"],
        ["**Pengamat Publik / Verifier**", "Passive Adversary", "Analisis buku besar on-chain, event logs, analisis grafik transaksi", "Enkripsi ciphertext Paillier 2048-bit, komitmen Poseidon", "Analisis metadata transaksi (alamat wallet donatur publik)"],
        ["**Penggalang Dana (Beneficiary)**", "Honest-but-Curious", "Melihat saldo terkumpul, klaim pencairan dana kampanye", "Pencairan terikat pada verifikasi pembuktian opening total", "Tidak dapat melihat pemecahan nominal per donatur"]
    ]
    tbl2_widths = [Cm(2.6), Cm(2.4), Cm(3.2), Cm(3.4), Cm(4.4)]
    tbl2_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    add_custom_table("Tabel 2. Model Ancaman Formal dan Batas Keamanan Prototipe TrustGive", tbl2_headers, tbl2_rows, tbl2_widths, tbl2_aligns, font_size_pt=8.5)
    
    add_h2("2. Formulasi Kriptografi Paillier AHE dan Analisis Komparatif")
    add_body_p(
        "Kriptosistem Paillier dievaluasi secara matematis untuk menangani akumulasi saldo terenkripsi. Pasangan kunci dibangkitkan dari dua bilangan prima besar p dan q "
        "yang dirahasiakan, dengan modulus n = p · q berukuran 2048-bit dan λ = lcm(p-1, q-1). Enkripsi nominal donasi m ∈ ℤ_n dilakukan dengan memilih bilangan acak r ∈ ℤ*_n secara independen:"
    )
    add_body_p("c = g^m · r^n mod n²")
    add_body_p(
        "Sifat aditif homomorfik memungkinkan perkalian dua ciphertext c₁ dan c₂ menghasilkan ciphertext dari penjumlahan pesan m₁ + m₂:"
    )
    add_body_p("c_total = c₁ · c₂ mod n² = (g^(m₁) · r₁^n) · (g^(m₂) · r₂^n) = g^(m₁ + m₂) · (r₁ · r₂)^n mod n²")
    add_body_p(
        "Perkalian modular ini dieksekusi secara off-chain oleh backend server Go dengan kompleksitas waktu O(1) BigInt, meniadakan beban komputasi eksponensiasi modular on-chain pada EVM."
    )
    
    add_h2("3. Perancangan Sirkuit ZK-SNARK dan Soundness Komparator")
    add_body_p(
        "Sirkuit ZK dirancang menggunakan bahasa Circom (Muñoz-Tapia et al., 2022) dan dikompilasi ke dalam sistem pembuktian Groth16 (Groth, 2016) di atas kurva BN254. "
        "Sirkuit membuktikan bahwa nilai donasi amount berada pada rentang positif (amount > 0) dan tidak melampaui sisa pagu target (amount ≤ maxCap). "
        "Pemeriksaan non-negativitas dikonstruksi melalui dekomposisi biner Num2Bits(64), menjamin ketiadaan celah pembungkusan modulus field (modulo underflow). "
        "Untuk mengikat bukti pada identitas kampanye, sirkuit menghitung komitmen hash Poseidon publik (Grassi et al., 2021):"
    )
    add_body_p("commitment = Poseidon(amount, donorSecret, campaignId)")
    
    add_h2("4. Perancangan Kontrak Pintar Solidity EVM")
    add_body_p(
        "Kontrak pintar TrustGive.sol diimplementasikan pada Solidity 0.8.20 dengan mengintegrasikan verifier Groth16 hasil ekspor SnarkJS. "
        "Fungsi donateVerify() menerima bukti proof (titik kurva A ∈ 𝔾₁, B ∈ 𝔾₂, C ∈ 𝔾₁) dan input publik, memverifikasi keabsahannya via EVM pairing precompile (0x08). "
        "Setelah verifikasi berhasil, kontrak mencatat hash komitmen ke dalam storage on-chain."
    )
    
    add_h2("5. Perancangan Model Data Relasional (ERD) dan Alur Bisnis")
    add_body_p(
        "Basis data relasional PostgreSQL dirancang untuk mengelola status transaksi dan data kampanye. Skema ERD terdiri dari 5 entitas utama: "
        "`users`, `campaigns`, `donations`, `campaign_aggregates`, dan `idempotency_keys` (Gambar 2). Relasi 1:N menghubungkan `users` dengan `campaigns` "
        "dan `donations`. Entitas `campaign_aggregates` berelasi 1:1 dengan `campaigns`, menyimpan akumulasi ciphertext Paillier yang diperbarui melalui row-level locking "
        "(`SELECT FOR UPDATE`) guna mencegah race condition. Entitas `idempotency_keys` menjamin deduplikasi transaksi donasi."
    )
    add_figure("assets/gambar/gambar2_erd_database.png", "Gambar 2. Diagram Relasi Entitas (ERD) Model Data Sistem", width_cm=13.5)
    
    add_body_p(
        "Alur transaksi donasi end-to-end, siklus hidup kampanye, dan pola rekonsiliasi state diilustrasikan berturut-turut pada Gambar 3, Gambar 4, dan Gambar 5."
    )
    add_figure("assets/gambar/gambar3_workflow_donasi.png", "Gambar 3. Diagram Alur Transaksi Donasi End-to-End", width_cm=14.0)
    add_figure("assets/gambar/gambar7_lifecycle_kampanye.png", "Gambar 4. Siklus Hidup dan Status Kampanye Donasi", width_cm=13.0)
    add_figure("assets/gambar/gambar5_alur_idempotensi_recovery.png", "Gambar 5. Alur Logika Idempotensi dan Rekonsiliasi State Transaksi", width_cm=13.5)
    
    # 9. HASIL DAN PEMBAHASAN
    add_h1("HASIL DAN PEMBAHASAN")
    add_body_p(
        "Evaluasi kinerja empiris prototipe TrustGive dilaksanakan pada lingkungan pengujian terdedikasi dengan spesifikasi: "
        "prosesor Intel Core i5-8250U (4 core, 8 thread, 1,60 GHz up to 3,40 GHz), RAM 8 GB DDR4, SSD NVMe 512 GB, sistem operasi Windows 11 Home 64-bit, "
        "Go versi 1.22.0, Node.js versi 20.11.0, Circom 2.1.6, SnarkJS 0.7.3, Hardhat EVM (Cancun hardfork, block gas limit 30.000.000 gas, 0 gwei basefee). "
        "Pengujian mencakup profil konsumsi gas EVM, waktu komputasi kriptografi, latensi transaksi end-to-end, serta pengujian keandalan konkurensi."
    )
    
    add_h2("1. Profil Konsumsi Gas Kontrak Pintar pada EVM dan Rekonsiliasi Storage")
    add_body_p(
        "Konsumsi gas EVM diukur secara presisi untuk setiap fungsi smart contract TrustGive.sol menggunakan Hardhat EVM tracer (Tabel 3 dan Gambar 6). "
        "Verifikasi pairing Groth16 mandiri memerlukan 225.035 gas. Transaksi pencatatan donasi lengkap on-chain membutuhkan 613.607 gas (muatan uji string 32-byte) "
        "hingga 959.421 gas (muatan biner Paillier 512-byte penuh). Tingginya konsumsi gas pada muatan biner disebabkan oleh alokasi 16 slot SSTORE berturut-turut (320.000 gas) "
        "dan eksekusi operasi MSTORE/SHA3 byte copy. Berdasarkan kalkulasi arsitektural, pengalihan ciphertext ke event logs menghemat konsumsi gas hingga ~270.000 gas per transaksi."
    )
    
    tbl3_headers = ["Operasi Kontrak Pintar", "Metode Eksekusi", "Konsumsi Gas (Actual)", "Gas Limit EVM", "% Batas Blok", "Rincian Alokasi Komputasi / Storage"]
    tbl3_rows = [
        ["**Deploy Verifier Groth16**", "Contract Creation", "594.137", "30.000.000", "1,98%", "Inisialisasi konstanta pairing IC[], curve precompile"],
        ["**Deploy TrustGive Main**", "Contract Creation", "1.845.220", "30.000.000", "6,15%", "Penyimpanan bytecode, mapping roles, address linkage"],
        ["**Create Campaign**", "`createCampaign()`", "148.912", "30.000.000", "0,50%", "SSTORE metadata target, pagu maxCap, beneficiary"],
        ["**Groth16 Verify Only**", "`verifyProof()`", "225.035", "30.000.000", "0,75%", "Precompile staticcall: 4 pairing checks kurva BN254"],
        ["**Donate Verify (Compact)**", "`donateVerify()`", "613.607", "30.000.000", "2,05%", "Pairing check (225k) + SSTORE komitmen + transfer"],
        ["**Donate Verify (Full 512B)**", "`donateVerify()`", "959.421", "30.000.000", "3,20%", "Pairing + 16 slot SSTORE ciphertext (320k) + MSTORE"],
        ["**Finalize Campaign**", "`finalize()`", "72.450", "30.000.000", "0,24%", "Perubahan status kampanye, transfer dana terkumpul"],
        ["**Optimasi Event Log (Proyeksi)**", "`donateOptimized()`", "~270.000", "30.000.000", "0,90%", "Estimasi kalkulasi: pairing (225k) + LOG3 event data"]
    ]
    tbl3_widths = [Cm(3.0), Cm(2.4), Cm(1.9), Cm(1.9), Cm(1.4), Cm(5.4)]
    tbl3_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.LEFT]
    add_custom_table("Tabel 3. Profil Konsumsi Gas Kontrak Pintar pada EVM Hardhat (Terukur dan Terproyeksi)", tbl3_headers, tbl3_rows, tbl3_widths, tbl3_aligns, font_size_pt=8.5)
    add_figure("assets/jurnal/grafik_konsumsi_gas.png", "Gambar 6. Profil Konsumsi Gas Kontrak Pintar pada EVM Hardhat", width_cm=14.0)
    
    add_h2("2. Evaluasi Waktu Komputasi Kriptografi dan Latensi End-to-End")
    add_body_p(
        "Waktu eksekusi operasi kriptografi dievaluasi secara statistik melalui 100 iterasi terstandarisasi (Tabel 4). "
        "Hasil pengukuran membuktikan bahwa operasi perkalian homomorfik Paillier sangat efisien (0,035 ± 0,003 ms), memungkinkan server mengeksekusi "
        "hingga ~28.200 agregasi per detik. Waktu pembuktian saksi Circom membutuhkan 185,20 ± 12,40 ms dan pembentukan bukti Groth16 memerlukan 1.350,40 ± 45,60 ms."
    )
    
    tbl4_headers = ["Tahapan Operasi Komputasi", "Pustaka / Algoritma", "Ukuran Parameter", "Rata-rata ± SD (ms)", "Min – Maks (ms)", "Kompleksitas Asimtotik"]
    tbl4_rows = [
        ["**KeyGen Paillier**", "Go `crypto/rand`", "Modulus 2048-bit", "720,94 ± 24,10", "695,20 – 765,80", "O(k⁴) bit operations"],
        ["**Enkripsi Paillier**", "Go `big.Int` modular", "m, r ∈ ℤ_n (2048-bit)", "36,35 ± 1,82", "34,10 – 39,80", "O(k³) modular exponentiation"],
        ["**Penjumlahan Homomorfik**", "Go `Mul(c₁, c₂) mod n²`", "Ciphertext 4096-bit", "0,035 ± 0,003", "0,031 – 0,042", "O(k²) modular multiplication"],
        ["**Dekripsi Paillier**", "Go `L(c^λ mod n²) · μ`", "Private key λ, μ (2048-bit)", "40,13 ± 2,14", "37,90 – 44,20", "O(k³) modular exponentiation"],
        ["**Pembangkitan Saksi (Witness)**", "Circom C++ WitnessCalc", "1.240 R1CS constraints", "185,20 ± 12,40", "168,40 – 205,30", "O(C) linear to constraints"],
        ["**Pembangkitan Bukti (Proof)**", "SnarkJS Groth16 Prover", "BN254 curve, zkey setup", "1.350,40 ± 45,60", "1.280,00 – 1.440,00", "O(C log C) MSM multi-exponentiation"],
        ["**Verifikasi Bukti Lokal**", "SnarkJS Verifier", "Input publik + proof (A, B, C)", "1.850,10 ± 52,30", "1.760,00 – 1.960,00", "O(1) pairing check BN254"],
        ["**Verifikasi Pairing On-Chain**", "EVM Precompile 0x08", "BN254 pairing (225.035 gas)", "35,40 ± 4,20", "30,10 – 42,50", "O(1) deterministik EVM"]
    ]
    tbl4_widths = [Cm(3.2), Cm(2.6), Cm(2.5), Cm(2.4), Cm(2.4), Cm(3.1)]
    tbl4_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    add_custom_table("Tabel 4. Evaluasi Waktu Komputasi Kriptografi Terstandarisasi (100 Iterasi)", tbl4_headers, tbl4_rows, tbl4_widths, tbl4_aligns, font_size_pt=8.0)
    
    add_body_p(
        "Distribusi latensi transaksi donasi sekuensial end-to-end terukur rata-rata ~3,45 detik, di mana fase pembuktian bukti ZK menyumbang 44,5% dari total durasi (Gambar 7)."
    )
    add_figure("assets/jurnal/grafik_latensi_e2e.png", "Gambar 7. Distribusi Komponen Latensi End-to-End Transaksi Donasi Sekuensial", width_cm=14.0)
    
    add_h2("3. Matriks Pengujian Fungsional, Keandalan, dan Pemetaan Keterbatasan")
    add_body_p(
        "Tabel 5 menyajikan hasil evaluasi pengujian fungsional dan pemetaan batasan keamanan prototipe."
    )
    tbl5_headers = ["Skenario Pengujian", "Ekspektasi Sistem", "Hasil Terukur Aktual", "Status", "Keterbatasan Terbuka (Residual Risk)"]
    tbl5_rows = [
        ["**Donasi Nominal Valid**", "Witness sah, bukti terverifikasi on-chain", "Pairing lolos, gas 613.607 terpotong, state tersimpan", "SUKSES", "Tidak ada celah fungsional"],
        ["**Donasi Nilai Negatif**", "Ditolak saat kompilasi witness Circom", "Assert violation pada Num2Bits(64), bukti gagal dibuat", "SUKSES", "Tervalidasi secara matematis"],
        ["**Donasi Melampaui Cap**", "Ditolak saat kompilasi witness Circom", "Assert violation pada LessEqThan(64), bukti gagal dibuat", "SUKSES", "Pagu kampanye terjaga"],
        ["**Proof Input Malleability**", "Ditolak oleh kontrak pintar EVM", "Pairing check gagal, transaksi revert `Invalid Proof`", "SUKSES", "Soundness BN254 terverifikasi"],
        ["**Pengujian Konkurensi (Race)**", "Saldo agregat akurat, tidak ada record ganda", "Row-level locking (`FOR UPDATE`) menjamin konsistensi", "SUKSES", "Throughput terbatas pada lock DB"],
        ["**Deduplikasi Idempotensi**", "Transaksi kembar ditolak/diabaikan", "Unique index `idempotency_key` menolak duplikasi", "SUKSES", "Idempotensi lokal terverifikasi"],
        ["**Injeksi RPC Timeout**", "State DB direkonsiliasi otomatis", "Worker memulihkan status transaksi dalam interval polling", "SUKSES", "Latensi pemulihan terikat polling"],
        ["**Inspeksi Memori Server**", "Nominal plaintext seharusnya terisolasi", "Nilai terlihat pada buffer proses backend Go", "BATASAN", "Risiko HbC: operator dapat melihat nominal"],
        ["**Substitusi Ciphertext**", "Ciphertext seharusnya terikat pada proof", "Ciphertext dan proof diverifikasi secara independen", "BATASAN", "Binding gap: bukti tidak mengikat ciphertext"],
        ["**Klaim Dana Tanpa Verifier**", "Total saldo diverifikasi sebelum rilis", "Klaim bergantung pada transfer dana kontrak", "BATASAN", "Perlu protokol ZK aggregate opening"],
        ["**Serangan DDoS RPC Node**", "Transaksi tetap terproses", "Koneksi RPC timeout, penundaan antrean transaksi", "BATASAN", "Bergantung pada ketersediaan relayer/RPC"]
    ]
    tbl5_widths = [Cm(2.8), Cm(3.2), Cm(3.4), Cm(1.6), Cm(5.2)]
    tbl5_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    add_custom_table("Tabel 5. Matriks Hasil Pengujian Fungsional, Keandalan, dan Pemetaan Keterbatasan Sistem", tbl5_headers, tbl5_rows, tbl5_widths, tbl5_aligns, font_size_pt=8.0)
    
    add_h2("4. Analisis Keamanan, Batas Privasi, dan Diskusi Literatur")
    add_body_p(
        "Kombinasi Paillier AHE dan zk-SNARK Groth16 berhasil membagi beban komputasi secara efektif antara komputasi off-chain yang murah dan verifikasi on-chain yang ringkas. "
        "Namun, analisis keamanan membuktikan adanya 3 keterbatasan struktural utama pada implementasi saat ini: (1) *Server Honest-but-Curious*, di mana server backend memegang "
        "private key Paillier sehingga dapat melihat nominal individual donatur; (2) *Proof-to-Ciphertext Binding Gap*, di mana sirkuit Circom membuktikan keabsahan nilai komitmen "
        "Poseidon, namun tidak membuktikan bahwa nilai tersebut identik dengan muatan di dalam ciphertext Paillier 2048-bit; dan (3) *Ketiadaan Protokol Opening Terverifikasi*, di mana "
        "pencairan dana belum mengikutsertakan bukti ZK pembukaan nilai akumulasi total."
    )
    
    # 10. KESIMPULAN
    add_h1("KESIMPULAN")
    add_body_p(
        "Penelitian ini membuktikan kelayakan teknis perancangan prototipe sistem donasi terdesentralisasi hibrida (TrustGive) yang memadukan enkripsi homomorfik Paillier, "
        "zk-SNARK Groth16, dan kontrak pintar EVM. Evaluasi kinerja empiris menunjukkan bahwa verifikasi bukti ZK on-chain memerlukan 225.035 gas, sementara pencatatan transaksi "
        "membutuhkan 613.607 hingga 959.421 gas (dapat dioptimasi ke ~270.000 gas via event logs). Agregasi homomorfik off-chain berlangsung sangat cepat (0,035 ms), menghasilkan "
        "latensi transaksi end-to-end ~3,45 detik. Mekanisme transactional idempotency worker berhasil mengatasi risiko dual-write inconsistency dan race condition pada kondisi konkurensi."
    )
    
    add_body_p(
        "Secara praktis, prototipe ini menawarkan kerangka kerja implementasi bagi platform filantropi Web3 dalam memenuhi prinsip minimisasi data sesuai regulasi "
        "Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP). Secara teoretis, penelitian ini menyajikan baseline empiris komparasi beban komputasi dan pemetaan "
        "batasan keamanan arsitektur hibrida. Agenda penelitian lanjutan terfokus pada: (1) implementasi distributed key generation (DKG) atau multi-party computation (MPC) "
        "untuk meniadakan kustodian kunci tunggal; (2) perancangan sirkuit ZK non-native field guna menutup *binding gap*; serta (3) penerapan zk-Rollup (Layer-2) guna mereduksi biaya gas hingga <50.000 gas per transaksi."
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
        "Habib Nayan, M. A. (2025). Analyzing performance bottlenecks in zero-knowledge proof based rollups on Ethereum. *arXiv preprint arXiv:2503.22709*. https://doi.org/10.48550/arXiv.2503.22709",
        "He, B., Feng, T., Fang, J., Liu, C., & Su, C. (2024). A secure and efficient charitable donation system based on Ethereum blockchain and searchable encryption. *IEEE Transactions on Consumer Electronics*, 70(1), 2977–2987. https://doi.org/10.1109/TCE.2023.3323356",
        "Lavin, R., Liu, X., Mohanty, H., de la Rocha, A. S., & Xu, M. (2024). A survey on the applications of zero-knowledge proofs. *arXiv preprint arXiv:2408.00243*. https://doi.org/10.48550/arXiv.2408.00243",
        "Li, M., Chen, Y., Zhu, L., Zhang, Z., Ni, J., & Conti, M. (2023). Astraea: Anonymous and secure auditing based on private smart contracts for donation systems. *IEEE Transactions on Dependable and Secure Computing*, 20(4), 3002–3018. https://doi.org/10.1109/TDSC.2022.3204287",
        "Morais, E., Koens, T., van Wijk, C., & Koren, A. (2020). A survey on zero knowledge range proofs and applications. *arXiv preprint arXiv:1907.06381*. https://doi.org/10.48550/arXiv.1907.06381",
        "Muñoz-Tapia, J. L., Bellés-Muñoz, M., Isabel, M., & Rubio, A. (2022). CIRCOM: A robust and scalable language for building complex zero-knowledge circuits. *TechRxiv*, preprint. https://doi.org/10.36227/techrxiv.19374986.v1",
        "Nairi, C., Cicioğlu, M., & Çalhan, A. (2024). Smart blockchain networks: Revolutionizing donation tracking in the Web 3.0. *Computer Communications*, 228, 107981. https://doi.org/10.1016/j.comcom.2024.08.012",
        "Paillier, P. (1999). Public-key cryptosystems based on composite degree residuosity classes. *Advances in Cryptology – EUROCRYPT '99*, LNCS 1592, 223–238. https://doi.org/10.1007/3-540-48910-X_16",
        "Quintero-Narvaez, C. E., et al. (2023). Zero-knowledge proofs for questionnaire result verification in smart contracts. *arXiv preprint arXiv:2310.13618*. https://doi.org/10.48550/arXiv.2310.13618",
        "Ren, J., et al. (2021). Cloak: Enabling confidential smart contract with multi-party transactions. *arXiv preprint arXiv:2106.13926*. https://doi.org/10.48550/arXiv.2106.13926",
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
