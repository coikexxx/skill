# skill

这是一个按 **skill** 维度组织的仓库：每个能力单独放在 `skills/<skill-name>/` 下，仓库根目录只保留共享索引、发布产物和许可证。

## Repository Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml        # 可选：UI / 调用元数据
    references/              # 可选：按需加载的参考资料
    scripts/                 # 可选：可复用脚本
    assets/                  # 可选：模板、图标、资源文件

dist/                        # 可分发的 .skill 打包产物

docs/INDEX.md                # 仓库级 skill 索引
```

## Skills

当前仓库包含两个 skill：

- `geo-risk-audit`：搜索前置的 GEO / AI 投毒风险审计。
- `skill-repo-maintainer`：维护多 skill 仓库结构、索引和发布准备事项。

详细目录、用途与发布状态见 `docs/INDEX.md`。

## Maintenance Workflow

1. 在 `skills/` 下为每个 skill 维护独立目录。
2. 每个 skill 至少提供 `SKILL.md`，并尽量补齐 `agents/openai.yaml`。
3. 新增或更新 skill 后，同步刷新 `docs/INDEX.md`。
4. 需要分发时，再为对应 skill 生成 `dist/<skill-name>.skill` 打包产物。

## License

MIT
