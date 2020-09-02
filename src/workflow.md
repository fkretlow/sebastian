# Workflow

We may need to refine this, but it's basically no different to working with sfd files.

1. Pull from GitHub.
2. Open `src/sebastian.ufo` in Fontforge, have fun.
3. Save your changes by generating back to the same file via File > Generate Fonts, selecting UFO 3 as file format.
4. Add, commit and push to GitHub.

The ``ff-smufl.py`` file in the `scripts` folder is mostly the same as the old script you know. I'm going to make a few changes there and set up a Makefile so we can automate the build process.
