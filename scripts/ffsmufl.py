#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The SmuflFont class defined in this module wraps SMuFL specific methods around
fontforge.font objects.

A copy of the `glyphnames.json` file from the SMuFL specification must be saved
in the same folder. It's available at https://github.com/w3c/smufl/tree/gh-pages/metadata.

Example:

    with SmuflFont("path/to/my/font.ufo") as font:
        font.rename_glyphs()
        font.save()
        font.engraving_defaults = my_defaults
        font.export_metadata()
        font.export_font()

Written by Florian Kretlow. Use, distribute and edit this file as you wish.
"""
import fontforge
import io
import json
from pathlib import Path


class SmuflFont(object):
    """
    This class represents a SMuFL font. It's wraps (but doesn't subclass)
    fontforge.font, adding a few SMuFL specific data members and methods. It's
    set up as a context manager so it works with the with statement:

        with SmuflFont("path/to/font/file", "r") as f:
            f.export_metadata()
            f.export_font()

    Relevant methods:
        - generate_metadata: get a dict with the font metadata
        - export_metadata: serialize and write metadata to a json file
        - export_font: export to any format other than sfd
        - rename_glyphs: rename available glyphs in the SMuFL range
          to their canonical names
    """
    valid_anchor_names = (
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

    # Find glyphnames.json anywhere in the repository. If it's not there, explode.
    for p in Path('.').glob('**/glyphnames.json'):
        try:
            with io.open(p, 'r') as infile:
                glyphnames = json.load(infile)
                codepoint_to_name = {data['codepoint']: name for name, data in glyphnames.items()}
                break
        except StopIteration:
            print("Couldn't find glyphnames.json.")
            exit(1)
        except:
            continue


    @staticmethod
    def format_codepoint(unicode_):
        # unicode 57344 --> 'U+E000'
        return 'U+' + hex(unicode_)[2:].upper()


    @staticmethod
    def canonical_glyphname(unicode_, fallback=True):
        codepoint = SmuflFont.format_codepoint(unicode_)
        try:
            return SmuflFont.codepoint_to_name[codepoint]
        except KeyError:
            if fallback: return glyph.glyphname
            raise ValueError(f'There’s no SMuFL character defined at codepoint {codepoint}.')


    @staticmethod
    def em_to_spaces(em):
        return round(em/250, 3)


    def __init__(self, path, mode='w', engraving_defaults=None):
        self.font = fontforge.open(path)
        self.read_only = (mode == 'r')
        self.engraving_defaults = engraving_defaults


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        if self.font: self.font.close()
        return False


    def __iter__(self):
        """
        fontforge.font.__iter__ returns an iterator over the font's glyphnames. This is
        the only thing we're doing differently: We iterate directly over all available
        glyphs in the SMuFL range.
        """
        # Standard SMuFL characters are encoded from U+E000 to U+F3FF.
        return (char for char in self.font.glyphs() if 57344 <= char.unicode <= 62463)


    def __getitem__(self, glyphname):
        return self.font[glyphname]


    def save(self, *args):
        """
        Save the font file, same as fontforge.font.save, but throws when we're
        in read-only mode.
        """
        if self.read_only and not args:
            raise PermissionError('Font is opened in read-only mode.')
        self.font.save(*args)

    def close(self):
        """
        Same as fontforge.font.close.
        """
        self.font.close()


    def export_font(self,filename=None, *args, **kwargs):
        """
        Export a usable binary. The signature is the same as fontforge.font.generate
        except that the filename is optional. If it is omitted, the font is exported
        to <fontname>.otf.
        """
        filename = filename or self.font.fontname.lower() + '.otf'
        self.font.generate(filename, *args, **kwargs)


    def export_metadata(self, filename=None, indent=2, **kwargs):
        """
        Export the complete font metadata as a json file.
        The signature is the same as json.dump except that the filename is optional.
        If it is omitted, the metadata is saved to <fontname>.json.
        """
        filename = filename or self.font.fontname.lower() + '.json'
        with io.open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(self.generate_metadata(), outfile, indent=indent, **kwargs)


    def generate_metadata(self):
        """
        Get the font metadata as a dictionary.
        """
        return _SmuflMetadata(self).asdict()


    def rename_glyphs(self):
        """
        Rename all available glyphs in the SMuFL range to their canonical names.
        """
        for glyph in self:
            glyph.glyphname = SmuflFont.canonical_glyphname(glyph.unicode)


    @property
    def fontname(self):
        return self.font.fontname


    @property
    def version(self):
        return self.font.version


    @property
    def engraving_defaults(self):
        return self._engraving_defaults

    @engraving_defaults.setter
    def engraving_defaults(self, defaults):
        if defaults is not None and not isinstance(defaults, dict):
            raise TypeError("Engraving defaults must be a dictionary.")
        self._engraving_defaults = defaults



class _SmuflMetadata(object):
    """
    This class is used by a SmuflFont to generate SMuFL metadata.

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
    """

    def __init__(self, font):
        self.font = font


    def asdict(self):
        d = {}
        d['fontName'] = self.font.fontname
        d['fontVersion'] = self.font.version

        # We don't want to include empty dictionary entries so we check if
        # there are values first.
        if defaults := self.engraving_defaults():
            d['engravingDefaults'] = defaults

        if anchors := self.anchors():
            d['glyphsWithAnchors'] = anchors

        if alternates := self.alternates():
            d['glyphsWithAlternates'] = alternates

        if bounding_boxes := self.bounding_boxes():
            d['glyphBBoxes'] = bounding_boxes

        if ligatures := self.ligatures():
            d['ligatures'] = ligatures

        return d


    def engraving_defaults(self):
        return self.font.engraving_defaults


    def anchors(self):
        all_anchors = {}

        for char in self.font:
            char_anchors = {}

            for anchor in char.anchorPoints:
                anchor_name = anchor[0]
                if anchor_name in SmuflFont.valid_anchor_names:
                    x, y = (SmuflFont.em_to_spaces(value) for value in anchor[2:4])
                    char_anchors[anchor_name] = (x, y)

            if char_anchors:
                char_name = SmuflFont.canonical_glyphname(char.unicode)
                all_anchors[char_name] = char_anchors

        return all_anchors


    def alternates(self):
        all_alternates = {}

        for char in self.font:
            char_alternates = []

            # Select all lookup tables for this character of type 'AltSubs'.
            for table in (table for table in char.getPosSub('*') if table[1]=='AltSubs'):
                substitute_names = table[2:]
                for name in substitute_names:
                    substitute_char = self.font[name]
                    codepoint = SmuflFont.format_codepoint(substitute_char.unicode)
                    name = SmuflFont.canonical_glyphname(substitute_char.unicode)

                    char_alternates.append({
                        'codepoint': codepoint,
                        'name': name,
                    })

            if char_alternates:
                char_name = SmuflFont.canonical_glyphname(char.unicode)
                char_alternates = {'alternates': char_alternates}
                all_alternates[char_name] = char_alternates

        return all_alternates


    def bounding_boxes(self):
        all_bounding_boxes = {}
        for char in self.font:
            char_name = SmuflFont.canonical_glyphname(char.unicode)
            xmin, ymin, xmax, ymax = (SmuflFont.em_to_spaces(value) for value in char.boundingBox())
            bounding_box = {'bBoxNE': (xmax, ymax), 'bBoxSW': (xmin, ymin)}
            all_bounding_boxes[char_name] = bounding_box

        return all_bounding_boxes


    def ligatures(self):
        all_ligatures = {}
        for char in self.font:
            char_name = SmuflFont.canonical_glyphname(char.unicode)

            # Select all lookup tables for this character of type 'Ligature'.
            for table in (table for table in char.getPosSub('*') if table[1]=='Ligature'):
                component_names = [name for name in table[2:]]
                all_ligatures[char_name] = {
                    'codepoint': SmuflFont.format_codepoint(char.unicode),
                    'componentGlyphs': component_names,
                }

        return all_ligatures
