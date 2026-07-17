# Defense Slides

> 本文件是 slides 目录的**唯一权威文档**（已合并原 `layout-issues-v0.4.md`）。
> 后续 agent 迭代前请先读「Build Internals & Hard-Won Fixes」和「红线规则」两节，再改 `build.py`。

## Files

- `thesis-slides-v0.4.pptx` — **current version**（85 张；0 重叠 / 0 越界 / 0 文字溢出 / 无丢图 / **PowerPoint 正常打开无"需修复"**）
- `thesis-slides-v0.3.pptx` / `v0.2` / `v0.1` — previous versions
- `build.py` — **设计系统参考库**（纯函数定义，不含 slide 内容；开新版本时从此派生设计 token 与组件）
- `figures/` — PNGs used by the current deck

## How figures are used

`build.py` places PNGs onto slides via `pic(s, "name", ...)`. Each call maps to `figures/name.png`:

```
pic(s, "gve/model", ...)           → figures/gve/model.png
pic(s, "mglvr/d2s", ...)           → figures/mglvr/d2s.png
pic(s, "thesis-framework", ...)    → figures/thesis-framework.png
```

`figures/` 中的 PNG 恰好是 `build.py` 引用的那些，都是仓库级 `figures/{gve,mglvr,gmpgr}/` 中矢量 PDF 的高分辨率光栅化结果。

## How to add a figure back

需要一张当前 deck 未引用的图时：

1. 找到仓库级 `figures/{gve,mglvr,gmpgr}/<name>.pdf`
2. 按矢量尺寸 2–4× 光栅化为 PNG（如 PyMuPDF 4×）
3. 存到 `slides/figures/{gve,mglvr,gmpgr}/<name>.png`
4. 在 `build.py` 加一句 `pic(s, "subdir/name", ...)`
5. **不裁剪、不编辑图片内容**（用户红线：改图前必须先告知并获同意）

---

## ⭐ Build Internals & Hard-Won Fixes（后续 agent 必读）

### 两个导致 PowerPoint「内容有问题 / 需修复」的根因（均已根治）

PowerPoint 打开时弹"发现内容有问题，可尝试修复"，根因**不是** XML 语法错误（190 个 XML 全部 well-formed），而是两处 OOXML 包级/schema 问题。**两者都修好后才不再弹框**——只修第一个是不够的。

**根因 ①：`<a:defRPr>` 元素顺序违规（schema order）**
- 字体强制函数 `_tf()` 曾用 `pPr.insert(0, d)` 把 `<a:defRPr>` 插到 `<a:pPr>` 最前；但 schema 要求 `defRPr` 必须排在 `lnSpc`(行距)/`spcBef`/`spcAft`(段后距)/`buChar`(项目符号)/`tabLst` **之后**、`extLst` 之前。凡设了行距/段后距/项目符号的段落均违序——全稿 24 处。
- **修复**：`pPr.insert(0, d)` → `pPr.append(d)`（本脚本不生成 `extLst`，append 即正确位）。违序 24→0。

**根因 ②：孤儿 notesMaster 关系（orphaned relationship）← 真正让"需修复"顽固不消的元凶**
- `build.py` 用 `s.notes_slide`（第 ~178 行 `notes()`）写演讲者备注。python-pptx 首次访问 `.notes_slide` 时会创建 notesMaster 部件**和** `presentation.xml.rels` 里的 notesMaster 关系（rId8），但**不会**在 `presentation.xml` 里写 `<p:notesMasterIdLst>` 去引用它。
- 结果：一个"声明了却没人引用"的**悬空关系**。PowerPoint 视为包不一致 → 弹"需修复"。（PowerPoint 修复时正是补上了 `<p:notesMasterIdLst><p:notesMasterId r:id=.../>`。）
- **修复**：保存前调用 `_register_notes_master(prs)`——找到 notesMaster 关系的 rId，在 `presentation.xml` 里插入 `<p:notesMasterIdLst>`（schema 位：`sldMasterIdLst` 之后、`sldIdLst` 之前，用 `sldIdLst.addprevious(nmil)`）。见 `build.py` 结尾。
- **诊断方法（决定性）**：让 PowerPoint 修复并**另存为新文件名**，解压前后两个 pptx，做**结构化 diff**（解析成元素树，比标签结构、忽略空白/属性顺序），过滤掉每页通用的规范化噪音（PP 每次另存都会加 `xfrm`/`endParaRPr`、重排 `bodyPr` 属性、合并同格式 run、给表格加 `colId/rowId`——这些**不丢内容、不触发弹框**），剩下的非通用差异（这里是 `presentation.xml` 多出的 `notesMasterIdLst`）就是真正被修复的点。

> 结论：点"修复"是**安全的**——除补登记 notesMaster 外，PowerPoint 对本 deck 做的全是静默规范化，不丢任何文字/图片/形状/数据。

### 红线规则（REDLINES，必须遵守）

1. **禁止自动缩放字号**（`normAutofit` / `fontScale` / 逐框缩字）——用户明确厌恶（"很坏的习惯"）。放不下就**改文案**（行末留白）或**补足成规整多行并调高文本框**；按内容重要性与表达性取舍。
2. **字号只用这些档位**：正文 `12 / 16 / 20 / 28`、表格 `14`、展示层 `40 / 54 / 96`。新增文本必须落在这些档位（详见「字号方案」）。
3. **操作 `pPr / rPr / spPr` 子元素必须按 OOXML 顺序 `append`/定位插入，禁止 `insert(0)`**（否则触发根因①）。
4. **用了 `s.notes_slide` 就必须 `_register_notes_master(prs)`**（否则触发根因②）。
5. **改完必须复跑校验**（见「验证配方」）：真实 TNR 测宽 + 重叠/越界 + 图片计数 + round-trip 重开 + defRPr 顺序 + **孤儿关系检查**。
6. 图片一律走 `pic()`（读 `p.height`）；不裁剪、不编辑图片内容。
7. **永远另起新版本**（v0.5…），不覆盖旧版；**绝不删除 pptx**（要删先移回收站并通知用户）。
8. 所有措辞与数值必须与 `main.tex` 一致，不升级也不降级表述强度。

### 字号方案（4 档正文 + 展示层 + 表格单一档）

| 层级 | pt | 用途 |
|---|---|---|
| T1 | **28** | 幻灯片标题、章节标题、stat 卡巨数（`S_TITLE/S_SECTL/S_KICK`） |
| T2 | **20** | claim 副标题、正文句、流程/阶段标签、section 提问 |
| T3 | **16** | 卡片标签(粗)+卡片正文+takeaway+chip+公式(`S_FORM`) |
| T4 | **12** | 图注、页脚、进度条、细注、封面副信息 |
| 表格 | **14** | 仅 `add_table`（`fs=hfs=14`） |
| 展示层 | **40 / 54 / 96** | 封面标题+超大对比数(40)、Q&A "Questions?"(54)、章节大数字(96) |

改字号改 `S_*` 常量块；**用 token 级替换**（`size=NN`、`expr_size=NN`、`fs=/hfs=`）而非裸数字全局替换（后者会误伤坐标）。校验：解析生成的 pptx 统计实际字号应 = `{12,16,20,28}` + `14` + `{40,54,96}`，无杂散值。

### `pic()`：零漂移图注锚点

python-pptx 只指定 `width` 时会**自动按真实宽高比算 height**，`shape.height`（EMU，914400/inch）就是精确渲染高度。`pic()` 读它来放图注 → 换图无须改代码、图注锚点与 PowerPoint 所见完全一致、图注宽度自动 = 图实际宽度。

```python
def pic(s, fname, l, t, width=None, height=None, caption=None):
    path = os.path.join(FIG, fname + ".png")
    kw = {}
    if width:  kw["width"]  = Inches(width)
    if height: kw["height"] = Inches(height)
    if not kw: kw["width"]  = Inches(8)
    p = s.shapes.add_picture(path, Inches(l), Inches(t), **kw)
    rh = p.height / 914400.0     # 真实渲染高度
    rw = p.width  / 914400.0
    if caption:
        txt(s, l, t + rh + CAP_PAD, rw, 0.34, caption, S_CAP, False, MUTED, PP_ALIGN.CENTER, italic=True)
    return rh
```

图注占位 = `CAP_PAD(0.06") + 文本高(0.34") = 0.40"`。逐页复核：图注底 = `t + rh + 0.40"` 须 ≤ `FOOT_RULE − 0.15`（≤7.01"）且小于下方第一个元素顶部。

### stat_card 高度红线（避免 sentence 溢出重叠）

`stat_card(s,l,t,w,h,big,label,sentence,...)` 内部布局固定：巨数 `t+0.16`(h0.66) → 标签 `t+0.86`(h0.36) → sentence `t+1.26`(h=`h-1.36`)。**带 sentence 的卡 `h` 必须 ≥ ~1.55**，否则 sentence 高度算成负值、文字溢出到卡外，落到下方元素上（v0.4 第 48 页 `+26%` 卡 `h=1.10` 时 "32→16-bit model." 溢出叠到 Freshness 蓝框、几乎不可见）。只放大数+标签（无 sentence）时可用 `h≈1.10`。**另：label 也只占单行(h0.36)**——若卡太窄使 label 折行(如 `w=2.85` 放 "Throughput (compilation)")，第二行会叠到 sentence，故卡宽须满足 `w-0.40 ≥ label 单行宽`（16pt bold 实测：`Throughput (…)` ≈2.5″ → `w≥3.1`）。校验：见「验证配方」重叠检查（会报 sentence 底 > 卡底的越界）。



一次性测量（非常驻工具）：用本机真实 Times New Roman ttf
（`/System/Library/Fonts/Supplemental/Times New Roman*.ttf`，含 Bold/Italic/BoldItalic），
生成后逐框 `PIL.ImageFont.getlength` 精确测宽（**与本机 PowerPoint 渲染一致**），
按每 run 的字号/粗体/斜体求单行宽度与框内宽比较；单行填充率 >~90% 视为折行风险。
读字号须回退链 `run→段落→默认`（chip/txt 常把字号设在段落级）。
处置一律**改文案 / 调框**，零缩放。最终：填充率 >86% 的单行框 0 个、多行卡片 body 溢出 0 个。

### 布局常量

```python
CONTENT_X0     = 0.55    # 内容区左边界
CONTENT_W      = 12.23   # 内容区宽度（右边界 12.78"）
CONTENT_TOP    = 1.98    # 标题下方内容起点
CONTENT_MAX_Y  = 6.50    # 主内容底部上限
TAKE_Y_MAX     = 6.55    # take() 顶部上限（底 7.09"，footer 7.16"）
FOOT_RULE      = 7.16    # 页脚线
COL2_GAP       = 0.15    # 两列间距（每列 w=6.04"）
COL3_GAP       = 0.22    # 三列间距（每列 w=3.93"）
CAP_PAD        = 0.06    # 图与图注垂直间距
```
幻灯片尺寸 13.33"×7.50"（widescreen）；安全底 y=7.09"。

### 验证配方（改完必跑，其他 agent 可复用）

1. **重叠/越界**：`python-pptx` 遍历每页 shape `(left,top,width,height)`，报 ①底边 >7.09" 的非页脚/非进度条元素；②两"实文本框"（各 >3 字符）横纵重叠均 >0.15" 且非包含关系。过滤既有设计（footer y≥7.16、进度条 y<0.5、chip 填充+文字同位、卡片内 strip/label 被外框包含）。
2. **真实 TNR 单行测宽**：见「溢出」节。
3. **schema 顺序**：解压后正则/`lxml` 抓 `<a:pPr>`/`<a:rPr>`，检查 `defRPr`/`latin` 等子元素下标是否升序。
4. **孤儿关系**：对每个 part，收集正文里所有 `r:id` 引用，对比其 `.rels` 声明；除 implicit 类型（slideLayout/slideMaster/notesMaster/theme/image/notesSlide/slide 反链等）外，声明了却无人引用即孤儿。**注意 notesMaster 从 `presentation.xml` 引用是 explicit（须有 `notesMasterIdLst`），不是 implicit。**
5. **图片计数**：源码 `pic()` 调用数 == pptx 中 `shape_type==13` 的图片数（无丢图）。
6. **round-trip**：`Presentation('...').slides` 能正常重载。

---

## Design Strategy & Principles

- **Thesis-level argument**，不是三个 paper talks
- **55–60 main slides** + **15–25 backup** for 50–60 min defense
- **Claim-driven titles**，少用表格，多用视觉证据
- **Times New Roman only**，每个角色一个字号，不自动缩放
- **Palette**：NAVY / GOLD / GREEN / RED / MUTED，不用手绘图
- **Self-contained slides**：关键页含 claim + evidence + how-to-read + thesis connection（方法/概念页可依赖上下文，不必强求每页四要素）
- Figures 按论文组织：`gve/`(Ch3)、`mglvr/`(Ch4)、`gmpgr/`(Ch5)；`thesis-framework.png` 在 figures 根
- 所有修改与 `main.tex` / `THESIS_OUTLINE.md` 保持一致（数值/引用/结论/图表标注全对齐）

### Common Mistakes to Avoid
- ❌ 直接删除 pptx 文件 / 覆盖现有版本而不新建版本
- ❌ 假设某 figure 不再需要而不查 `build.py`
- ❌ 改论文内容后忘记同步 slides；图表标注与论文不一致
- ❌ 在 slides 中用论文里没有的术语或缩写
- ❌ `insert(0)` 操作 OOXML 子元素 / 用了 notes 却不登记 notesMaster（→ PowerPoint 需修复）
- ❌ 自动缩放字号

## Iteration History

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | Jul 3 | Initial build with basic structure |
| v0.2 | Jul 3 | Incremental revision: factual fixes, visual hierarchy, layout polish |
| v0.3 | Jul 7 | Aesthetic pass + content-faithfulness pass（wording、图注 callout、叙事连贯） |
| v0.4 | Jul 8 | 图注锚点根治(`pic()` 读真实高度)、布局常量、`take` 越界修复、逐页重排；新增 MG-LVR Benchmark Construction 页；A2-1 改比较表；Q&A 6→3 页合并；**字号收敛 4 档**；**单行溢出系统性根治**；**两个 OOXML 修复：defRPr 顺序 + notesMaster 登记 → PowerPoint 不再需修复**；末轮:第 48 页主图放大满宽+一行三卡(修 stat_card 矮/窄导致的 sentence/label 溢出重叠)、Q&A 删无用 "Response strategy" 金卡并重排；**patch：删 slide 61（冗余 recap 并入 slide 55 takeaway）86→85 张** |

---

## Archive · v0.4 逐页修复记录（历史工作日志）

> 页码 = PowerPoint 侧栏物理序号（封面 = 第 1 页）；共 84 张。**[U]**=用户指出 **[S]**=自查 **[X]**=交叉核对补充。
> 四条最高优先级判据：①字在框里 ②无非设计性重叠 ③每页饱满无大空白 ④视觉重心平衡。

### 主线正文
- **11 Universal Video Retrieval [U]**：`uvr` 居中 `height=2.0`；两 flatcol y=4.12 bh=0.90；warn_card y=5.55 h=0.95；删 gold_card；take y=6.55。⚠**偏离**：新 `pic()` 使图注宽=图宽与两侧 flatcol 标签重叠 → **删该图注**（标题+warn 卡已说明）。
- **12 UVRB Protocol [X]**：`pic()` 通用修复即可（图注 y=4.59）。
- **13 UVRB Reveals Gaps [X]**：`pic()` 通用修复（图注 y=6.46，距页脚 0.36）。
- **15 V-SynFlow [X]**：flatcol → y=5.00（原缝隙仅 0.04）。
- **17 GVE Unified Embedding [U]**：`model` 居中 `height=2.5`；下方 3 列 flatcol/mathbox/result_card y=5.05。⚠**偏离**：Objective 卡加高 `h=1.50`。
- **18 Modality Pyramid Curriculum [U]**：`modality-pyramid` 居中 `width=4.0`；下方两列 y=6.00；省 take。⚠**偏离**：info body 缩一行 + `h=1.05`（原 h=1.00 body 仅 0.40 溢出）。
- **19 GVE Zero-Shot [U]**：整页重排——表格不动；右上双 stat_card（+6.5% / +7.3%）；右下 info_card(Efficiency)；删 gold_card；take y=6.10。（左下约 1" 留白，判为重心平衡保留。）
- **20 Where Gains Come From [S]**：`caption y=5.85` + `take y=6.40`（纠正早期 caption/take 重叠）。
- **21 UVRD + Curriculum [X]**：`caption y=5.92` + `take y=6.46`。
- **22 Correlation Analysis [S]**：`pic()` 通用修复（图注 y=4.73）；3 info_card y=5.22。
- **23 Inter-Ability Correlations [U]**：`corr_matrices` 居中 `height=2.6`；3 列信息卡 y=5.10 h=1.60。
- **29 MG-LVR Benchmark [U]**：`statistics` 左对齐缩到 `width=5.5`；**删对比表→附录 A2-1**；右侧 4 张 stat_card 2×2；take y=6.30。⚠**偏离**：stat 卡加宽到 `w=2.93`、加高 `h=1.90`、`y=1.98/3.92`，保留精确计数（`FN 4,706 · MD 4,142 · CR 1,123.`）。
- **30 MG-LVR Benchmark Construction [U]（新增页）**：`mglvr/mg-lvr` `width=11.0`(l=1.16,t=2.02)；claim 传构造动机一句话。
- **31 Coarse–Fine Gap Universal [U]**：表 h=3.85 保留；**删 gold_card**（并入 take）；take y=6.05。
- **33 Temporal Scaling [X]（新增）**：两卡下移 y=4.90；standalone `caption y=6.55`。
- **34 Fixed Token Budgets [X]（新增）**：两卡下移 y=4.90；`caption y=6.55`。
- **40 Web-Scale Retrieval [U]**：统一到 CONTENT_X0/W——chip `sw=2.206`、mathbox+warn_card gap=0.15、gold_card 满宽。⚠**偏离**：warn "The catch" 恢复 `h=1.45`（与 mathbox 同高）。
- **42 Neural Metrics Break Traversal [U]**：两列统一 gap=0.15；底行两框统一 h=1.15 底对齐。
- **46 GMP-GR Coverage/Recall/Speed [U]**：两统计框 `w→3.40`（消水平重叠）；`pic()` 修复后图注底 6.06；take y=6.28 不动。
- **48 System-Level Execution [U]**：`Application` banner 放大为**满宽** `width=12.23`（h≈2.65，B4.63）；下方改为**一行三卡**——两张 stat_card(+74%/+26%) 各 `w=3.15 h=1.73`(l=0.55/3.85) + Freshness info_card `l=7.15 w=5.63 h=1.73`。⚠**修复两处重叠**：①原 stat_card `h=1.10` 太矮，sentence 溢出卡外叠到 Freshness 蓝框；②收窄到 `w=2.85` 后 label "Throughput (compilation/quantization)"(16pt≈2.5″) 折行又叠到 sentence → 卡宽必须让 label 单行(`w-0.40 ≥ label 宽`，这里 `w=3.15`→内 2.75 ≥ 2.54)。见「stat_card 高度红线」。
- **49 Ablation Metric+Graph [U]**：`pic()` 通用修复（各图注底 5.58）；`caption y=6.55`。

### 附录
- **64 (A1-2) Radar [U]**：`uvrb_radar_tasks`(竖图) 改 `width=3.0`（图注底 6.02）；右侧 3 卡 x=3.80。
- **66 (A1-4) Training Dynamics [U]**：两图 `width=5.5`；info_card → y=5.70 h=1.10。标题精简为 "A1-4 GVE Training Dynamics"。
- **67 (A1-5) Test-Time Scaling [X]（新增）**：gold_card → y=5.55 h=1.10。
- **68 (A1-6) Data Scaling [S]**：`pic()` 通用修复（图注 y=5.66）。
- **70 (A2-1) [U]**：内容由 `mg-lvr` 构造图 → **MG-LVR vs. Prior Long-Video Benchmarks 比较表**。
- **73 (A2-4) Spatial Scaling [U+X]**：图 `width=10.0` 居中（图注底 4.55）；两卡 y=4.75 h=1.55；`caption y=6.45`。
- **74 (A2-5a) Error Type 1 [U]**：图 `width=9.5` 居中；脚注 → y=6.35（12pt）。
- **75 (A2-5b) [U]**：标题精简为 "A2-5b Error Analysis: Temporal Miss & Partial Constraints"。
- **77 (A3-2) Ablation All Four Metrics [U]**：删独立 caption，说明并入 info_card(y=4.62,h=1.80)。标题精简 "A3-2 Ablation: All Four Metrics"。
- **79 (A3-4) Service-Level Traffic [X]（新增）**：两图 `width=4.0`（正方形，图注底 6.42）；右侧 info_card l=9.60 w=3.18 h=4.00。标题 "A3-4 Service-Level Traffic and Latency"。
- **80 (A3-5) Server-Level Traffic [U]**：两图 `width=4.75` 居中（图注底 6.22）；`caption y=6.35` 代 info_card。
- **81 (A3-6) Query-Level Traffic [U]**：`pic()` 修复后图注底 4.19；gold_card y=4.25 h=1.40；info_card y=5.80 h=1.20。
- **82–84 (Q&A, 3 页)[U]**：6 页合并为 3——每页两张 info_card 上下排。**删除通用 "Response strategy" 金卡**（三页内容雷同、纯套话、无信息量，用户判为无用）；删后把两卡重排为 `y=2.20/4.55, h=2.05`(B4.25/6.60) 填满页面、视觉重心平衡。

### 图片实测宽高比（PIL，设计参考）
采用 `p.height` 方案后运行时不再需要此表，仅作 width/height 选择参考。关键：`gmpgr/service_{1,2}_traffic_latency` aspect=**1.000**（正方形，慎用大 width，width=4.5 即高 4.5"）；宽扁图 `mglvr/*_scaling`、`st_tradeoff` aspect≈5.0；竖图 `gve/uvrb_radar_tasks` aspect=0.825。完整像素尺寸见 git 历史 `layout-issues-v0.4.md`。

---

---

## Content Audit — v0.4（2026-07-08，对照 main.tex 核查）

> 数值层面高度忠实，无编造。问题集中在**概念框架和论证语气**。

### 🔴 严重问题（答辩时可能被直接质疑）

1. **Slide 29 — "96% Audited" 误导**：幻灯片将 96% 审计率与 9,971 条全量数据并列，但论文明确写 "over **50** query-video pairs"。改为 "96% accuracy on 50 audited pairs"。
2. **Slide 49 — "five servers each" 无依据**：论文 Ch5 写 "two services supported by five servers"（共 5 台），幻灯片加 "each" 变成 10 台。去掉 "each"。
3. **Slide 13 — Unite-7B VIS 错误来源于论文正文笔误**：论文正文 line 360 写 "Unite-7B (VIS: 0.702)"，但表格 Table 3.2 显示 Unite-7B VIS = 0.666，UniME-7B VIS = 0.702。幻灯片用 "an 8B MLLM (0.702)" 回避了模型名，但引用来源是论文的错误文字。
4. **Slide 6 — "Benchmark World vs. Production Reality" 框架为幻灯片自创**：论文从未构建此四轴二元对比；幻灯片底部 "Each production stage exposes a bottleneck…" 过度泛化。

### 🟠 高优先级措辞问题

| 幻灯片 | 当前措辞 | 论文实际 | 建议 |
|--------|----------|----------|------|
| 11 | "reveals nothing" | ρ=0.58（中等相关） | "reveals little about" |
| 14 | "scaling paradox" | "Limited Impact"（可解释） | "anomaly" |
| 16 | "the most effective" | 从未与其他数据集规模比较 | "more effective than naive scaling" |
| 19 | "data quality beats parameter count" | 归功于 data + curriculum；GVE-7B > GVE-3B | "data quality and curriculum design compensate for smaller model size" |
| 41/43 | "worthless / useless" | "degrades retrieval efficiency" | "accuracy gains are lost at search time" |
| 60 | "released" | "will be publicly released upon acceptance" | "to be released" |

### 评委最可能挑战的 5 个问题

1. **"Your 'Benchmark World vs. Production Reality' table is not in your thesis. Where does this framework come from?"** (Slide 6)
2. **"You say MSR-VTT 'reveals nothing,' but your own data shows ρ = 0.58. That is not nothing."** (Slide 11)
3. **"You claim 'data quality beats parameter count,' but GVE-7B beats GVE-3B. Doesn't parameter count also matter?"** (Slide 19)
4. **"You call the visual finding a 'scaling paradox,' but you explain it clearly. If you can explain it, it is not a paradox."** (Slide 14)
5. **"You say the problem is 'solved stage by stage.' Two of your three papers are still under review. Is it solved, or is it preliminary?"** (Future Work slides)

---

*Last updated: 2026-07-08 · 设计系统库：`slides/build.py` · 产出：`slides/thesis-slides-v0.4.pptx`（85 张；0 重叠 / 0 越界 / 0 文字溢出 / 无丢图 / PowerPoint 正常打开无需修复 / 字号 4 档正文+展示层）*

---

## Current Version · v0.5 (2026-07-14; build layout maintained 2026-07-18)

- The earlier `Files` block is retained verbatim as the v0.4 historical snapshot. This section supersedes only its current-version designation.
- `thesis-slides-v0.5.pptx` is the latest defense deck. Its content is the fully reviewed former v0.6.6 candidate, consolidated under the requested v0.5 version number.
- It contains 79 slides: 56 main-talk slides including Questions, one backup divider, and 22 backup slides.
- The complete v0.5-to-v0.6.x evolution, committee-review decisions, evidence-boundary corrections, rebuild instructions, and QA record are consolidated in `v0.5-final-changelog.md`.
- All v0.5 build code is grouped under `v0.5-build/`. Run `v0.5-build/build-v0.5.py` as the single rebuild entry point. The historical v0.1–v0.4 PPTX files and the original README content above remain unchanged.
- The 2026-07-18 cleanup changed only the location and names of internal build scripts. A fresh rebuild remained semantically identical to the delivered v0.5 in visible text, tables, and speaker notes.
- All v0.6.x PPTX checkpoints were moved to the macOS Trash after their final content was incorporated into v0.5. No thesis `.tex` file or thesis figure was changed.
