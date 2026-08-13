# Lessons — Essential 1: Silence

Drop the relevant chapter of your guide into this folder as Markdown
files. The Afterschool Agent reads them and uses them as the source
of truth for what to teach.

## File naming

Use a simple, sortable scheme:

```
01-introduction.md
02-why-silence-matters.md
03-the-two-minute-practice.md
...
```

The agent loads them in alphanumeric order. You can also use
`chapter-NN.md` if you prefer; either works.

## File structure

Each lesson MD file should have:

1. A title (`#` H1).
2. A short intro paragraph (2–4 sentences).
3. The body — what the student needs to understand.
4. A "Try this" section with one or two small, concrete actions.
5. A "Reflection" prompt or two.
6. (Christian tradition only) A Scripture quote or reference.

Example skeleton:

```markdown
# Why Silence Matters

Two sentences on what this lesson is about and why it matters.

[body of the lesson — what to teach]

## Try this

- One small, concrete action. Keep it under five minutes.
- A second action for the student who wants to go deeper.

## Reflection

- One question the student can sit with for the day.

> "Be still, and know that I am God." — Psalm 46:10
```

## Tradition branching

If the same lesson needs a different framing for Christian vs
Universal students, use two files:

```
03-the-two-minute-practice.christian.md
03-the-two-minute-practice.universal.md
```

The agent picks the right one based on the student's tradition.

## What to do first

Drop your existing chapter on Silence from the onetoeight guide
into this folder as `01-introduction.md`. The agent will pick it up
on the next chat.