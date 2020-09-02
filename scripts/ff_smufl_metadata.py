#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The SmuflMetadata class defined in this module generates SMuFL metadata
from fontforge.font objects by inspecting their glyphs and OpenType lookups.

A copy of the glyphnames.json file from the SMuFL specification must be
saved in the same folder for this to work. Download it from here:
    https://github.com/w3c/smufl/tree/gh-pages/metadata

A basic script is included below. If all you need is a metadata json file
for your music font, copy this file and glyphnames.json to the folder
where your font is saved and edit the ENGRAVING_DEFAULTS dictionary below
as needed. Then run the script with a Python 3 interpreter that has access
to the fontforge module, e.g.:
    ffpython smufl_metadata.py myfont.sfd

If you need to generate metadata files as part of a more involved scripted
procedure, import the SmuflMetadata class to your script.

Supported tables:
SMuFL table           | source
----------------------+---------------------------------
fontName              | Font Info Dialog
fontVersion           | Font Info Dialog
engravingDefaults     | defined below
glyphsWithAnchors     | anchor points
glyphsWithAlternates  | alternate substitution lookups
glyphBBoxes           | glyph contours
ligatures             | ligature lookups

Written by Florian Kretlow. Use, distribute and edit this file as you wish.
"""
import io, json


# Set these values as needed for your font project:
ENGRAVING_DEFAULTS = {
    'arrowShaftThickness'        : 0.16,
    'barlineSeparation'          : 0.6,
    'beamSpacing'                : 0.33,
    'beamThickness'              : 0.5,
    'bracketThickness'           : 0.5,
    'dashedBarlineDashLength'    : 0.67,
    'dashedBarlineGapLength'     : 0.67,
    'dashedBarlineThickness'     : 0.16,
    'hairpinThickness'           : 0.16,
    'legerLineExtension'         : 0.4,
    'legerLineThickness'         : 0.1875,
    'lyricLineThickness'         : 0.1,
    'octaveLineThickness'        : 0.1875,
    'pedalLineThickness'         : 0.16,
    'repeatBarlineDotSeparation' : 0.16,
    'repeatEndingLineThickness'  : 0.16,
    'slurEndpointThickness'      : 0.125,
    'slurMidpointThickness'      : 0.25,
    'staffLineThickness'         : 0.125,
    'stemThickness'              : 0.125,
    'subBracketThickness'        : 0.16,
    'textEnclosureThickness'     : 0.16,
    'thickBarlineThickness'      : 0.5,
    'thinBarlineThickness'       : 0.16,
    'tieEndpointThickness'       : 0.125,
    'tieMidpointThickness'       : 0.2,
    'tupletBracketThickness'     : 0.125,
}


# SMuFL data
SMUFL_ANCHOR_NAMES = (
    'stemUpSE',
    'stemUpNW',
    'stemDownNW',
    'stemDownSW',
    'splitStemUpSE',
    'splitStemUpSW',
    'splitStemDownNE',
    'splitStemDownNW',
    'cutOutNE',
    'cutOutSE',
    'cutOutSW',
    'cutOutNW',
    'numeralTop',
    'numeralBottom',
    'graceNoteSlashSW',
    'graceNoteSlashNE',
    'graceNoteSlashNW',
    'graceNoteSlashSE',
    'repeatOffset',
    'noteheadOrigin',
    'opticalCenter',
)

try:
    with io.open('glyphnames.json', 'r') as file:
        glyphnames = json.load(file)
        SMUFL_CODEPOINT_TO_NAME = {data['codepoint']: name for name, data in glyphnames.items()}
except FileNotFoundError:
    print("Couldn't find glyphnames.json.")
    exit(1)


# utility functions
def smufl_codepoint(glyph):
    # unicode 57344 --> 'U+E000'
    codepoint = 'U+' + hex(glyph.unicode)[2:].upper()
    return codepoint

def smufl_canonical_name(glyph, fallback=True):
    codepoint = smufl_codepoint(glyph)
    try:
        return SMUFL_CODEPOINT_TO_NAME[codepoint]
    except KeyError:
        if fallback:
            return glyph.glyphname
        raise ValueError(f'there’s no SMuFL character defined at codepoint {codepoint}.')

def to_spaces(i):
    return round(i/250, 3)


class SmuflMetadata(object):
    """
    This class generates metadata for a SMuFL font.

    __init__ arguments:
        font (fontforge.font), engravingDefaults (dict, optional)

    attributes:
        fontName, fontVersion, glyphsWithAnchors, glyphsWithAlternates, glyphBBoxes, ligatures

    methods:
        asdict, dump_json

    basic usage:
        >>> font = fontforge.open('myfont.sfd')
        >>> metadata = SmuflMetadata(font, my_engraving_defaults)
        >>> metadata.dump_json() # exports to <fontname>.json
    """

    def __init__(self, font, engravingDefaults=None):
        self.font = font
        self.engravingDefaults = engravingDefaults


    def asdict(self):
        d = {}
        d['fontName'] = self.fontName
        d['fontVersion'] = self.fontVersion

        # We don't want to include empty dictionary entries so we need to
        # check if there are values first.
        if self.engravingDefaults:
            d['engravingDefaults'] = self.engravingDefaults

        # These attributes are actually function calls, we bind the return value
        # before the check so we don't do the work twice.
        anchors = self.glyphsWithAnchors
        if anchors:
            d['glyphsWithAnchors'] = anchors

        alternates = self.glyphsWithAlternates
        if alternates:
            d['glyphsWithAlternates'] = alternates

        bboxes = self.glyphBBoxes
        if bboxes:
            d['glyphBBoxes'] = bboxes

        ligatures = self.ligatures
        if ligatures:
            d['ligatures'] = ligatures

        return d


    def dump_json(self, target=None, indent=2, **kwargs):
        """
        Export the complete metadata as a json file.
        The signature is the same as json.dump except that the target
        is an optional path pointing to the file. If it is omitted,
        the metadata is saved to <fontname>.json.
        """
        target = target or self.fontName + '.json'
        with io.open(target, 'w', encoding='utf-8') as file:
            json.dump(self.asdict(), file, indent=indent, **kwargs)


    @property
    def characters(self):
        # Standard SMuFL characters are encoded from U+E000 to U+F3FF.
        return (char for char in self.font.glyphs() if 57344 <= char.unicode <= 62463)


    @property
    def fontName(self):
        return self.font.fontname


    @property
    def fontVersion(self):
        return self.font.version


    @property
    def glyphsWithAnchors(self):
        all_anchors = {}

        for char in self.characters:
            char_anchors = {}

            for anchor in char.anchorPoints:
                anchor_name = anchor[0]
                if anchor_name in SMUFL_ANCHOR_NAMES:
                    x, y = (to_spaces(value) for value in anchor[2:4])
                    char_anchors[anchor_name] = (x, y)

            if char_anchors:
                char_name = smufl_canonical_name(char)
                all_anchors[char_name] = char_anchors

        return all_anchors


    @property
    def glyphsWithAlternates(self):
        all_alternates = {}

        for char in self.characters:
            char_alternates = []

            # Select all lookup tables for this character of type 'AltSubs'.
            for table in (table for table in char.getPosSub('*') if table[1]=='AltSubs'):
                substitute_names = table[2:]
                for name in substitute_names:
                    substitute_char = self.font[name]
                    codepoint = smufl_codepoint(substitute_char)
                    name = smufl_canonical_name(substitute_char)

                    char_alternates.append({
                        'codepoint': codepoint,
                        'name': name,
                    })

            if char_alternates:
                char_name = smufl_canonical_name(char)
                char_alternates = {'alternates': char_alternates}
                all_alternates[char_name] = char_alternates

        return all_alternates


    @property
    def glyphBBoxes(self):
        all_bounding_boxes = {}
        for char in self.characters:
            char_name = smufl_canonical_name(char)
            xmin, ymin, xmax, ymax = (to_spaces(value) for value in char.boundingBox())
            bounding_box = {'bBoxNE': (xmax, ymax), 'bBoxSW': (xmin, ymin)}
            all_bounding_boxes[char_name] = bounding_box

        return all_bounding_boxes


    @property
    def ligatures(self):
        all_ligatures = {}
        for char in self.characters:
            char_name = smufl_canonical_name(char)

            # Select all lookup tables for this character of type 'Ligature'.
            for table in (table for table in char.getPosSub('*') if table[1]=='Ligature'):
                component_names = [name for name in table[2:]]
                all_ligatures[char_name] = {
                    'codepoint': smufl_codepoint(char),
                    'componentGlyphs': component_names,
                }

        return all_ligatures



# script for command line usage
if __name__ == '__main__':
    import fontforge, sys

    if len(sys.argv) < 2:
        print("USAGE: ffpython smufl_metadata.py <myfont.sfd>")
        exit(1)

    fontfile = sys.argv[1]
    font = fontforge.open(fontfile)

    metadata = SmuflMetadata(font, ENGRAVING_DEFAULTS)
    metadata.dump_json()
    print(f"SMuFL metadata written to {metadata.fontName}.json.")

    font.close()
