# Sebastian music font family

The music fonts and symbol resources in this archive are free to use for everybody. I've been developing them over the last few years. They're not finished, but I cannot afford to spend any more time tweaking and refining them. If you'd like to use or even develop them, you're welcome, go for it! Do whatever you like.

The fonts are licensed under the [SIL Open Font License](http://scripts.sil.org/ofl).

**SMuFL compatible version**  

A SMuFL-compatible version has [now been released](https://github.com/fkretlow/sebastian/releases), with over 1100 glyphs (some taken from the Bravura reference font). SMuFL reference can be found here: (https://w3c.github.io/smufl/gitbook/).

This version is based on the Unified Font Object (UFO) data structure in the src folder.

Releases will contain an OTF font and the SMuFL *metadata.json* file that supplies supplementary data.



### A FEW NOTES

The original designs in the FontForge files are a work in progress that I won't continue. That means, that there is in some cases a certain lack of consistency. For example I changed the style of accidentals several times, but didn't draw correspondent micro-tonal or smaller accidentals. The same goes for numbers and clefs and maybe everything else. There is, however, enough consistency left to use the fonts as is.

The version 0.1 fonts have been used and tested with Finale 2009, they should work with later versions as well.

The symbols in **Sebastian.otf** are mapped mostly in accordance to Finale's default font Maestro, thus any Finale user should be able to use Sebastian without greater effort just by changing said default music font. It is an open type font though, and some symbols stored in it are not accessible in Finale, but those were not important for me, and I didn't fix that.

There are specific symbols for clef changes. Finale does not allow you to use them. You can, however, make custom expressions and hide normal clefs, if you think it's worth the effort.

**Sebastian-Ornaments** contains trills, some outdated articulations and smaller numbers.

**Sebastian-Met** is useful for metronome marks and metric modulations. The numbers are fit for fingerings as well.

**Sebastian-Acc-Art** contains among other things (outdated) microtonal accidentals, alternate flags (I used them as articulations, as Finale doesn't support alternate flag sizes), fermatas. The numbers are still smaller than those in Sebastian-Ornaments.

**Sebastian-Note-Clef** contains among other things alternate noteheads and italic numbers for tuplets.

**Sebastian-Numerals** contains very big and very small numbers, octaves (as they are currently partly not accessible in Sebastian, see above), and narrower accidentals (just change the font for accidentals to Sebastian-Numerals if you need them).

**Sebastian-FigBass** contains all you need to notate figured bass (basso continuo) numbers. The style of the numbers ist not the same as in the other fonts, though.

**Sebastian-Lines** contains, well, a store of lines, parentheses, arrows. Very much a work in progress.

### RESOURCES

The folder **Resources** contains all used symbols and some more resources for many types of musical symbols, all stored in FontForge projects. I cleaned it up, mostly. In most cases you'll find the latest versions of symbols at the bottom. When in doubt, compare with the FontForge projects in the fonts-folder. Modify, develop, change them as you like.

FK, September 2014
