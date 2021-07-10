# Sebastian music font

Sebastian is a SMuFL-compatible music font, with over 1200 glyphs (some taken from the Bravura reference font). SMuFL reference can be found here: (https://w3c.github.io/smufl/gitbook/). 

The fonts are licensed under the [SIL Open Font License](http://scripts.sil.org/ofl). You are free to use, copy and modify this font. Modified versions must use a different name.

The source files are provided as Unified Font Object (UFO) data structure in the src folder.

Releases will contain an OTF font and the SMuFL *metadata.json* file that supplies supplementary data. [They can be found here](https://github.com/fkretlow/sebastian/releases).

 
### LEGACY FILES

Also included are several 'legacy' files: FontForge .sfd files containing various designs for music characters, and a set of version 0.1 OTF fonts using the alphanumeric '8-bit' range. These were intended for pre-SMuFL versions of Finale. They are abandoned, in terms of Sebastian's development, but may be useful to others. 

The symbols in **Sebastian.otf** are mapped mostly in accordance to Finale's legacy default font, Maestro, thus any Finale user should be able to use Sebastian without greater effort just by changing said default music font. It is an open type font though, and some symbols stored in it are not accessible in Finale, but those were not important for me, and I didn't fix that.

**NB: Do not install both the v0.1 version of Sebastian.otf AND the newer, SMuFL-compatible font.

**Sebastian-Ornaments** contains trills, some outdated articulations and smaller numbers.

**Sebastian-Met** is useful for metronome marks and metric modulations. The numbers are fit for fingerings as well.

**Sebastian-Acc-Art** contains among other things (outdated) microtonal accidentals, alternate flags (I used them as articulations, as Finale doesn't support alternate flag sizes), fermatas. The numbers are still smaller than those in Sebastian-Ornaments.

**Sebastian-Note-Clef** contains among other things alternate noteheads and italic numbers for tuplets.

**Sebastian-Numerals** contains very big and very small numbers, octaves (as they are currently partly not accessible in Sebastian, see above), and narrower accidentals (just change the font for accidentals to Sebastian-Numerals if you need them).

**Sebastian-FigBass** contains all you need to notate figured bass (basso continuo) numbers. The style of the numbers ist not the same as in the other fonts, though.

**Sebastian-Lines** contains, well, a store of lines, parentheses, arrows. Very much a work in progress.


FK, BBW - July 2021
