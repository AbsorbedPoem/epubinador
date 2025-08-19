import xml.etree.ElementTree as ET


root_path = './Manuscrito'
output_path = './epub/raw/'


routes:dict = {
    'pre': [],
    'parts': {},
    'post': [],
}

ncx_tree:ET.ElementTree = ET.parse('./templates/toc.ncx')
ncx = ncx_tree.getroot()