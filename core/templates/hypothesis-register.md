# Hypothesis register — {{RES-ID}} round {{NN}}

> Frozen prediction set: {{PRD ids}} at {{timestamp}}. Any prediction added later is
> marked `late` and excluded from the hit rate.

## Summary

| ID | Statement (short) | Origin | Status | Band | Predictions |
|---|---|---|---|---|---|
| {{HYP-001}} | {{...}} | {{actor-model}} | {{live}} | {{moderate}} | {{2 confirmed / 1 pending}} |
| {{HYP-002}} | {{...}} | {{interaction}} | {{weakened}} | {{weak}} | {{0/2, untested}} |

## {{HYP-001}} — {{statement}}

**Mechanism** (link by link; name the link that would break first)

1. {{...}}
2. {{...}}
3. **Weakest link:** {{...}}

**Scope:** {{where}} · {{when}} · excludes {{...}}

**Premises:** {{FACT-00x, CLM-00x}}
**Assumptions:** {{ASM-00x}}

**Relation to others**

| Other | Relation | Consequence |
|---|---|---|
| {{HYP-002}} | {{contradicts}} | {{separable by PRD-003}} |
| {{HYP-003}} | {{overlaps}} | {{both may hold; not worth a discriminating test}} |

**Predictions**

| ID | Observable | Window | Confirm if | Disconfirm if | Counter-indicator | Separates | Strength |
|---|---|---|---|---|---|---|---|
| {{PRD-001}} | {{...}} | {{from–to}} | {{...}} | {{...}} | {{...}} | {{001 vs 002}} | {{strong}} |

**Evidence balance**

| Supports | Undermines |
|---|---|
| {{EVD-004 (strong, 2 independent)}} | {{EVD-009 (moderate, 1)}} |

**Survived in review:** {{A1 steelman, A4 independence audit}} — a surface never attacked is untested, not clean.

---

## Draft hypotheses (excluded from synthesis)

| ID | Why draft |
|---|---|
| {{HYP-004}} | {{no mechanism: cannot name the causal link}} |

## Excluded this round

| ID | Reason | DEC |
|---|---|---|
| {{HYP-005}} | {{load-bearing link falsified by EVD-011}} | {{DEC-006}} |
