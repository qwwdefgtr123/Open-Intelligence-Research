# PROJECTS.md — 候选项目比较与采用决定

> 状态：Phase 1（生态调研）产物。调研日期 **2026-11-13**（元数据取自 GitHub API，star 数与最后提交时间均为此日快照）。
> 本文件只记录**实际读到的东西**。凡是只看了 README 或只列了目录的，一律标注为「初步研究」，不得写成「已借鉴」。

## 状态标记约定

| 标记 | 含义 |
|---|---|
| `DEEP` | 已深入研究：读过入口文件与至少 2 个核心实现文件 |
| `SHALLOW` | 初步研究：读过 README / 文件树，未读核心实现 |
| `REF` | 仅作参考：只用于确认生态位或打包形式 |
| `ADOPT` | 已决定采用（思想或结构） |
| `REJECT` | 已决定不采用（并写明理由） |
| `UNVERIFIED` | 尚未核实（含仓库不存在 / 无法访问） |

## 关系标记

- **已借鉴**：读过实际实现，且特定设计已进入 OIR 设计。
- **参考**：读过，但未采用，或仅作背景。

---

## 1. 总览表

| 项目 | URL | Star | 最后提交 | 许可证 | 研究状态 | 关系 | 一句话结论 |
|---|---|---:|---|---|---|---|---|
| structured-analysis | github.com/bushrabeg/structured-analysis | 1 | 2026-09-10 | MIT | DEEP / ADOPT | 已借鉴 | 八个分析框架的**触发与深度强制**机制可直接继承；但它只做**单次**分析，没有证据闭环 |
| agent-studio | github.com/nraford7/agent-studio | 3 | 2026-10-17 | MIT | DEEP / ADOPT | 已借鉴 | 多视角面板的**硬规则集**（隔离、反从众、反均值混合、source check、基线对照）是目前见到最扎实的工程化反从众实现 |
| stress-test | github.com/yogsoth-ai/stress-test | 2 | 2026-06-21 | Apache-2.0 | SHALLOW / REF | 参考 | 110 个细粒度对抗检验 skill 的方法**清单**有价值，但碎片化，单 skill 仅 1.4–5.8 KB，未形成闭环 |
| scientific-agent-skills | github.com/K-Dense-AI/scientific-agent-skills | 56,949 | 2026-11-09 | MIT | SHALLOW / REF | 参考 | 177 skills + 471 MB 的**库级组织方式**是分发层参照；与 OIR 方法论无关 |
| deep-research | github.com/alirezarezvani/deep-research | — | — | — | UNVERIFIED | 不采用 | **仓库不存在（API 404）**。原始候选清单中的该条目已失效 |
| snowglobe | github.com/IQTLabs/snowglobe | 62 | 2026-02-11 | Apache-2.0 | SHALLOW / ADOPT | 已借鉴 | In-Q-Tel 的 LLM 兵棋框架；**裁决者（adjudicator）**角色设计可继承 |
| ROMANCER | github.com/RANDCorporation/ROMANCER | 11 | 2024-10-14 | MIT | SHALLOW / ADOPT | 已借鉴 | RAND 核危机模型；**多阶心智理论（theory-of-mind）**是主体建模的关键缺失件 |
| Geopol-Modeller | github.com/danielrosehill/Geopol-Modeller | 4 | 2026-04-13 | Apache-2.0 | SHALLOW / REF | 参考 | snowglobe 的工程化分叉（LangGraph + YAML 主体 + 预测打分），证明「预测留档 + 事后评分」可行 |
| OASIS | github.com/camel-ai/OASIS | 5,423 | 2026-11-09 | Apache-2.0 | UNVERIFIED / REF | 参考 | 百万级 agent 社会模拟，规模取向与 OIR 相反（OIR 要少而深），仅作生态位对照 |

> 说明：star 数普遍很低（1–62），这不是缺陷信号而是**领域事实**——「结构化情报分析 + Agent Skills」这个交叉点目前没有成熟项目。这既说明 OIR 有真空，也说明**没有可直接抄的现成答案**。

---

## 2. 逐项目记录

### 2.1 structured-analysis（DEEP，已借鉴）

**实际读取**：`SKILL.md`（21,686 B，全文）、`README.md`。仓库仅 3 个文件，无脚本、无 schema、无模板目录。

**它做什么**：把情报分析 tradecraft 的八个框架（Genealogy / Actor Mapping / Red Team / STEEP / Key Assumptions Check / Scenario 2x2 / Second-Order Effects / ACH-PreMortem-WhatIf）做成一个 Claude Skill。选框架 → 声明选择 → 深跑。

**真实机制（不是 README 宣称）**：
- 四步选框架决策流：显式覆盖 → 触发词典匹配 → 主题类型默认匹配 → 声明并等待。
- **强制深度**：每个框架都有 `Required output sections` 与 `Failure modes to avoid`。这是全文最有价值的设计——它用输出结构对抗「五条 bullet 式敷衍」。
- 默认只跑 **两个**框架而非五个，理由是「两个跑深 > 五个跑浅」。
- 每个框架自带 steel man 与 source quality note。

**继承**：框架的「必填输出段 + 明确失败模式」写法；「选了哪个方法要显式声明」的透明节拍；深而不广的默认值。
**不继承**：单次分析、无状态、无证据台账、无迭代。它的 Actor Mapping 只有 stated vs revealed interest + 联盟图 + 位置快照，没有派系、决策规则、心智理论层级。
**OIR 改进**：把「输出结构强制」升级为「**schema 强制**」——不是要求写某一节，而是要求写入可校验的实体；把「一次选两个框架」升级为「跨轮次的方法调度」。

### 2.2 agent-studio（DEEP，已借鉴）

**实际读取**：`SKILL.md`（10 KB 全文）、`references/hard-rules.md`（全文，13.9 KB）、`references/synthesis-modes.md`（前半）、`methodologies/kernel.md`（片段）、`references/evidence-gate.md`（部分）、`references/roster.md`（部分）、文件树（84 项）。未读：`scripts/*.py`、`docs/research/*`（约 180 KB 研究圣经）。

**它做什么**：判断一项工作到底需不需要「人格/面板」，需要时招聘、运行、检验一个多视角 agent 面板，并强制与单模型基线对照。

**真实机制**：
- 四条前置门（door 1–4），door 4 = 一次性面板，走 8 步：Frame → Gate → Hire → Assemble → Run → Synthesize → Check → Report。
- **隔离是硬规则**：一个 lens 一个全新 subagent，禁止在同一 context 内换人格（明确称为「maximally-colluding anti-pattern」）。
- **反从众是一等公民**：每个 lens 的 prompt 注入固定前言，要求「只从自身立场推理、不得预判他人、必须给出 Dissent I would defend」。
- **禁止 naive-mean-blend**，默认用 dissent-carrying synthesis（多数意见 + 标注的少数意见 + 独有发现）。
- **SOURCE CHECK**：交付前由全新 checker 逐条比对来源，标 SUPPORTED / UNSUPPORTED / CONTRADICTED。
- **基线可以否决面板**：每个面板都必须跑一条「纯单模型」对照；若单模型在决定性标准上更好，**就交付单模型**，并说明原因。
- 强制同时报告质量与覆盖（kept N of M points），并报成本。

**继承（几乎整套反从众纪律）**：隔离、反预判前言、dissent 保留、SOURCE CHECK、基线对照、质量+覆盖双报告、成本实报。
**不继承**：persona 招聘/名册/field-evidence 那套「人味」外壳（OIR 的 agent 是**分析角色**不是**被雇的人**）；`NO WebFetch` 硬禁令（那是它为规避摘要器失真作的选择，OIR 需要按平台工具能力决定）；它的证据门（evidence gate）用于判断「人格是否有用」，与 OIR 的「证据是否支持假说」不是同一件事，不能混用。
**OIR 改进**：把它的「面板 vs 基线」对照，从**运行期检查**升级为 OIR 的**研究方法本身**（Mode A 基线是 OIR 的一等模式，而不是事后抽查）；把 SOURCE CHECK 从交付前一次性检查，升级为贯穿 Source Dependency Graph 的**持续**记账。

**许可证**：MIT。上述均为**借鉴思想**，OIR 不复制其代码或文档原文；若未来复用 `run_check.py` 等脚本，须保留版权声明。

### 2.3 stress-test（SHALLOW，参考）

**实际读取**：文件树（110 个 `skills/*/SKILL.md`）、`README.md` 摘要、`ENTRY.md` 存在性。**未读任何一个 skill 正文**。

**它做什么**：研究产物的对抗性压测引擎，五个 campaign 产出带弱点标注的核验报告。

**观察**：110 个 skill 平均 2–4 KB，命名极细（`counterexample-generation`、`assumption-cascade-tracer`、`circular-validation-audit`、`critical-case-design`…）。这是一份**对抗检验动作的词典**。
**结论**：作为**方法清单**参考，作为**架构**不采用——把方法论切成一万个微 skill 会让 agent 无法判断何时用哪个，且没有状态与闭环。OIR 采用「少量阶段 + 每阶段内含检验动作」的结构。
**后续动作**：Phase 2 若有需要，定向抽取 3–5 个动作（如 `critical-case-design`、`circular-validation-audit`）并入 Red Team 流程，届时再标为「已借鉴」。

### 2.4 snowglobe（SHALLOW，已借鉴一点）

**实际读取**：文件树、`config/*.yaml` 命名、`examples/haiwire_files/*.csv` 结构。未读 `src/llm_snowglobe/` 实现。

**关键机制**：`players respond × N` → `narrator adjudicate` → `next move` 的状态机；场景与主体由 YAML 配置；有 injects（注入事件）。
**继承**：**裁决者**角色。OIR 的主体各自陈述「我会做什么」，但不能各自宣布「我成功了」——必须有一个不站在任何主体立场上的裁决环节，按现实约束判定交互结果。
**不继承**：叙事驱动的多回合推演（OIR 不是兵棋，产出是分析判断而非剧情）；无证据台账。
**许可证**：Apache-2.0。仅借鉴思想。

### 2.5 ROMANCER（SHALLOW，已借鉴一点）

**实际读取**：`README.md`（含引用信息）、仓库元数据。未读 Python 实现。

**关键机制**：RAND 核危机升级模型，明确以「**multiple theories-of-mind**」为核心——决策者不仅有自己的效用，还对对手的信念建立信念。
**继承**：主体模型必须区分 **0 阶（事实）**、**1 阶（我认为 X 会怎么做）**、**2 阶（我认为 X 认为我会怎么做）**。缺了 2 阶，所谓「策略互动」只是两个独白并置。
**不继承**：形式化效用计算与 GUI（OIR 是文本方法论，不做数值仿真）。
**许可证**：MIT（RAND 2024）。仅借鉴思想。

### 2.6 其他已检索但未深入

| 对象 | 状态 | 处理 |
|---|---|---|
| `alirezarezvani/deep-research` | UNVERIFIED（404） | 候选清单失真，记录在此，不再追踪 |
| `K-Dense-AI/scientific-agent-skills` | SHALLOW | 仅取「库级目录组织 + 每 skill 一元数据」的分发经验 |
| `camel-ai/OASIS` | UNVERIFIED | 规模取向相反，仅作生态位对照 |
| `danielrosehill/Geopol-Modeller` | SHALLOW | 「预测结构化留档 + 事后自动评分」思路可参照，但其评分依赖联网检索回填，OIR 只做**留档 + 人工可复核的窗口判定** |

---

## 3. 生态位结论

现有工作可归为三类，**没有一类闭合 OIR 想要的环**：

1. **检索—摘要型**（Deep Research 类）：从问题到一段综合文本。缺主体建模、缺竞争性假说、缺可检验预测。
2. **叙事模拟型**（snowglobe / Geopol-Modeller / OASIS）：从场景到一段推演过程。缺事实核验、缺假说比较、缺证据回填、缺不确定性表达。
3. **结构化检查单型**（structured-analysis / stress-test）：从材料到一份更严谨的分析。缺状态、缺迭代、缺主体间互动。

OIR 的差异不在「更多 agent」，而在**把三者串成一条能被证据打断并修正的回路**：主体模型 → 竞争性假说 → 区分性预测 → 定向取证 → 独立反驳 → 状态更新 → 下一轮。

这也决定了 OIR 的成本结构：贵在**隔离运行**与**多轮取证**，不在 agent 数量。因此规模方案必须与「轮数」和「取证预算」一起给，而不能只报 agent 数。
