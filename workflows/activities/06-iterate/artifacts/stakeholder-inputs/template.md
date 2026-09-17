# Stakeholder Inputs — [Dashboard Name]

A record of every input the stakeholder supplied during the [YYYY-MM-DD] HELIX cycle
that produced [dashboard name], and what to prepare before running the next one.

**Totals**: [N] questions across [N] prompts, [N] gate approvals, [N] opening brief.
**Result**: [N] widgets, [N] pages, [N/N] verification checks passing [on first deploy /
after N re-prompts].

---

## 1. Opening brief (volunteered, not asked)

| Input | Value |
|---|---|
| Goal | [what the stakeholder asked for, in their words] |
| Environment | [workspace / profile / catalog] |
| Requirements document | [filename and version, or "none — blank slate"] |
| Source DDL | [filename, or how the schema was obtained] |

[Constraints that came from saved preferences or a prior cycle rather than this
conversation — name them here, or the next cycle will assume they were agreed in this
one.]

---

## 2. [Activity or round] — [N] questions

[One section per activity or round in which questions were asked: Setup/Step Zero,
Frame round 1, Frame round 2, Frame structure, Design, Test, Build, Deploy. Number
questions continuously across all sections.]

| # | Question | Options offered | Chosen |
|---|---|---|---|
| [n] | [the question as asked, including the conflict or ambiguity that forced it] | [option *(rec)* · option · option] | **[choice]** |

**Effect on the build**: [what changed as a result — W-### widgets added, replaced, or
retired, filters extended, a definition settled. "Nothing changed" is a valid and
useful answer.]

[Where a recommendation was overridden, say so and record the stakeholder's reasoning;
note whether it becomes a standing preference for future cycles.]

---

## [N]. Gate approvals — [N] free-text

| Gate | Response | What it released |
|---|---|---|
| [Frame] | `[verbatim response]` | [next activity] |

[Note any gate still open when this record was written.]

---

## [N]. What to prepare before the next cycle

[How many of the questions existed only because live data contradicted the supplied
documents — the round-tripping that is avoidable next time.]

**Profile the data before writing the requirements document.** [Each conflict that a
single query would have surfaced, and what it changed:]

- [Cardinality of every column intended as a filter or breakdown]
- [Distinct-value counts for any column named in a KPI]
- [Date coverage per fact table, at month grain]
- [Row counts against stated grain, and the actual double-counting test]

**Decide these in advance — they will be asked every time:**

1. [Numerator and denominator for every rate, stated explicitly]
2. [Which exact column backs each KPI, not just the business term]
3. [Top-N depth for ranked widgets]
4. [Filter coverage per page, including which widgets are deliberately exempt and why]
5. [Page structure and who owns each page]
6. [Theme, against the catalog in `workflows/resources/themes/README.md`]
7. [Target environment, warehouse, and whether deployment may write to the catalog]

**[Material named but not supplied]** — [what had to be recovered from elsewhere, and
which widgets depended on it.]

**Expect to be asked about anything the document leaves as an open question.** [How
many open questions the document carried and how each was closed — by evidence, by
decision, or deferred.]
