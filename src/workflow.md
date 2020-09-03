# Workflow

We may need to refine this, but it's basically no different than working with sfd files.

1. Pull from GitHub.
2. Open `src/sebastian.ufo` in Fontforge, have fun.
3. Save your changes by generating back to the same file via File > Generate Fonts, selecting UFO 3 as file format.
4. Optional: Make a build to test your changes by running `make build` in the root directory.
5. Add, commit and push to GitHub.

When you add new glyphs in Fontforge, you can rename them automatically with `make rename`.
