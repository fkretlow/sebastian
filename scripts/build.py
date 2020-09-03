import json
from ffsmufl import SmuflFont

with open('./src/sebastian_defaults.json', 'r') as infile:
    defaults = json.load(infile)

with SmuflFont('./src/sebastian.ufo', 'r') as sebastian:
    sebastian.engraving_defaults = defaults
    sebastian.export_metadata('./build/sebastian.json')
    sebastian.export_font('./build/sebastian.otf')
