# Style guide

Goal: the shortest README a replicator can follow without guessing.

## Rules

1. **Lists over prose.** One fact per bullet. Use prose only for the Overview (2–5 sentences) and for data access conditions that need a sentence.
2. **Lists over tables.** Use tables only where the content is a grid with several attributes per row: data availability summary, dataset list, table/figure map. Do not put instructions or software lists in tables.
3. **Chronological order.** Instructions follow the order a replicator acts: configure → install → get data → run → manual steps. One action per step. Number the steps when order matters.
4. **No chattiness.** Remove: greetings, thanks, "we hope", "please feel free", "this README will guide you", "in this section we describe".
5. **No AI-speak.** Remove words and constructs such as: "delve", "comprehensive", "robust" (non-statistical), "seamless", "leverage", "utilize", "it is important to note", "ensure that", "in order to", "plays a crucial role", "a wide range of", "streamline", "elevate", "navigate the complexities", "Furthermore,", "Moreover,", "In summary,", emoji, bold on random words, a summary at the end of every section.
6. **Concrete beats vague.** "Runs ~3 hours on a 4-core laptop" beats "may take some time". "Stata 17 MP" beats "Stata".
7. **Paths and commands in code formatting:** `programs/main.do`, `pip install -r requirements.txt`.
8. **No duplication.** Say each fact once, in its Template section; link instead of repeating.
9. **Active, imperative voice in instructions:** "Run `main.do`", not "The main file should be run by the user".
10. **English**, plain, no jargon beyond the field's standard terms.

## How to report style findings

- Quote the text (≤ 20 words; use "…" to shorten).
- Give the replacement.
- Tag style findings **Low** unless they make instructions ambiguous (then **Medium**).

Example:

- **Low** — Overview: "In this comprehensive replication package, we are delighted to provide all the materials needed to…" → "This package contains the data and Stata code to produce all tables and figures."
