# TODO: 待解决的问题与潜在风险

> **最后更新**: 2026-06-22
> **编译状态**: ✅ 成功 (157页)

---

## 当前状态

- **编译**: ✅ 成功
- **PDF**: [main.pdf](main.pdf) (157页, 9.4MB)
- **致命错误**: 无
- **模板文件**: `ustthesis.cls` / `ustthesis.sty` 与 `../Template-of-HKUST-GZ-Thesis` 一致
- **图表状态**: 正文浮动体使用页顶放置；Table 3.1--3.3 已按页宽排版，无表格本体重叠

---

## 待处理问题（按优先级）

### 🔴 高优先级

| 问题 | 文件 | 解决方案 |
|-----|------|---------|
| 委员会信息占位符 | `main.tex` | 填写正确的委员会成员 |
| 模板官方认可 | - | 联系研究生院确认模板有效性 |
| 致谢内容 | `chapters/00-acknowledgments.tex` | 确认是否完整 |

### 🟡 中优先级

| 问题 | 文件 | 影响 |
|-----|------|------|
| 表格中`→`符号缺失 | `appendices/A-universal-video-retrieval.tex` | 显示空白，可选修复 |
| `qwen3vlembedding` 缺少 arXiv ID | `references/references.bib` L469-474 | 该 arXiv 条目无法生成 `eprint`，影响链接与元数据；疑为 `arXiv:2601.04720`（来自已删除的 `li2026qwen3`），需人工确认 |
| 条目标题含可疑空格 | `references/references.bib` L115, L291 | `InternVideo2. 5` 与 `Qwen2. 5-vl` 中间的空格疑似原始数据错误，应改为 `InternVideo2.5` 与 `Qwen2.5-VL` |
| 大量条目缺失 `pages` / `publisher` / `DOI` | `references/references.bib` | 约 41 个条目缺 `pages`，49 个会议条目缺 `publisher`，107/109 个条目缺 `DOI`；需从出版源逐一补全 |
| 多条作者列表截断为 `and others` | `references/references.bib` | 如 `lin2025towards`、`wang2024internvideo2`、`kong2025modality`、`radford2021learning`、`bolya2025perception` 等；需从论文原文补全作者 |
| `booktitle` 大小写/格式不统一 | `references/references.bib` | 会议名称写法不一致，部分应加 `{...}` 保护大写，如 CVPR/ICCV/ECCV/NeurIPS 等 |
| 单独出现的 `clip` 未保护 | `references/references.bib` | 为避“video clip（片段）”与“CLIP 模型”歧义，未自动把 `clip` 改为 `{CLIP}`；若上下文确指 CLIP 模型，需手动加花括号 |

### 🟢 低优先级（可忽略）

- 字体小型大写警告
- Overfull/Underfull hbox（主要来自目录附录编号和正文长串）
- PDF版本兼容警告

---

## 已修复问题

| 问题 | 状态 |
|-----|------|
| 参考文献重复 key (`li2026qwen3` / `qwen3vlembedding`) | ✅ 已统一为 `qwen3vlembedding` |
| 参考文献冗余条目 (5 个未引用 key) | ✅ 已删除 |
| 三个未使用的影子 bib 文件 (`gve.bib` 等) | ✅ 已删除，仅保留 `references.bib` |
| microtype与XeTeX兼容性 | ✅ 已注释 |
| 致谢摘要格式 | ✅ 已修复 |
| 日期格式错误 | ✅ 已修复 |
| Unicode箭头符号（正文） | ✅ 已添加命令 |
| Caption全局覆盖 | ✅ 已移除 `\captionsetup`，保持模板默认字体 |
| Caption上下间距 | ✅ 在 `main.tex` 局部镜像模板逻辑，仅补充 caption 下方 10pt |
| 第三章 Table 3.1--3.3 重叠/过宽 | ✅ 已参考 MM2026 原稿列分组，用 `tabular*{\linewidth}` 按页宽排版 |
| 正文表格缩放方式 | ✅ 未使用 `tabularx` / `adjustbox` / `resizebox` / `wraptable` |

---

## 编译命令

```bash
# 进入论文目录
cd HKUSTGZ-Thesis

# 完整编译（推荐）
latexmk -xelatex -f main.tex

# 清理辅助文件
latexmk -C
```

---

## 文件结构（清理后）

```
HKUSTGZ-Thesis/
├── main.tex                 # 主编译文件
├── main.pdf                 # 编译输出
├── chapters/                # 论文章节
├── appendices/              # 附录
├── figures/                 # 图片资源
├── references/              # 参考文献
├── ustthesis.cls            # 论文模板类文件
├── ustthesis.sty            # 模板样式文件
├── README.md                # 项目说明
└── TODO.md                  # 本文件
```

---

## 更新日志

| 日期 | 更新内容 |
|-----|---------|
| 2026-06-22 | 更新第三章 Table 3.1--3.3 为页宽 `tabular*` 排版，解决表格重叠/挤压 |
| 2026-06-22 | 确认 caption 字体与模板一致，保留模板 caption 样式 |
| 2026-06-22 | 同步当前编译状态：成功，157页 |
| 2026-06-21 | 统一参考文献格式：保护缩写、规范 arXiv 字段、统一期刊名大小写 |
| 2026-06-21 | 添加参考文献待补全/确认事项到 TODO |
| 2025-06-21 | 清理模板示例文件和编译辅助文件 |
| 2025-06-21 | 简化TODO.md，保留关键信息 |
| 2025-06-14 | 修复编译问题，生成PDF |
