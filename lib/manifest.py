import xml.etree.ElementTree as ET
from .vars import routes, output_path
import os


ET.register_namespace('', 'http://www.idpf.org/2007/opf')

content_opf = ET.parse('./templates/content.opf')
opf = content_opf.getroot()

manifest = opf.find('{http://www.idpf.org/2007/opf}manifest')
spine = opf.find('{http://www.idpf.org/2007/opf}spine')

def add_mani (x):
    manifest.append(ET.Element('item', {
        'id' : x,
        'href' : f'Text/{x}.xhtml',
        'media-type' : "application/xhtml+xml"
    }))
    spine.append(ET.Element('itemref', {
        'idref' : x
    }))

def create_manifest():
    for section in routes:
        if section == 'parts':
            for part in routes[section]:

                add_mani(f'Parte{part.split(':')[0]}')

                for chapter in routes[section][part]:
                    add_mani(chapter['path'][:-6])
        else:
            for parafernalia in routes[section]:
                add_mani(parafernalia['path'][:-6])

    for file in os.listdir(f'{output_path}/OEBPS/Styles'):
        mani = ET.Element('item', {
            'id' : file,
            'href' : f'Styles/{file}',
            'media-type' : "text/css"
        })
        manifest.append(mani)

    for file in os.listdir(f'{output_path}/OEBPS/Fonts'):
        mani = ET.Element('item', {
            'id' : file,
            'href' : f'Fonts/{file}',
            'media-type' : "font/ttf"
        })
        manifest.append(mani)

    for file in os.listdir(f'{output_path}/OEBPS/Images'):
        mani = ET.Element('item', {
            'id' : file,
            'href' : f'Images/{file}',
            'media-type' : "image/jpeg"
        })
        manifest.append(mani)
    
    with open(f'{output_path}/OEBPS/content.opf', 'wb') as out:
        ET.indent(content_opf, '    ')
        content_opf.write(out, 'utf-8')
        print('\nManifest')
