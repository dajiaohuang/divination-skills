# 资料快照库

`references/library/` 保存来源清单对应的、可进入版本控制的 Markdown
审计快照。它和 `references/upstream/` 的职责不同：

- `library/` 是来源级资料快照，记录 URL、版本、许可、解析状态和哈希；
- `upstream/` 是被忽略的外部仓库克隆，只用于人工对照，绝不打包或依赖；
- `systems/*/sources/*.json` 与 `catalog/sources/*.json` 仍是来源元数据主记录；
- `systems/*/rules/*.json` 仍是机器规则主记录，Markdown 不能替代规则数据。

生成或刷新，并把 Markdown 路径与 SHA-256 回写到全部来源清单：

```powershell
.\.venv\Scripts\python.exe tooling\scripts\build_reference_library.py --update-manifests
```

检测网络资料、解析器或已提交快照是否漂移：

```powershell
.\.venv\Scripts\python.exe tooling\scripts\build_reference_library.py --check
```

正文保存遵守各来源自己的许可。公版、明确允许衍生使用的资料可以保存全文解析；
仅参考、许可不明、要求额外授权或只允许使用事实元数据的来源，只保存必要元数据、
哈希与明确标注的事实摘要。根目录 Apache-2.0 不会重新许可第三方资料。
