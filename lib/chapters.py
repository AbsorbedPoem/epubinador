from mammoth import convert_to_html
import xml.etree.ElementTree as ET
import os
from .vars import output_path, root_path, routes
import shutil


has_readed_chapters = False


def add_title_and_index(raw, title:str, index, is_chapter):
    if is_chapter:
        return b'<body>' + \
            b'<h3>' + bytes(str(index), encoding='utf-8') + b'</h3>' + \
            b'<h2>' + bytes(title.upper(), encoding='utf-8') + b'</h2>' + \
            raw + \
            b'</body>'
    else :
        if title not in ['Sinópsis', 'Dedicatoria', 'Detalles'] :
            return b'<body>' + \
                b'<h1>' + bytes(title.upper(), encoding='utf-8') + b'</h1>' + \
                raw + \
                b'</body>'
        else: return b'<body>' + raw + b'</body>'

def add_parafernalia_nav(parafernalia):

    global has_readed_chapters
    text_parafernalia = parafernalia[:-6]

    if not has_readed_chapters:
        routes['pre'].append({
            'path' : parafernalia,
            'nav_text' : text_parafernalia
        })
    else:
        routes['post'].append({
            'path' : parafernalia,
            'nav_text' : text_parafernalia
        })


def prepare_and_save_page(origin, is_chapter=True) -> str:

    ET.register_namespace('', 'http://www.w3.org/1999/xhtml')
    chapter = os.path.basename(origin)
    chapter_template:ET.ElementTree = ET.parse('./templates/chapter.xhtml')
    
    chapter_xml = chapter_template.getroot()
    number:int = int(chapter[:2]) if is_chapter else None
    title:str = chapter[4:-5]
    content:ET.Element

    with open(origin, 'rb') as f:
        raw = convert_to_html(f).value.encode('utf-8')
        raw = add_title_and_index(raw, title, number, is_chapter)
        raw = raw.replace(b'<p>#</p>', b'<hr />')

        content = ET.fromstring(bytes(raw))

    chapter_xml.find('{http://www.w3.org/1999/xhtml}head').\
    find('{http://www.w3.org/1999/xhtml}title').\
    text = title

    chapter_xml.append(content)

    save_name = f'Cap{number}.xhtml' if is_chapter else f'{title}.xhtml'
    save_name = save_name.replace(' ', '_')

    ET.indent(chapter_template, '    ')
    with open(f'{output_path}/OEBPS/Text/{save_name}', 'wb') as out:
        out.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        out.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" \n\t'
                b'"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n\n')
        chapter_template.write(out, 'utf-8')
    
    if is_chapter : print(number, title)
    else : print(title)

    return save_name


def prepare_part_page(number:str, title:str):
    ET.register_namespace('', 'http://www.w3.org/1999/xhtml')
    part_template:ET.ElementTree = ET.parse('./templates/part.xhtml')
    
    chapter_xml = part_template.getroot()

    chapter_xml.find('{http://www.w3.org/1999/xhtml}body').\
    find('{http://www.w3.org/1999/xhtml}h2').text = f'{number.upper()} PARTE'
    chapter_xml.find('{http://www.w3.org/1999/xhtml}body').\
    find('{http://www.w3.org/1999/xhtml}h1').text = title.upper()

    chapter_xml.find('{http://www.w3.org/1999/xhtml}head').\
    find('{http://www.w3.org/1999/xhtml}title').text = f'{number} Parte'


    save_name = f'Parte{number}.xhtml'

    ET.indent(part_template, '    ')
    with open(f'{output_path}/OEBPS/Text/{save_name}', 'wb') as out:
        out.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        out.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" \n\t'
                b'"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n\n')
        part_template.write(out, 'utf-8')
    
    print(f'{number} Parte')

    return save_name

def add_portada():
    shutil.copy('./templates/cubierta.xhtml', f'{output_path}OEBPS/Text/Portada.xhtml')
    routes['pre'].append({
        'path' : 'Portada.xhtml',
        'nav_text' : 'Portada'
    })
    print('Portada')

def add_presentacion():

    from .vars import meta, book_name

    ET.register_namespace('', 'http://www.w3.org/1999/xhtml')
    part_template:ET.ElementTree = ET.parse('./templates/presentacion.xhtml')
    
    chapter_xml = part_template.getroot()

    chapter_xml.find('{http://www.w3.org/1999/xhtml}body').\
    find('{http://www.w3.org/1999/xhtml}h1').text = book_name.upper()
    chapter_xml.find('{http://www.w3.org/1999/xhtml}body').\
    find('{http://www.w3.org/1999/xhtml}h4').text = meta['autor']


    ET.indent(part_template, '    ')
    with open(f'{output_path}/OEBPS/Text/Presentación.xhtml', 'wb') as out:
        out.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        out.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" \n\t'
                b'"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n\n')
        part_template.write(out, 'utf-8')
    
    routes['pre'].append({
        'path' : 'Presentación.xhtml',
        'nav_text' : 'Presentación'
    })
    print('Presentación')


def parse_chapters():

    add_portada()

    global has_readed_chapters

    for part in os.listdir(root_path):

        if os.path.isdir(f"{root_path}/{part}") and part != 'Parafernalia':

            part_number = part.split('.')[1].split(' ')[1]
            part_title = part.split('.')[2].strip()

            routes['parts'][f'{part_number}: {part_title}'] = []
            part_nav:list = routes['parts'][f'{part_number}: {part_title}']

            prepare_part_page(number=part_number, title=part_title)
            has_readed_chapters = True

            for chapter in os.listdir(f"{root_path}/{part}"):

                path = f"{root_path}/{part}/{chapter}"
                result_name = prepare_and_save_page(origin=path)
                
                part_nav.append({
                    'path' : result_name,
                    'nav_text' : str(int(chapter[:2])) + chapter[2:-5]
                })
                
        elif part[-5:] == '.docx':

            path = f"{root_path}/{part}"
            result_name = prepare_and_save_page(origin=path, is_chapter=False)

            add_parafernalia_nav(result_name)

            if part[4:] == 'Sinópsis.docx': add_presentacion()
        
        elif part == 'Portada.jpg':
            if os.path.isfile(f"{root_path}/Portada.jpg"):
                os.remove(f"{root_path}/Portada.jpg")
            shutil.copy(f"{root_path}/Portada.jpg", f"{output_path}/OEBPS/Images/Portada.jpg")
