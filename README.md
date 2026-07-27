# Genie Dashboard Design

Code, skills, and tools for automating **Databricks AI/BI dashboard design** and generating the **prompts for Genie** that build each widget.

The core of the repo is a [Claude Code skill](SKILL.md) that walks a dashboard from idea to deployable Genie prompts through three approval gates:

| Gate | Deliverable |
|------|-------------|
| **1. Plan** | Context analysis and dashboard architecture (pages, sections, layout, filters) |
| **2. Design Review** | Wireframe/mockup, design rationale, global filter flow |
| **3. Build Prompts** | Databricks AI/BI Genie prompts and setup instructions, ready to deploy |

## Repository layout

- [SKILL.md](SKILL.md) — the three-gate workflow skill (`/genie-dashboard-design`)
- [assets/design-template.md](assets/design-template.md) — Gate 2 design checklist and ASCII wireframe template
- [assets/prompt-style-guide.md](assets/prompt-style-guide.md) — Gate 3 style guide for writing unambiguous Genie prompts
- [references/genie-dashboard-prompts.md](references/genie-dashboard-prompts.md) — a complete example: a three-page healthcare analytics dashboard (Members, Claims & Charges, Clinical Conditions) built on the Tuva Input Layer synthetic dataset

## Using the skill in Claude Code

Clone this repo into your Claude Code skills directory (or symlink it), then invoke it:

```
/genie-dashboard-design Members & claims dashboard for healthcare analytics
```

The skill gathers context (audience, data sources, KPIs, filters), proposes an architecture, iterates on a wireframe with you, and then emits a prompt catalog you paste widget-by-widget into a Databricks AI/BI dashboard.

## Key principles

1. **Clarity first** — every prompt carries exact table paths, join logic, and aggregation rules.
2. **No double-counting** — distinct IDs, max-per-claim, and grain are always explicit.
3. **Explicit metric definitions** — e.g., "Denial rate = (paid = 0 or null) / total claims".
4. **KPIs first, drill-downs second** — designed for executives glancing and analysts digging.
