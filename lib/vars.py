import xml.etree.ElementTree as ET
import json
from docx import Document
import json


root_path = './Manuscrito'
output_path = './epub/raw/'


routes:dict = {
    'pre': [],
    'parts': {},
    'post': [],
}

ncx_tree:ET.ElementTree = ET.parse('./templates/toc.ncx')
ncx = ncx_tree.getroot()



meta:str = {}
book_name:str = ''

def setMeta():
    doc = Document(f'{root_path}/meta.docx')
    text_content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

    global meta
    meta = json.loads(text_content)
    global book_name
    book_name = meta['titulo'].title()