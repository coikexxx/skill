# skill

This repository is organized as a multi-skill catalog. Each skill lives in its own folder under `skills/<skill-name>/`, while the repository root keeps shared indexes, packaged artifacts, and repository-level metadata.

## Repository Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml        # optional: UI / invocation metadata
    references/               # optional: load-on-demand reference material
    scripts/                  # optional: reusable helper scripts
    assets/                   # optional: templates, icons, or static files

dist/                         # packaged .skill artifacts

docs/INDEX.md                 # repository-wide skill index
```

## Skills

The repository currently contains these skills:

- `geo-risk-audit`: pre-search guardrail for GEO contamination, source quality, and recommendation-risk audits.
- `rating-doc-audit`: local rating-material audit workflow for Word and Excel inputs, with large-file handling and Excel result export.
- `skill-repo-maintainer`: maintenance workflow for shared multi-skill repositories, indexes, and publishing readiness.

See `docs/INDEX.md` for the current catalog, descriptions, and packaging status.

## Maintenance Workflow

1. Keep each skill isolated under `skills/`.
2. Ensure every skill has at least a `SKILL.md`, and preferably `agents/openai.yaml` when UI metadata is needed.
3. Update `docs/INDEX.md` whenever a skill is added or materially changed.
4. Package a `.skill` artifact into `dist/` only when the skill is ready for distribution.

## License

MIT
