import xml.etree.ElementTree as ET
from .vars import routes, output_path, ncx, ncx_tree

ET.register_namespace('', 'http://www.daisy.org/z3986/2005/ncx/')

base:ET.Element = ET.Element('navMap')
count = 0

def createNavElement(element_data:str, parte=False):

    global count
    count += 1
    navItem = ET.Element('navPoint', {
            'id' : f'navPoint-{count}',
            'playOrder' : str(count)
        })
    
    label = ET.Element('navLabel')
    text_label = ET.Element('text')
    if not parte:
        text_label.text = str(element_data['nav_text']).replace('_', ' ')
    else:
        split_part_title = element_data['nav_text'].split(':')
        text_label.text = str(split_part_title[0]) + ' Parte:' + str(split_part_title[1])
    label.append(text_label)
    navItem.append(label)

    if not parte:
        content = ET.Element('content', {'src': f'Text/{element_data['path']}'})
    else:
        content = ET.Element('content', {'src': f'Text/Parte{element_data['nav_text'].split(':')[0]}.xhtml'})
    navItem.append(content)

    return navItem

def create_table_of_content():
    for key in routes:
        if key != 'parts' :
            for parafernalia in routes[key]:

                base.append(createNavElement(parafernalia))
        
        else :

            for part in routes[key]:

                partElement = createNavElement({'nav_text': part}, parte=True)

                for chapter in routes[key][part]:
                    chapterElement = createNavElement(chapter)
                    partElement.append(chapterElement)

                base.append(partElement)


    with open(f'{output_path}/OEBPS/toc.ncx', 'wb') as out:
        ncx.append(base)
        ET.indent(ncx_tree, '    ')
        out.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        out.write(b'<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" \n\t'
                    b'"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n\n')
        ncx_tree.write(out, 'utf-8')
        print('\nTabla de contenido')


