# Research plan — RES-001

## Question
Why did Intel pause the Magdeburg fab in September 2024 and cancel it entirely in
July 2025, and what did each party's judgement rest on?

## Decision context
Test case for the A-vs-B comparison (see `tests/records/`). Nobody is deciding
anything on the basis of this run; it exists to compare two research modes on
identical inputs.

## Scope
- **as_of** 2026-10-31
- **In** Intel corporate decisions Sep 2024 – Jul 2025; German federal subsidy and
  budget politics; EU Chips Act aid framework
- **Out** US CHIPS Act award terms; Poland site economics; competitor capacity plans
  except as comparison

## Actor candidates (from facts)
| Candidate | Why a party | Fact |
|---|---|---|
| Intel executive leadership | Owns the pause/cancel decision | FACT-001, FACT-003 |
| German federal government (finance vs economy ministries) | Pledged EUR 9.9bn; internally split over reclaiming it | FACT-002, FACT-004 |
| Saxony-Anhalt / local authorities | Site, jobs, cleared land | FACT-002 |

Structural counterparty: EU Commission (aid approval) — included inside the German
party's constraints rather than as a separate seat, because it had no independent
action in the window.

## Scale
Standard, 3 actor seats. Evidence and red-team seats are **not** dispatched in this
case: Mode B is defined as actor simulation + synthesis only. That is a deliberate
feature of the comparison, not an omission.

## Budget
6 queries for the fact base (spent). Seats: 3 actor runs + 1 Mode A baseline run.

## Known gaps
- Der Spiegel / FAZ originals not retrieved, so FACT-004 is single-source.
- Intel 10-K/10-Q not consulted; figures come from aggregated reporting.
