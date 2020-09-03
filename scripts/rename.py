from ffsmufl import SmuflFont

with SmuflFont('./src/sebastian.ufo', 'w') as sebastian:
    sebastian.rename_glyphs()
    sebastian.export_font('./src/sebastian.ufo')
