# Release Readiness

Before creating `dist/<skill-name>.skill`, check:

- The skill instructions are complete enough for reuse.
- `agents/openai.yaml` exists if downstream UI metadata is expected.
- Paths mentioned in `SKILL.md` point to real files.
- Repository docs do not claim a package exists unless it has been built.
- The packaged artifact name matches the skill folder name exactly.
