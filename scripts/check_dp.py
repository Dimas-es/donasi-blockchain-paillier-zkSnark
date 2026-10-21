import docx

doc = docx.Document('assets/template/TEMPLATE SIMASI CONTOH.docx')
body = doc._body._element
print('Total body elements:', len(body))
for idx, el in enumerate(body):
    if el.tag.endswith('p'):
        text = ''.join(el.itertext())
        if 'DAFTAR PUSTAKA' in text.upper():
            print(f'Found at body element {idx}: {text}')
            for j in range(idx+1, min(idx+20, len(body))):
                tag_name = body[j].tag.split('}')[-1]
                t = ''.join(body[j].itertext())[:90]
                print(f'  Elem {j} ({tag_name}): {t}')
