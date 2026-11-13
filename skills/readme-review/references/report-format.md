# Report format

Write the report in Markdown, in this shape. Omit empty groups.

```markdown
# README review: <README file name>

- Skill: readme-review v<VERSION> · Template v1.2 · <YYYY-MM-DD>
- Mode: review-only | edit (package available)
- Verdict: <one line, e.g. "Close to Template; data access details and table map incomplete.">
- Findings: <n> High · <n> Medium · <n> Low

## A. Structure

- **High** — <section>: <problem>. Fix: <fix>.

## B. Content

### <Template section name>

- **High** — <problem>. Fix: <fix>.
- **Medium** — …

## C. Style

- **Low** — <section>: "<quoted text>" → "<replacement>".

## Sections with no findings

<comma-separated list>

## Edited copy (edit mode only)

- File: `README-ai-edited.md`
- Sections changed: <list>
- Placeholders left for the author: <n> (search for `AUTHOR TO`)

---

Feedback on this review: <FEEDBACK_LINK>
```

## Priority definitions

- **High**: a replicator cannot proceed or cannot reproduce a result (missing data access, missing entry point, unmapped exhibits, missing software).
- **Medium**: a replicator can proceed but will lose time or guess (no versions, no runtime, unclear order).
- **Low**: style or polish.

## Feedback line

Read the file `FEEDBACK_URL` in this skill folder. Replace `{VERSION}` in it with the skill version; the result is `<FEEDBACK_LINK>`. If the file is missing or empty, omit the feedback line.
