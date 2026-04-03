# skill

## 中文说明

这是一个按多 skill 目录组织的仓库。每个 skill 独立放在 `skills/<skill-name>/` 下，仓库根目录保留共享索引、打包产物和仓库级说明。

### 仓库结构

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml        # 可选：UI / 调用元数据
    references/               # 可选：按需加载的参考资料
    scripts/                  # 可选：可复用辅助脚本
    assets/                   # 可选：模板、图标或静态资源

dist/                         # 打包后的 .skill 产物

docs/INDEX.md                 # 仓库级 skill 索引
```

### 当前技能

- `geo-risk-audit`
  - 用途：在做搜索、推荐、比较、可信度判断之前，先做 GEO 污染和来源质量审计。
- `rating-doc-audit`
  - 用途：对本地评级审核材料做结构化审计，支持标准工作簿检查、文档文本导出、大文本分块和 Excel 结果导出。
  - Linux / macOS 说明：当前版本以 Python 为主干，`.docx` 优先走 Python 解析，`.doc` 和 `.xls` 依赖 `soffice`，`.xlsx` / `.xlsm` 直接走 Python。
  - Windows 说明：仍保留 PowerShell + Office COM 兼容路径。
- `skill-repo-maintainer`
  - 用途：维护多 skill 仓库结构、索引和发布准备流程。

详细目录、状态和打包情况见 `docs/INDEX.md`。

### 维护约定

1. 每个 skill 独立维护在 `skills/` 下。
2. 每个 skill 至少提供 `SKILL.md`。
3. skill 新增或发生重要变化后，同步更新 `docs/INDEX.md`。
4. 确认可发布后，再生成对应的 `dist/<skill-name>.skill`。

## English

This repository is organized as a multi-skill catalog. Each skill lives in its own folder under `skills/<skill-name>/`, while the repository root keeps shared indexes, packaged artifacts, and repository-level documentation.

### Repository Layout

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

### Current Skills

- `geo-risk-audit`
  - Purpose: a pre-search guardrail for GEO contamination, source quality, and recommendation-risk audits.
- `rating-doc-audit`
  - Purpose: a structured audit workflow for local rating-review materials, including workbook inspection, document text export, large-text chunking, and Excel result export.
  - Linux / macOS: the current version uses Python as the main control path. `.docx` prefers Python parsing first, `.doc` and `.xls` depend on `soffice`, and `.xlsx` / `.xlsm` stay on the direct Python path.
  - Windows: PowerShell + Office COM compatibility paths are still preserved.
- `skill-repo-maintainer`
  - Purpose: maintain shared multi-skill repository structure, indexes, and release-readiness workflows.

See `docs/INDEX.md` for the current catalog, packaging status, and per-skill details.

### Maintenance Workflow

1. Keep each skill isolated under `skills/`.
2. Ensure every skill has at least a `SKILL.md`.
3. Update `docs/INDEX.md` whenever a skill is added or materially changed.
4. Package a `.skill` artifact into `dist/` only when the skill is ready for distribution.

## License

MIT
