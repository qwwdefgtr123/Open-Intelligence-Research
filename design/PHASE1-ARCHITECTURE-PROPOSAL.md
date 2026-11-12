# OIR 第一阶段架构提案（待授权）

> 版本：v0.1 · 2026-11-13 · 状态：**提案，未实现**
> 本文件是第二阶段的施工图。授权后其内容将拆解进 `core/CORE_SPEC.md`、`core/workflows/*`、`core/schemas/*`，本文件保留为设计决策记录（design rationale）。

---

## 0. 一句话定位

OIR 不是「让多个 AI 一起给答案」，而是把**主体视角**当作可证伪的分析装置：让不同利益结构的模拟产生**互相竞争的解释**，再让现实证据去**分开它们**，并且允许证据反过来改掉主体模型。

三条不可让渡的性质，决定了它与 Deep Research 类工具的分野：

1. 产出是**被区分过的假说集合**，不是一段综合叙述；
2. 每个重要判断都能回溯到 `FACT-* / EVD-* / SRC-*` 实体；
3. 系统**必须能输**——能跑单 agent 基线并如实对照。

---

## 1. 总体工作流

```
                        用户研究问题
                             │
                    ┌────────▼─────────┐
               S0   │ Intake 问题诊断   │  ← 不合格问题在此被拒（事实查询 → 直接答，不启动 OIR）
                    └────────┬─────────┘
                             │ research.json + plan
                    ┌────────▼─────────┐
               S1   │ 事实底座 Fact Base│  分级取证 → FACT / SRC / CLM 三分离
                    └────────┬─────────┘
                             │ 冻结 FACT-snapshot-v1（所有主体共享同一份文件，不共享对话）
              ┌──────────────┼──────────────┐
              │              │              │        ← 上下文隔离，互不可见
        ┌─────▼────┐   ┌─────▼────┐   ┌─────▼────┐
   S2   │ Actor A  │   │ Actor B  │   │ Actor C  │   各自产出：目标/利益/资源/约束/派系/决策规则/0-2阶信念
        └─────┬────┘   └─────┬────┘   └─────┬────┘
              └──────────────┼──────────────┘
                    ┌────────▼─────────┐
                    │ 交互裁决 Adjudicate│  ← 中立：只认可行行动集与约束，不认主体自述的成功
                    └────────┬─────────┘
                    ┌────────▼─────────┐
               S3   │ 竞争性假说 H-*    │  每个假说必须附带预注册预测 PRD-*
                    └────────┬─────────┘
                    ┌────────▼─────────┐
               S4   │ 区分性取证        │  排序依据 = 能分开几对活假说 × 可得性 / 成本
                    └────────┬─────────┘   空结果（没找到）同样入库
                    ┌────────▼─────────┐
               S5   │ 盲审反方 Red Team │  去身份输入 → 逐条裁决（接受/部分/驳回 + 理由）
                    └────────┬─────────┘
                    ┌────────▼─────────┐
               S6   │ 综合 + 状态更新   │  分解评估 / 模型回溯修订 / 下一轮价值排序
                    └────────┬─────────┘
                             │
                   ┌─────────▼──────────┐
                   │ 停止规则 S1–S5 触发？│
                   └──┬─────────────┬───┘
                      │否           │是
              ┌───────▼──────┐  ┌───▼──────────────┐
              │ 回到 S3/S4    │  │ report.md + 未决清单│
              │ (第 N+1 轮)   │  │ + 停止理由 + 预算实报│
              └──────────────┘  └──────────────────┘
```

**与常见的「多 agent 讨论」流程图的关键差别**：从 S2 到 S3 之间没有「互相辩论」的边。交叉质疑只发生在 S5，而且是**单向、盲审、一轮**。这是文献结论（`references/METHODS.md` §3）的直接后果，不是省成本。

---

## 2. 模块与职责

| 模块 | 职责 | 不做什么 |
|---|---|---|
| **Director**（主 agent） | 问题诊断、事实底座、预算台账、交互裁决、假说合并、停止判定、最终装配 | 不扮演任何现实主体；不在无证据时下结论 |
| **Actor Simulation** | 单一主体模型 + 该主体视角下的行动选项与反应函数 | 不评价其他主体是否理性；不宣布自己行动成功 |
| **Hypothesis Analyst** | 把主体模型与互动结果转成竞争性假说 + 预注册预测 | 不去找证据；不给自己假说打分 |
| **Evidence Investigator** | 按区分性排序执行取证、写来源依赖、记空结果 | 不判断假说真伪；不替主张者找支持材料 |
| **Red Team** | 盲审、找反例/替代机制/被忽略主体/隐含前提 | 不做综合；不重复提出假说 |
| **Synthesis Analyst** | 分解评估、不确定性表达、分歧保留式综合 | 不重新检索（只能读台账） |

---

## 3. 研究状态与数据结构

### 3.1 目录布局

```
research/<slug>/
├── index.json                 # Research 实体 + 各实体注册表 + 预算台账
├── plan.md                    # S0 产出：范围、决策相关问题、规模方案、预算
├── facts/FACT-001.json        # 已核实事实（含 sources[]）
├── sources/SRC-001.json       # 来源（含 derived_from → 来源依赖图）
├── claims/CLM-001.json        # 来源中的主张 / 公开表态
├── actors/ACT-001.json        # 主体模型（含 factions[]、beliefs_about[]、version）
├── simulations/SIM-ACT-001-r1.md  # 主体视角推演（人类可读）
├── hypotheses/HYP-01.json     # 含 predictions[]、status、support、counter
├── predictions/PRD-001.json   # 预注册：窗口 / 指标 / 阈值 / 反向指标 / 判定
├── evidence/EVD-001.json      # 证据 + 强度 + 独立信源贡献
├── investigations/INV-001.json# 调查任务（目标假说对、结果、空结果标记）
├── conflicts/CFL-001.json     # 证据/假说/主体模型之间的冲突
├── assumptions/ASM-001.json   # 关键前提 + 证伪条件 + 影响面
├── decisions/DEC-001.json     # 流程决策（含 red team 裁决、停止理由）
├── uncertainties/UNC-001.json # 未解不确定性
├── iterations/round-01.md     # 每轮状态快照与变更
└── report.md                  # 最终报告（仅停止时生成）
```

**为什么一实体一文件**：agent 可以只读需要的文件（渐进披露），diff 友好，ID 可被直接引用；避免一个巨型 state.json 每次全量重写导致丢字段。`index.json` 只存注册表与计数，不存正文。

### 3.2 实体与关键字段（摘要）

| 实体 | ID | 必填关键字段 |
|---|---|---|
| Research | `RES` | question, scope_in, scope_out, decision_context, scale_mode, budget_plan, status |
| Fact | `FACT` | statement, as_of, sources[], verification_level(`confirmed`/`corroborated`/`single-source`), contradicts[] |
| Source | `SRC` | url, publisher, published_at, retrieved_at, tier(`primary`/`official`/`media`/`ngo`/`social`/`anonymous`), **derived_from[]**, independence_class, interest_note |
| Claim | `CLM` | speaker, venue, date, text, source, type(`statement`/`denial`/`leak`/`analysis`) |
| Actor | `ACT` | identity, factions[{name,weight,goal}], goals[], interests[], resources[], constraints[], relations[], decision_rule, risk_tolerance, options[], reaction_function, **beliefs_about[{actor,order,belief}]**, version, change_log[] |
| Hypothesis | `HYP` | statement, mechanism, scope, assumptions[], predictions[], supporting[], undermining[], relation_to_others(`contradicts`/`overlaps`/`subsumes`/`conditional`), status |
| Prediction | `PRD` | hypothesis, observable, indicator, window{from,to}, confirm_if, disconfirm_if, counter_indicator, registered_at, **judgement**(`pending`/`confirmed`/`disconfirmed`/`inconclusive`/`not-observable`) |
| Evidence | `EVD` | description, sources[], direction(`supports`/`undermines`/`neutral`), targets[{hypothesis, weight}], strength, independence_note, alternative_readings[], obtained_by |
| Investigation | `INV` | question, separates[hypothesis pairs], method, budget, result_summary, **null_result**(bool), evidence[] |
| Assumption | `ASM` | statement, held_by, falsifier, blast_radius, checked(bool) |
| Conflict | `CFL` | between[], description, resolution(`open`/`revised-model`/`revised-hypothesis`), decision_ref |
| Decision | `DEC` | kind(`redteam-verdict`/`model-revision`/`stop`/`scale`/`budget`), rationale, refs[] |
| Iteration | `ITR` | round, inputs_frozen, changes[], open_questions[], voi_ranking[] |
| Budget | 在 `index.json` | runs_used/max, fetches_used/max, rounds_used/max, degradation_level |

Schema 以 JSON Schema（Draft 2020-12）落在 `core/schemas/*.schema.json`，并配 `tests/` 里的校验脚本；**无脚本时不得声称「已校验」**。

### 3.3 三个必须机械强制的约束

这三条不是约定，是校验项——写不进去就意味着设计失败。

1. **`FACT` 与推断物理分离**：主体模型只能引用 `FACT-*` 或 `CLM-*`；引用不存在的 ID → 校验失败（对应失败模式 F4）。
2. **`HYP` 无 `PRD` 即不完整**：假说没有至少一条预注册预测，`status` 只能是 `draft`，不进入评估（F9）。
3. **`SRC.derived_from` 必填（可为空数组）**：转载必须指回根来源；`EVD.independence_note` 必须给出**有效独立信源数**，不是来源条数（F6）。

---

## 4. 七个阶段的具体做法

### S0 Intake
- 判定问题类型（事实型 / 机制型 / 意图型 / 预测型 / 政策型），并**判断是否该用 OIR**。事实型直接答，写 `DEC-` 记录拒绝理由。
- 明确「决策背景」：这个判断会被用来做什么？没有决策背景的开放题，产出必然空泛。
- 输出 `plan.md`：范围、候选主体（来自事实而非臆测）、规模方案、预算、停止条件。

### S1 事实底座
- 分级取证：`primary`（原始文件/数据/条约/财报）> `official`（官方声明）> `media`（需追溯至其引用的原始来源）> `ngo` > `social`。**不同层用不同评价标准，不混算。**
- 每条事实标注 `verification_level`；`single-source` 的事实**不得**作为主体模型的关键前提（可作为待核项）。
- 冻结快照：`index.json` 记 `fact_snapshot` 版本与 FACT ID 列表。所有主体读同一份，确保「共享相同基础事实」是**文件级**保证，不是提示词级承诺。

### S2 主体建模与独立模拟
每个主体一个隔离 subagent，输入只有三样：FACT 快照、该主体的任务书、输出 schema。**不含**其他主体的输出，也不含 Director 的倾向。

每个 subagent 必须回答（写进 `SIM-*.md`，结构化部分进 `ACT-*.json`）：
1. 核心目标与「最怕失去什么」；
2. 内部派系与谁能否决；
3. 在什么条件下会改变策略（reaction_function 必须是**条件式**，不是一句话倾向）；
4. 可行行动集（并标注哪些被自己排除，为什么）；
5. **0/1/2 阶信念**：我认为 X 会怎么做；我认为 X 认为我会怎么做；
6. 我这条判断需要什么现实迹象才能被证伪。

**反预判前言**（每个主体 prompt 固定注入）：只从本主体立场推理；不得预判其他主体将说什么；不得追求「平衡」；结尾必须给一条「即使被所有人反对我也会坚持的判断」。

**交互裁决**（Director）：把各主体的行动集取交集/冲突，按现实约束判定「哪些行动真的会发生」。裁决只依据 `FACT` 与可行性，不依据任何主体的叙事。产出 `CFL-*`。

### S3 假说生成
- 从「主体模型 + 裁决后的互动」推导假说，而非从「网上有哪些说法」推导。
- 每个假说必须有 `mechanism`（为什么会这样，中间步骤是什么）。只有结论没有机制的，退回重写。
- **假说不要求互斥**，但必须标注 `relation_to_others`。强行造互斥是 ACH 的坏习惯。
- 预测预注册在**取证之前**写完并锁定 `registered_at`。事后补写的预测在校验中会被标 `late`。

### S4 区分性取证
排序公式（**序数启发式，不是概率**）：

```
score(INV) = Σ_pairs [ 1 if 该调查能分开这对活假说 else 0 ] × obtainability(0.2/0.5/1.0) / cost(1/2/3)
```
取 top-k 执行，k 由本轮预算决定。每个 INV 必须写明它**打算分开哪一对**；写不出来的调查任务不予执行（那是「主题相关搜索」，不是取证）。

- 强制记 **null_result**：搜了但没有 → 这是信息，必须入库，否则下一轮会重复搜。
- 每条证据必须给 `alternative_readings[]`（至少 1 条其他解释）。给不出的证据视为未评估。
- 冗余折减：同一根来源的第二条证据，`independence_note` 记 `redundant`，权重不计入有效独立计数。

### S5 盲审反方
- 输入**去身份**：隐藏 `actor` 名与假说提出者，只留 HYP-ID 与内容（依据 arXiv:2510.07517）。
- 五类必答：最强假说怎么被推翻 / 替代机制 / 被忽略的主体 / 哪个隐含前提最脆 / 哪条「支持」其实是同源重复。
- **裁决制**：Director 对每条反驳给 `ACCEPT / PARTIAL / REJECT + 理由`，写入 `DEC-`。没有裁决的反审等于没做。
- 经受住审查的假说要**明确记录它通过了哪些检验**——不是只有被推翻才算结果。

### S6 综合与状态更新
- 评估**分解**为四项，不许合并成一个总分：证据支持强度 / 来源独立性 / 预测命中情况 / 逻辑完整性。四项分别写理由。
- **模型回溯检查**（F8）：预测被证伪时，强制判定是「假说错」还是「主体模型错」，二选一或都错，写入 `DEC-model-revision`；主体模型改动必须升 `version` 并留 `change_log`。
- 下一轮价值排序写入 `ITR.voi_ranking`。
- 停止判定（见 §6）。

---

## 5. 子 Agent 规模方案

### 5.1 三个方案

| 方案 | 子 Agent | 组成 | 适用 | 独立性代价 |
|---|---:|---|---|---|
| **精简** | 3 | 2×ActorSim + 1×RedTeam | 单一主体或双主体、边界清晰、时间紧 | Director 同时做假说与综合，锚定风险最高 |
| **标准** | 5 | 3×ActorSim + 1×EvidenceInvestigator + 1×RedTeam | 多主体、多个竞争性假说（默认推荐） | Director 做综合，但取证已独立 |
| **扩展** | 7 | 4×ActorSim + 1×EvidenceInvestigator + 1×RedTeam + 1×SynthesisAnalyst | 主体内部派系复杂、多方博弈、结论将被用于真实决策 | 综合独立，锚定风险最低 |

每个方案都是「Director（主 agent）+ N 个子 agent」。**Director 不计入 N。**

### 5.2 为什么是这个递增方式

每一级只做两件事：**多一个主体**、**多一层独立性**。不增加"协调 agent"——协调本身就是 Director 的职责，多一个只会增加传话损耗。

### 5.3 主体数量从哪里来

**不是从方案档位来，是从「有几个利益结构真正不同」来。** 判定标准：两个候选主体若在「核心目标 + 最怕失去的东西 + 否决者」三项上高度重合，就合并成一个。

典型展开方式（按需，不是模板）：
- 国家 → 拆成行政系统 / 安全系统 / 经济利益集团（**不要**把国家当单一理性人）
- 企业 → 管理层 / 董事会与投资人 / 核心业务部门 / 员工与工会
- 组织 → 正式领导层 / 实际执行层 / 外部资助方
- 另需一个「结构性约束方」（监管者、盟友、对手），因为互动需要对手

### 5.4 能合并 / 不能合并

| 角色 | 能否合并 | 理由 |
|---|---|---|
| 主体 A 与主体 B | **不能** | 隔离是多视角唯一的价值来源；合并即为「同 context 换人格」，是同质性最高的反模式 |
| Red Team 与假说提出者 | **不能** | 自我证明在结构上无效；这是原则 E |
| Synthesis 与 Director | **可以**（精简/标准） | 但必须在报告里声明「综合由流程负责人完成，独立性较低」 |
| Hypothesis Analyst 与 Director | **可以**（全部方案） | 假说生成需要全局视野，Director 天然具备；且扩展方案里用 Synthesis 独立来补锚定 |
| Evidence Investigator 与 Director | 可以（预算极紧时） | 代价是取证与主张分离失效，属于降级项，必须告知 |

### 5.5 角色 → agent 的映射

| 功能角色 | 精简 | 标准 | 扩展 |
|---|---|---|---|
| Research Director | 主 agent | 主 agent | 主 agent |
| Actor Simulation | 子 ×2 | 子 ×3 | 子 ×4 |
| Hypothesis Analyst | Director 兼任 | Director 兼任 | Director 兼任 |
| Evidence Investigator | Director 兼任 | 子 ×1 | 子 ×1 |
| Red Team | 子 ×1 | 子 ×1 | 子 ×1 |
| Synthesis Analyst | Director 兼任 | Director 兼任 | 子 ×1（独立） |

---

## 6. 预算、降级与停止

### 6.1 预算台账（标准方案，3 轮上限）

| 项 | 预估 | 说明 |
|---|---|---|
| 子 agent 运行次数 | 10–13 | 5 首次 + ≤2 主体重跑 + 1 取证×3 轮 + 反审×2 + 综合×1 |
| 单轮取证查询数 | 15–30 | 每轮 top-k，k 由预算定 |
| 全流程查询总数 | 60–120 | 含事实底座 15–25 |
| 并发度 | 3–4 | 主体并行、取证串行（避免重复搜） |
| 轮数 | 2–3 | 第 3 轮只在 VoI 排名仍高时开 |
| 墙钟时间 | 15–35 min | 取决于检索延迟 |

**关于 token 与费用：不做精确数字。** 理由：本环境的模型单价与上下文计费规则不由 OIR 掌握，任何具体金额都是编的。OIR 只报**可观测的量**（runs / queries / rounds），费用由使用者按自己的单价换算：

```
cost ≈ (Σ 各次 run 的 input_tokens × 单价_in) + (Σ output_tokens × 单价_out)
```
报告里必须写「runs 与 queries 为实测，费用未估算」或「按 X 单价折算」，二选一，不许混。

### 6.2 降级阶梯（按剩余预算触发）

| 级别 | 触发 | 动作 | 明示代价 |
|---|---|---|---|
| L0 | 100% | 正常执行 | — |
| L1 | <60% | 轮数 3→2 | 少一轮验证，可能有预测停留 `pending` |
| L2 | <40% | 去掉第二轮反审；心智理论 2 阶→1 阶 | 策略互动判断退化为主体独白并置 |
| L3 | <25% | 取证并入 Director；主体 3→2 | 取证独立性丧失，视角减少 |
| L4 | <10% | 只跑 Mode A 单 agent 基线 | 报告首行必须写「未执行主体模拟」 |

降级是**显式事件**，写入 `DEC-budget` 并在报告里单独一行说明。悄悄降级比不降级更糟。

### 6.3 停止规则

任一触发即停：

| 规则 | 条件 |
|---|---|
| **S1 区分耗尽** | 剩余活假说之间，已无「可获得的证据」能进一步分开；或每一对都已被至少一条诊断性证据处理过 |
| **S2 预算耗尽** | runs / queries / rounds 任一达上限 |
| **S3 无进展** | 连续两轮：无假说状态变更，且无新 FACT 与既有主体模型冲突 |
| **S4 不可观测** | 关键预测的观察窗口在可预见期内不会到来，或来源不可得 |
| **S5 用户停止** | 用户要求停 |

停止 ≠ 问题解决。报告必须列**未决清单**：哪些假说仍无法区分、哪些预测仍 `pending`、哪些事实是 `single-source`。

### 6.4 什么情况不该启动 OIR

- 有唯一正确答案的事实查询；
- 主体只有一方、且无策略互动（此时主体模拟退化为角色扮演，纯增加成本）；
- 信息极度匮乏（连基础事实集都建不起来）——此时应输出「信息不足」而不是模拟。

---

## 7. 不确定性怎么表达（不许伪装成概率）

**不做**：`置信度 78%`。这个数字混装了四种不可通约的东西，且文献显示人类分析员自报信心校准很差（Mandel 2018 的对照实验正是靠外部重校准才降低误差）。

**做**：四栏分解 + 定性档位。

| 假说 | 证据支持 | 来源独立性 | 预测命中 | 逻辑完整 | 综合档位 |
|---|---|---|---|---|---|
| HYP-01 | 3 条支持 / 1 条削弱，其中 2 条同源 | 有效独立 2 | 2/3 已确认 | 机制链有两处跳跃 | **较强，但有单点依赖** |
| HYP-02 | 1 条支持，无削弱 | 有效独立 1 | 0/2 已观察 | 机制完整 | **弱，未被检验** |

档位用语固定为：`较强 / 中等 / 弱 / 仅存疑 / 已排除`，每档附「要变成上一档需要什么」。这样读者知道该看什么，而不是盯着一个假数字。

---

## 8. 平台适配设计

- **核心层**：`core/` 全为平台无关 Markdown + JSON，无任何工具名硬编码。
- **适配层**：`distributions/<platform>/skills/oir/SKILL.md`，只做四件事：识别研究请求 → 按需读取 `core/` 对应文件 → 用**本平台**的隔离机制派发子 agent → 用**本平台**的文件工具写 `research/<slug>/`。
- **隔离机制抽象**：核心层只写「一个主体一个独立执行单元，互不可见」，不写具体是 subagent、`codex exec` 还是独立进程。平台层负责翻译。
- **不能整仓打包**：Skill 入口必须精简，靠 `core/` 的路径导航按需加载。

当前平台（WorkBuddy）已具备：文件读写、子 agent 派发、网页检索。**尚需在 Phase 2 核验**的是用户级 Skill 安装目录与 frontmatter 必填字段——已初步确认 `~/.workbuddy/skills/<name>/SKILL.md`，但**未按官方文档逐项核对，Phase 2 必须补证并注明验证日期**。

---

## 9. Phase 2 交付清单

| 类别 | 文件 | 说明 |
|---|---|---|
| 入口 | `README.md` | 兼作人类与 Agent 的统一入口（含 Agent Reading Guide、目录索引、来源清单、局限） |
| 核心 | `core/CORE_SPEC.md`、`core/PRINCIPLES.md` | 原则可执行化，每条附「违反时怎么发现」 |
| 工作流 | `core/workflows/01–06` | 六个阶段，含输入/输出/校验点/失败模式 |
| 角色 | `core/roles/*.md`（6 个） | 每个含：职责、必答问题、禁止事项、输出 schema 指向、固定前言 |
| Schema | `core/schemas/*.schema.json`（7 个） | Draft 2020-12 |
| 模板 | `core/templates/*.md`（6 个） | 人可读产出 |
| 分发 | `distributions/workbuddy/skills/oir/SKILL.md` + 至少 2 个其他平台 | 每个附安装路径与验证方法 |
| 打包 | `packaging/PACKAGING.md`、`PLATFORM_COMPATIBILITY.md` | 后者必须附官方文档链接 + 验证日期 + 「未验证」标注 |
| 测试 | `tests/` | 结构检查、frontmatter 检查、schema 校验脚本、工作流完整性、四模式对照实验协议 |
| 治理 | `LICENSE`(MIT 拟)、`CHANGELOG.md`、`CONTRIBUTING.md` | 未获授权不推远程 |

**不会做的事**：不创建空文件凑结构；不在没有实测的情况下写「已通过测试」；不在未授权时创建 GitHub 远程仓库。

---

## 10. 已知风险（Phase 1 结束时点）

1. **最大风险是「看起来很深，实际没区分力」**。缓解：S4 强制「写不出要分开哪一对就不许执行」，S1 停止规则强制承认区分耗尽。
2. **主体模拟容易被读成事实**。缓解：schema 层禁止把 `ACT` 内容写入 `FACT`；报告里主体判断永远带「模拟」标记。
3. **Red Team 可能沦为表演**。缓解：裁决制 + 必须锚定 ID + 记录经受住的检验。但这仍是最弱的一环，Phase 2 要为它设计可检验的自检（例如：反审是否提出了至少一条导致假说状态改变的发现？若连续两轮为零，说明反审失效）。
4. **没有对照实验就没有资格说更好**。缓解：Mode A/B/C/D 四模式协议必须真的能跑，并在 `tests/` 留出可执行步骤。若本次无法实跑，报告中必须写「未验证」。
5. **成本不确定**。缓解：只报可观测计数，费用交使用者换算；不编金额。
