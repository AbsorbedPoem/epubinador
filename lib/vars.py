import xml.etree.ElementTree as ET
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

meta:dict
book_name:str
with open(f'{root_path}/meta.txt', 'r') as js:
    meta = json.load(js)
    book_name = meta['titulo'].title()