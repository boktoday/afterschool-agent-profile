# Universal Edition — Eight Essentials (PDF)

**File:** `onetoeight-eight-essentials-universal-edition.pdf` — 97 pages, ~194 KB.

A standalone PDF of the Eight Essentials guide in the Universal
(secular) tradition. Built from the `universal.md` lesson files in
this repo's `essentials/<NN-name>/lessons/` folders.

## What it is

- **Cover** — title page with Universal Edition framing.
- **Colophon** — explains how this edition relates to the source
  Universal Edition V.3.0.0.
- **Contents** — table of contents with all 11 sections.
- **Introduction** — Why Roots Matter (Universal edition).
- **Chapters 1–7** — the seven essentials before Faith, with body
  content from the source guide. The body is intentionally inclusive
  in the source (Hebrew Bible + New Testament + Qur'an + Stoic + Muir),
  and the Universal Edition honours that inclusion by sitting
  alongside all traditions without endorsing any one.
- **Chapter 8** — Tested Convictions. The body is the source chapter.
  Appendix B's *Secular / Humanist Customisation* notes are appended
  at the end of the chapter.
- **Conclusion** — Building a Life That Holds.
- **Before & After** — Your Roots Assessment.
- **Closing colophon** — Brendan's note.

## How it was built

Generated from the source guide by reading each
`essentials/<NN>/lessons/universal.md`, stripping the frontmatter
wrapper, and laying the content out via reportlab. The full content
of every chapter is preserved exactly (byte-identical to the source
for the chapter bodies — verified).

## Regenerating

The PDF is buildable from the lesson MD files in this repo. The
generator script reads them directly, so updating any
`essentials/<NN>/lessons/universal.md` and rebuilding gives a fresh
PDF that matches the repo state. The build script (not in this repo)
needs Python 3.13 with `reportlab` and `pypdf`.