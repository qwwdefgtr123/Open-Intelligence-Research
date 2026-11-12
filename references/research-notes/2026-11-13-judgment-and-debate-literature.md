# 2026-11-13 · 判断与辩论文献笔记

记录 OIR 设计所依赖的实证依据。**这些文献的作用是限制设计，不是给设计背书。**

## A. ACH 的实测表现

| 文献 | 结论 | 对 OIR 的约束 |
|---|---|---|
| Mandel, Karvetski & Dhami (2018), *Boosting intelligence analysts' judgment accuracy: What works, what fails?*, JDM 13(6), doi:10.1017/S1930297500006628 | 受训用 ACH 的分析员在概率判断任务上**略差于**未用任何方法的对照组；ACH 组在「评估信息有用性」上更好。**重新校准 + 聚合使 MAE 下降 61%** | 不要做打分矩阵；要做分解判断 + 聚合 |
| Dhami, Belton & Mandel (2019), *The ACH in Intelligence Analysis*, Applied Cognitive Psychology 33(6):1080–1090 | ACH 训练者未完整执行步骤；混合证据显示可减少部分确认偏误，但**增加判断不一致与错误** | 不要假定「用了结构化方法 = 更严谨」 |
| Chang, Berdini, Mandel & Tetlock (2018) | 情报专业人员中 ACH 未降低确认偏误 | 同上 |
| Karvetski, Mandel & Irwin（经 Mandel 综述转述） | 当两个**完全相关**的证据来源显著时，ACH 使用者**更容易重复计算**第二份冗余证据 | 冗余折减必须在最显眼处强制；这是 ACH 的加重项，不是中性项 |
| Mandel（*Intelligence, Science and the Ignorance Hypothesis*，OSF 预印） | ACH 逐格独立评估证据，抑制了对**构型性事实模式**（configural patterns）的推理；其信息整合规则源自对 Popper 证伪主义的误用（情报假说不是「所有天鹅皆白」式全称命题） | 不要按格子判 consistency；要看证据组合形态 |

**综合判断**：ACH 值得继承的是「先列全对手假说，再问哪些证据能分开它们」这个**提问方式**；不值得继承的是它的**计分与排除程序**。这是 OIR 与「照搬情报分析法」的分野。

## B. 多智能体辩论（MAD）

| 文献 | 结论 |
|---|---|
| Zhang et al. (2025), arXiv:2502.08788, *Stop Overvaluing Multi-Agent Debate* | 5 种 MAD × 9 benchmark × 4 模型；MAD 常**不如** CoT / Self-Consistency，成本高一个量级；批评评测实践（benchmark 覆盖窄、基线弱、设置不一致） |
| Yao et al. (2025), arXiv:2509.23055, *Peacemaker or Troublemaker* | 谄媚是核心失效模式；**过早共识**；最终准确率低于单 agent 基线；区分 debater-driven / judge-driven 失效 |
| Choi et al. (2025), arXiv:2510.07517, *When Identity Skews Debate* | 身份驱动的谄媚与自我偏置主导；**去身份化**几乎消除该效应 |
| Wu et al. (2025), arXiv:2511.07784, *Can LLM Agents Really Debate?* | 多数压力压制独立纠错；辩论顺序/置信度可见性/团队规模收益有限；决定性因素是个体推理能力 |
| Choi et al. (2025) 鞅分析（经 arXiv:2601.19921 转述） | 同质 agent + 无权重更新下，辩论对期望正确率是鞅 → 不能系统性改善 |
| Padmakumar & He (2024)、Kirk et al. (2024)（转述） | 后训练与对齐导致**多样性塌缩** |
| MALLM, Becker et al. (2025)（转述） | 144 种辩论布局的可组合实验框架；说明布局空间大但收益不确定 |

**综合判断**：收益主要来自**独立采样（ensembling）**，不是辩论轮次；多样性的来源必须被工程化（不同模型 / 不同信息 / 不同目标），否则 N 个 agent 只是同一个观点采样 N 次。→ OIR 的隔离 + 盲审 + 单轮 + 分歧保留综合，是这组结论的直接落地。

## C. 对「多视角」价值的正面依据（避免只引负面文献）

- **Tetlock / Good Judgment Project** 一脉：聚合多个**真正独立**的判断者能显著提升准确性；但前提是独立性，且个体需有反馈校准机会。
- **Mandel et al. 2018**：聚合本身是最稳健的提升手段（与 ACH 失败形成对照）。
- **structured-analysis / agent-studio** 的实践观察：强制输出结构能显著改变产出深度（非受控观察，不能当证据用，仅作工程参考）。

含义：OIR 应该把资源投入到**独立性**与**聚合规则**，而不是投入到「让 agent 多聊几轮」。

## D. 尚未核实 / 需要谨慎的地方

1. 上述 MAD 文献多为英文 benchmark 上的结果，**未在「政治/地缘分析」这类开放判断任务上验证**。把它们外推到 OIR 的场景是**合理但未证实**的推断，必须在文档中如实标注。
2. 部分文献信息来自综述与二手转述（标注为「转述」）。Phase 2 若要写进 README 的「参考」列表，需回到原文核对卷期页码。
3. arXiv 编号 2601.19921、2511.07784 的完整作者与发表状态未逐一核对。
4. 没有找到「多 agent 主体模拟 vs 单 agent 深度研究」在**真实情报问题**上的对照实验。**这正是 OIR 想补的空白，也意味着 OIR 自己必须做对照测试，否则无权声称更优。**
