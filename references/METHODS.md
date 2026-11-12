# METHODS.md — 方法继承、修改与来源追踪

> 状态：Phase 1（方法论研究）产物，2026-11-13。
> 本文件回答一个问题：**OIR 的每一条规矩，从哪里来，为什么改成现在这样。**
> 凡标「借鉴思想」者，OIR 不复制原文；凡标「直接复用」者，必须附许可证与署名。**当前无任何直接复用代码或文档。**

## 0. 三种关系

| 关系 | 含义 | 义务 |
|---|---|---|
| 借鉴思想 | 读过其实现，理解机制后独立重写 | 在 README 与方法表署名来源 |
| 直接复用 | 复制代码/文档/提示词原文 | 遵守原许可证 + 保留版权声明 + 标注改动 |
| 参考 | 读过但未采用 | 仅列入 PROJECTS.md |

## 1. 继承总表

| # | 方法 | 来源 | OIR 继承 | OIR 修改 | 关系 | 许可证 | 落位 |
|---|---|---|---|---|---|---|---|
| M1 | Actor Mapping | Heuer & Pherson SATs；structured-analysis 框架 2 | stated vs revealed interest；off-stage actor；否决权；位置快照 | 升级为**带派系与决策规则的主体模型**，加心智理论层级与修订触发器 | 借鉴思想 | MIT（structured-analysis） | `core/workflows/02`、`schemas/actor` |
| M2 | ACH | Heuer 1999 | 竞争性假说必须显式；**证据诊断性**优先；对所有假说同等一致的证据无价值 | **拒绝**独立打分矩阵与排除法计算；改为诊断性提问 + 来源依赖性记账 | 借鉴思想（并部分否定） | 公共领域方法 | `core/workflows/03`、`04` |
| M3 | Key Assumptions Check | Heuer & Pherson；structured-analysis 框架 5 | 关键前提显式化、找反证条件 | 前提成为**一等实体**（含证伪条件、影响面、负责人）；扩展到主体模型内部前提 | 借鉴思想 | MIT | `schemas/assumptions`、`workflows/05` |
| M4 | Red Team / Devil's Advocacy | 美军 red teaming；structured-analysis 框架 3；agent-studio critic | 角色分离；steelman 先行；专攻最有力假说 | **盲审**（去身份）+ **裁决制**（每条反驳必须被接受/驳回并给理由）+ **范围约束**（防过度对抗） | 借鉴思想 | MIT | `core/workflows/05`、`roles/red-team-analyst` |
| M5 | Scenario Planning | Shell/GBN 2x2；structured-analysis 框架 6 | 触发条件与路标（signpost） | 取消 2x2 图式美学；只保留「条件性情景 + 可观察路标」，并入 Prediction 实体 | 借鉴思想 | MIT | `schemas/prediction`、`workflows/03` |
| M6 | Multi-Agent Debate | Du et al. 2023 起一脉；agent-studio 面板 | **独立采样 + 结构化聚合**；反从众前言；dissent 保留 | **删除多轮辩论**：最多一轮交叉质疑，且盲审；聚合用分歧保留式综合 | 借鉴思想 | MIT | `core/workflows/02`、`05`、`PRINCIPLES.md` |
| M7 | Deep Research / agentic search | 通用 agentic research 实践 | 迭代查询规划、按缺口补搜 | 搜索由**区分性预测**驱动而非主题覆盖；每轮预算硬上限；来源依赖必须入账 | 借鉴思想 | — | `workflows/04`、`06` |
| M8 | Hypothesis Generation / 科学推理 | Popper 式可证伪性；现代预注册实践 | 可检验预测；对手假说 | **预注册预测台账**（观察窗口 + 判定阈值 + 反向指标），搜索前锁定 | 借鉴思想 | — | `schemas/prediction`、`workflows/03` |
| M9 | Evidence Evaluation / 来源核验 | 情报来源评级传统；agent-studio SOURCE CHECK | 溯源、时效、利益相关、独立性 | **来源依赖图（SDG）**：按根来源计算有效独立信源数 | 借鉴思想 | MIT | `schemas/source`、`schemas/evidence` |
| M10 | Iterative Research | 自适应研究规划 | 每轮更新状态、找下一轮最值问题 | **信息价值停止规则** + 无进展检测 + 模型回溯修订触发器 | 借鉴思想 | — | `workflows/06` |
| M11 | 交互裁决 | IQTLabs snowglobe（narrator adjudicate） | 交互结果由中立裁决者按约束判定 | 裁决者只看「可行行动集合」与「约束」，不看主体自述的成功叙事 | 借鉴思想 | Apache-2.0 | `workflows/02` |
| M12 | 多阶心智理论 | RAND ROMANCER（multiple theories-of-mind） | 0/1/2 阶信念分层 | 只保留 0–2 阶；3 阶以上收益递减且不可核验，明确不建模 | 借鉴思想 | MIT | `schemas/actor` |
| M13 | 反从众工程纪律 | agent-studio hard-rules | 隔离、禁均值混合、基线对照、质量+覆盖双报、成本实报、审群体而非审个体 | 「面板 vs 基线」升级为 OIR 的 **Mode A 一等模式**；SOURCE CHECK 升级为持续记账 | 借鉴思想 | MIT | `core/PRINCIPLES.md`、`workflows/02`、`05` |
| M14 | 输出结构强制 | structured-analysis `Required output sections` / `Failure modes` | 用必填结构对抗敷衍 | 从「必填段落」升级为「**可校验 schema**」 | 借鉴思想 | MIT | `core/schemas/*` |

## 2. 为什么否定 ACH 的计算核心

这是 OIR 与「照抄情报分析法」最重要的分歧点，必须给出依据。

Heuer 的 ACH 要求：列出假说 → 列证据 → 逐格判定 consistent/inconsistent → 以「不一致证据最少」的假说胜出。这套**独立打分 + 排除法**在实验里表现不佳：

- **Mandel, Karvetski & Dhami (2018)**, *Judgment and Decision Making* 13(6)：受训并使用 ACH 的情报分析员，其判断**并不比**未使用任何方法对照组更准确，且一致性更差。同一研究里真正有效的是**重新校准 + 聚合**（MAE 下降 61%）。
- **Dhami, Belton & Mandel (2019)**, *Applied Cognitive Psychology* 33(6):1080–1090：ACH 训练者并未完整执行步骤；有混合证据表明它能减少确认偏误，但同时**增加判断不一致与错误**。
- **Chang, Berdini, Mandel & Tetlock (2018)**：在情报专业人员中未发现 ACH 降低确认偏误。
- **Karvetski, Mandel & Irwin**：当两个**完全相关**的证据来源变得显著时，使用 ACH 的受试者**更容易重复计算**（而非折减）第二份冗余证据。也就是说，ACH 在「多家媒体转载同一通讯社稿」这个场景上**加重**了错误。

对 OIR 的直接含义有三条，且互相独立：

1. **不要实现打分矩阵。** 它给使用者一种「已经算过了」的错觉，而实验显示它不改善准确度。OIR 保留 ACH 的**问题意识**（哪些证据真正能分开假说），丢弃它的**计算形式**。
2. **冗余折减必须显式做，而且要在最显眼处做。** 这是 ACH 的实测弱点，也恰好是 LLM 研究代理最容易犯的错。OIR 用 Source Dependency Graph 强制入账。
3. **真正提升判断的是重校准与聚合**（Mandel 2018）。因此 OIR 的不确定性表达不采用「模型自报 7/10 置信度」，而采用**分解式判断 + 显式聚合规则 + 校准提示**。

## 3. 为什么删除多轮辩论

2025–2026 年的系统评测对 MAD（multi-agent debate）给出了相当一致的负面结论：

- **Zhang et al. (2025)**, *Stop Overvaluing Multi-Agent Debate*（arXiv:2502.08788）：5 种 MAD 方法 × 9 个 benchmark × 4 个基座模型，MAD **经常打不过** Chain-of-Thought 或 Self-Consistency 这类**单 agent** 方法，而算力消耗高一个量级。
- **Yao et al. (2025)**, *Peacemaker or Troublemaker: How Sycophancy Shapes Multi-Agent Debate*（arXiv:2509.23055）：谄媚（sycophancy）是 MAD 的核心失效模式，agents 会在得出正确答案之前**塌缩为过早共识**，最终准确率低于单 agent 基线；并区分了 debater-driven 与 judge-driven 两类失效。
- **Choi et al. (2025)**, *When Identity Skews Debate: Anonymization for Bias-Reduced Multi-Agent Reasoning*（arXiv:2510.07517）：agents 会因**身份**而非论证质量采纳同伴观点；**去掉身份标记即可显著改善可靠性**。这是 OIR 采用「盲审」的直接依据，而且实现成本近乎为零。
- **Wu et al. (2025)**, *Can LLM Agents Really Debate?*（arXiv:2511.07784）：多数压力会压制独立纠错，少数派即使正确也被压过；调整辩论顺序、置信度可见性、团队规模的收益都有限，**决定性因素是单个模型的推理能力**。
- 理论侧：**Choi et al. (2025)** 的鞅（martingale）分析表明，在同质 agent + 无权重更新的条件下，辩论**保持**期望正确率不变——它不可能系统性地变好。

由此得到的 OIR 设计约束（不是偏好，是约束）：

| 约束 | 理由 |
|---|---|
| 独立分析在前，交叉质疑在后，且只有**一轮** | 多轮无增益，还放大从众 |
| 生成阶段**上下文隔离**，不得共享 transcript | 同 context 换人格是同质性最高的反模式 |
| 交叉质疑**去身份** | arXiv:2510.07517 的直接结论 |
| 综合**不得均值化**，必须保留分歧 | 均值化把方差抹平，等于只跑了一次 |
| 必须能跑**单 agent 基线**并如实对照 | arXiv:2502.08788 的方法论要求 |
| 多样性必须**被设计**，不能假设 | 同模型同提示 = 一个观点采样 N 次，付 N 倍价钱 |

## 4. 十二个已知失败模式 → 对应机制

这一节直接回应「必须探索的创新问题」。**每条机制都必须能回答：它解决什么、为什么这样实现、代价是什么。**

| # | 失败模式 | OIR 机制 | 为什么这样实现 | 代价 / 残留风险 |
|---|---|---|---|---|
| F1 | 多 agent 过早共识 | 上下文隔离 + 冻结后可见 + 反预判前言 + 盲审 | 从众的通道是「看到别人」和「知道那是谁」；把两条都切断最便宜 | 无法利用交互带来的即时纠错 |
| F2 | 观点高度重复 | 主体差异必须落在**利益结构**而非语气；输出重复度作为**诊断指标**报告 | 表面差异（不同措辞）不改变注意力分配 | 重复度只是代理指标，不能证明多样性充分 |
| F3 | 角色设定过简，处理不了派系 | 主体含 factions[]、决策规则、否决者 | 现实主体几乎从不统一；把国家当单一理性人是最大失真源 | schema 变重，填写成本上升 |
| F4 | 模拟建立在错误前提上 | 事实层与推断层**物理分离**；主体模型必须引用 `FACT-*`；引用不存在的事实即校验失败 | 只靠提示词要求「注意区分」不可靠，必须让错误无法写入 | 前提错误仍可能藏在被引用的「事实」里 |
| F5 | agent 只找支持自己的资料 | 取证任务由**假说对之间的区分性**排序，不由主张者提出 | 让提出者去找证据必然偏；把「找什么」的决策权从主张者手里拿走 | 需要 Director 做一次跨假说比较，增加一次调用 |
| F6 | 转载被当成多个独立来源 | Source Dependency Graph，按**根来源**计有效独立信源数 | 这是 ACH 实测会加重的错误（Karvetski et al.），必须显式对抗 | 依赖关系常不可见，只能记「疑似同源」并标不确定性 |
| F7 | 反方审查流于形式 | 盲审 + 每条反驳必须被**裁决**（接受/部分接受/驳回 + 理由） + 反驳必须锚定到具体实体 ID | 没有裁决，red team 输出就是一段可忽略的散文 | 裁决本身由 Director 做，仍可能被压制 |
| F8 | 新证据不回溯修正主体模型 | 修订触发器：预测被证伪 → 强制检查「是假说错还是主体模型错」；模型带 version 与 change_log | 只改假说不改模型，会让同一错误在下一轮复现 | 无法自动判定归属，需人/导演裁量 |
| F9 | 假说无法转化为可检验预测 | 假说**未附预测即视为不完整**（schema 必填）；预测必须含窗口、指标、反向指标、阈值 | 把「可检验」变成结构约束而不是道德劝告 | 部分重要假说确实只能给弱预测，需允许 `weak` 并标明 |
| F10 | 无限循环 | 五条停止规则 + 无进展检测 + 信息价值排序 | 停止必须可判定，不能靠感觉 | 价值排序是**序数启发式**，不得包装成概率 |
| F11 | 过度自信 | 分解式判断（证据强度/来源独立性/预测命中率分列）+ 显式聚合规则；禁止把打分说成概率 | Mandel 2018：真正有效的是重校准与聚合，不是自报信心 | 仍非严格校准，须在报告中声明 |
| F12 | 数量与成本失控 | 预算台账（runs / fetches / rounds）+ 硬上限 + 降级阶梯 | 成本随轮数超线性增长 | 降级会牺牲独立性，必须显式告知用户 |

## 5. 不采用清单（含理由）

| 方法/做法 | 不采用的理由 |
|---|---|
| ACH 打分矩阵 | 实验不支持，且在相关来源上加重重复计算（见 §2） |
| 多轮自由辩论 | 无系统性增益，放大谄媚与从众（见 §3） |
| 单一「置信度 0–100」总分 | 假的精确性；混装了证据强度、来源质量与逻辑严密性三种不可通约的东西 |
| 2x2 情景矩阵作为默认产出 | 轴的选择常由美学而非机制决定；OIR 只在机制真的二分时才用 |
| 3 阶以上心智理论 | 不可核验，且 LLM 在此深度上产出的是文采不是推理 |
| 「让 agent 投票决定研究规模」 | 规模是用户授权问题，不是 agent 决策问题 |
| 把整个仓库打包成一个 Skill | 与渐进披露原则冲突，会让每次调用都吃掉全部上下文 |
| 以 agent 数量作为卖点 | 数量不是能力；OIR 的对照基线明确包含「1 个 agent」 |

## 6. 署名与合规状态

| 来源 | 使用方式 | 许可证 | 义务 | 当前状态 |
|---|---|---|---|---|
| bushrabeg/structured-analysis | 借鉴思想（框架必填结构、透明声明） | MIT | 署名 | 已在 README/PROJECTS 署名 |
| nraford7/agent-studio | 借鉴思想（隔离、反从众、dissent 综合、source check、基线对照） | MIT | 署名 | 已署名；**未复制任何提示词原文** |
| IQTLabs/snowglobe | 借鉴思想（裁决者） | Apache-2.0 | 署名；若复用代码需 NOTICE | 仅思想，无代码复用 |
| RANDCorporation/ROMANCER | 借鉴思想（多阶心智理论） | MIT | 署名 | 仅思想 |
| Heuer / Heuer & Pherson SATs | 公共领域方法论 | — | 学术引用 | 已引用 |
| 各 arXiv 论文 | 学术引用 | — | 引用 | 已引用 |

> 待办（Phase 2）：若最终决定复用 agent-studio 的 `run_check.py` 逻辑，须在 `THIRD_PARTY_NOTICES.md` 登记，并在文件头保留原版权行。
