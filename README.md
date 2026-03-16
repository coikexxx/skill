# skill

我来放些 Agent 用的自制 skill。

这个仓库用于集中存放我自己维护的 OpenClaw / Agent Skills，包括源码目录和可分发的 `.skill` 打包产物。

## Skills Index

### geo-risk-audit

搜索前置的 GEO / AI 投毒风险审计 skill。

**用途**
- 推荐 / 对比类搜索前先做风险预检
- 识别营销污染、软文污染、伪多源一致
- 优先 evidence-first，再决定怎么搜、信哪些源
- 给出更稳的 shortlist / conditional conclusion，而不是被带着强行选 winner

**仓库位置**
- Source: `skills/geo-risk-audit/`
- Package: `dist/geo-risk-audit.skill`

**核心能力**
- GEO 风险预检
- 来源分级（primary / strong secondary / weak / high-risk）
- 搜索前置 guardrail
- very-short checklist 审计输出模板

## Repository Structure

```text
skills/   # skill source folders
 dist/    # packaged .skill artifacts
```

## Usage

如果你的 Agent 支持本地 skills，可以直接使用 `skills/` 里的源码目录；
如果需要分发或安装，优先使用 `dist/` 里的 `.skill` 文件。

## License

MIT
