# dnd-tools

> This repository supplies a set of tools for authoring DnD content in markdown and LaTeX quickly and in a visually thematic way.

## Features

At the moment:

- A Pandoc template to leverage [this](https://github.com/rightbrace/DND-5e-LaTeX-Template) LaTeX package, which styles an `article` like the player's handbook. My fork is already a fork of a fork, so for full credit, use the button on GitHub.
- A script to pull monster stat blocks from [this](https://www.dnd5eapi.co/) convenient API, and to format them into LaTeX

## Planned

- More automatic generation scripts (spells, etc)
- Minor bugfixes in the LaTeX package (upstream hasn't been updated in four years, so I'd prefer to fix issues on my end)

## Installation

1. Ensure you have:
- Python 3
- LaTex (`texlive-full` or equivalent)
- Pandoc

2. Double check the installation directories in `install.sh`. if yours are different from the following, update them accordingly:

**Pandoc**: `~/.pandoc/templates`
**LaTeX**: `~/texmf/tex/latex/`

3. `./install.sh`

## Usage

Usage is pretty simple, as this is mostly glue. I like to setup a makefile with the command `pandoc --template dnd --toc -o Campaign.pdf Campaign.md`, and just run `make` every once in a while. 

While editing, if your editor supports inserting the output of shell commands into your document, then I would suggest using it liberally. In Vim, you can just run `:r!./monsterdata.py orc` to insert the correct LaTeX formatting instructions for orcs.

There is one additional provided LaTeX environment at the moment, to reduce the amount of LaTeX you need to mix into your markdown:

```latex
\begin{dnditem}
{Name}
{Type, rarity}
Description
\end{dnditem}
```

More may follow.

## Disclaimer

It is very possible that the monster stat block script misses something. This could be either the APIs fault or mine. If you're concerned, always double check your stat blocks!

## Licenses

The LaTeX template I forked was under MIT, I am retaining this license, even if I make significant changes.

The other scripts here are also placed under MIT.

*Dungeons & Dragons* is owned by Wizards of the Coast, with whom none of this is affiliated.
