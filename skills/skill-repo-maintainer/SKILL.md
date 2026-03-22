---
name: skill-repo-maintainer
description: Maintain a multi-skill repository that stores several Codex/OpenAI skills under a shared `skills/` directory. Use when Codex needs to add a new skill, refactor a repo into per-skill folders, normalize metadata such as `SKILL.md` and `agents/openai.yaml`, refresh repository-level indexes, or prepare a skill for packaging and distribution.
---

# Skill Repo Maintainer

Keep the repository organized by **skill folder first**.

## Core workflow

1. Identify the target skill name and create or update `skills/<skill-name>/`.
2. Ensure the skill keeps its own `SKILL.md` as the source of truth.
3. Add or refresh `agents/openai.yaml` when UI metadata is needed.
4. Store reusable support material inside that skill only:
   - `references/` for documentation loaded on demand
   - `scripts/` for deterministic helpers
   - `assets/` for templates or bundled files
5. Update repository-level indexes or README files after changing the skill set.
6. Treat `dist/<skill-name>.skill` as a release artifact, not the editing source.

## Repository normalization rules

- Prefer one top-level folder per skill under `skills/`.
- Keep cross-skill documentation in shared repo files such as `README.md` or `docs/INDEX.md`.
- Do not mix one skill's references, assets, or scripts into another skill's directory.
- Keep skill names in lowercase hyphen-case.
- Keep YAML frontmatter limited to `name` and `description`.
- Make the `description` explain both capability and trigger conditions.

## When adding a new skill

- Pick a short hyphen-case folder name.
- Write `SKILL.md` for the reusable workflow, not for one-off project notes.
- Create only the resource subdirectories the skill truly needs.
- Add an index entry that records source path, package path, and current status.
- If packaging is not done yet, mark the skill as source-only instead of inventing a release artifact.

## When refactoring an existing repo into a skill repo

- Move each distinct capability into its own folder under `skills/`.
- Rewrite the root README so it describes the repository as a catalog of skills.
- Add a compact shared index that lists every skill and its release state.
- Standardize metadata before worrying about packaging.
- Preserve already-built artifacts in `dist/`, but treat them as outputs.

## Release-readiness check

Before packaging a skill, confirm:

- `SKILL.md` frontmatter is valid.
- referenced files and folders actually exist.
- `agents/openai.yaml` matches the current skill purpose.
- repository indexes mention the skill and package status.
- the skill can still be understood without unrelated repo context.

## Load references as needed

- Read `references/repo-checklist.md` for a compact maintenance checklist.
- Read `references/release-readiness.md` before packaging or publishing a skill.
