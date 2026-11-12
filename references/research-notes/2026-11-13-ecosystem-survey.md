# 2026-11-13 · 生态调研原始笔记

本文件是 `references/PROJECTS.md` 的原始记录：**我实际执行了什么、看到了什么、哪些没看到**。保留细节以便日后复核或推翻结论。

## 检索方式

- GitHub REST API（`/repos/{owner}/{repo}`、`/repos/.../git/trees/{sha}?recursive=1`）取元数据与文件树。
- `raw.githubusercontent.com` 直取文件正文。
- 环境注意：本机 `curl` 需 `--ssl-no-revoke`，否则 schannel 报 0x80092012；`/tmp` 不可用，临时文件写入项目内 `.workbuddy/tmp/`。
- arXiv 元数据经 `export.arxiv.org/api/query?id_list=` 核对标题与日期（用于防止引用张冠李戴）。

## 时间戳说明

所有 star 数、`pushed_at` 均为 **2026-11-13** 快照。开源项目排名会变，引用时应重新取。

## 逐项记录

### structured-analysis
```
LICENSE 1066 / README.md 5731 / SKILL.md 21686
```
无 scripts、无 references、无模板。全部逻辑在单个 SKILL.md 内。读完前 ~9 KB（八个框架的前五个）与结构骨架，后 12 KB 为框架 6–8 + 双语触发词典 + anti-pattern 列表，已确认无隐藏机制（无脚本、无状态文件）。

结论：**它的价值在提示工程纪律，不在系统**。21 KB 单文件能承载八个框架，说明「必填输出段 + 失败模式」是高压缩比的设计手段，值得直接学。

### agent-studio
84 个 tree 项。结构：
```
SKILL.md 10353
references/{hard-rules 13923, voice, evidence-gate 7474, field-evidence, full-lifecycle 12153,
            recipes, synthesis-modes 6727, persona-template 8613, roster 4139,
            work-sample, doit-handoff, diagnose-rubric, harden-checklist, job-description}
methodologies/{kernel.md 5062, overlays/{root-cause, scenario-planning, terrain-mapping}}
docs/research/{Persona-Construction-Research-Bible 38018, Persona-Ensembles-Research-Bible 83869,
               Perspective-Synthesis-Research-Bible 42706, ...}
scripts/{run_check.py, field_gate.py, coverage_report.py, exemplar_find.py, diversity.py, team_validate.py}
THIRD_PARTY_NOTICES.md 3183
```
这是本次调研中**工程质量最高**的一个：有脚本做机械校验（run manifest、lens 是否实质、覆盖率），有 field-evidence 日志做跨运行证据积累，有第三人称声明文件。

值得注意的是它自己的 `docs/simmer/` 里有 iteration-0 到 3 的候选版本与 `docs/review/2026-10-17-critical-review.md`——即**它对自己的设计做过迭代与批判**。这说明「多视角面板」这类东西确实需要多轮硬化，不能一次写对。

未读部分：`scripts/*.py` 全部、`docs/research/*`（约 180 KB）。若要复用其脚本，Phase 2 必须读。

### stress-test
110 个 skill 目录，平均 1.4–5.8 KB。命名密度示例：
`action-priority-matrix, adversarial-debate-truthseeking, adversarial-escalation, adversarial-persona,
assumption-cascade-tracer, assumption-negation, attack-vector-generation, boundary-enumeration,
boundary-probing, breakpoint-detection, causal-claim-extraction, causal-necessity-testing,
circular-validation-audit, claim-negation, claim-refinement, closest-worlds, confidence-calibration,
contradiction-derivation, contradiction-detection, counterexample-generation, critical-case-design,
cross-examination, debate-architect, debate-critic, debate-defender, debate-judge, deductive-chain, design-fmea ...`

**只读了 README 与目录，未读任何 skill 正文。** 因此只能判定为「方法名词清单」，不能声称了解其实现质量。若要引用其中某个具体动作，必须回到原文。

### snowglobe
```
config/{game.yaml, WoTRM.yaml, openai/llms.yaml, local/llms.yaml}
examples/{ac_game.py, ac_sim.py, haiwire.py}
examples/haiwire_files/{incidents.csv, injects.csv}
src/llm_snowglobe/{api.py, assets/...}
```
`injects.csv` + `incidents.csv` + narrator 的循环，是「事件注入 → 各方响应 → 裁决 → 下一回合」。这套循环对 OIR 的启发仅限**裁决环节**：OIR 不需要回合制剧情，但需要「谁的行动真的发生了」的中立判定。

### ROMANCER
README 确认：Python 实现，`multiple theories-of-mind`，AFGSC A5/8 委托，RAND Project AIR FORCE，引用 A2673-2（用户指南）与 A2673-3（理论与背景）。MIT。
未读实现，因此只借鉴「心智理论分层」这一概念，不引用其具体参数。

## 未完成 / 存疑

1. `alirezarezvani/deep-research` 返回 404 —— 原始候选清单此处已失效。**这提示原始清单整体需要重新核验**，不能假定其余条目准确（事实上 agent-studio 与 stress-test 的描述也与实际相符度需逐项比对，本文件只记录我核实过的）。
2. 未检索中文生态（知乎/公众号/Gitee）中的类似工作。
3. 未核验 Claude Code / Codex CLI / Gemini CLI 对 Agent Skills 的最新支持状态——留给 Phase 2 的 `packaging/PLATFORM_COMPATIBILITY.md`，必须附官方文档链接与验证日期。
4. OASIS 未读。
