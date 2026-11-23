# Quantum

Work on Quantum Computing for the Big Data course at HCMUT, split into two areas that share one set of tools and reference material.

| Folder | What it is |
|---|---|
| [`seminar/`](seminar) | The three-part group seminar: content packages, speaker notes (English and Vietnamese), the generated slide decks and the merged 91-slide talk. Start with [`seminar/README.md`](seminar/README.md). |
| [`project/`](project) | The course project. See [`project/README.md`](project/README.md). |

## Shared at the repo root

| Path | Used for |
|---|---|
| `.claude/skills/educational-dark-design/` | The slide skill (design system and deck builder). Claude Code loads it when opened in this folder; type `/` to see it. |
| `material/` | Reference book, *Quantum Computation and Quantum Information* (Nielsen & Chuang). The PDF itself is not committed; put your own copy in this folder. |
| `.gitignore` | Keeps the textbook PDF, caches and local settings out of git. |

## Layout

```
quantum/
├── seminar/        seminar content, notes and decks
├── project/        course project
├── material/       reference book (local only)
└── .claude/skills/educational-dark-design/
```
