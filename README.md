# Genie Dashboard Design

A **Claude Code plugin** with skills and tools for automating **Databricks AI/BI dashboard design** and generating the **prompts for Genie** that build each widget.

The repo is its own plugin marketplace — install it once and the skills work in every repo you open.

## Installation (one time, per person)

In any Claude Code session:

```
/plugin marketplace add FocusedDiversity/genie-dashboard-design
/plugin install genie-dashboard-design@focused-diversity
```

The repo is private, so you need GitHub credentials configured (`gh auth status` should succeed, or a working SSH key with access to FocusedDiversity).

Then, in any repo, invoke the skill:

```
/genie-dashboard-design:genie-dashboard-design Members & claims dashboard for healthcare analytics
```

## Recommending the plugin from a working repo

To have Claude Code prompt teammates to install this plugin automatically when they open one of your team's repos, commit this to that repo's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "focused-diversity": {
      "source": { "source": "github", "repo": "FocusedDiversity/genie-dashboard-design" }
    }
  },
  "enabledPlugins": {
    "genie-dashboard-design@focused-diversity": true
  }
}
```

## What the skill does

The core skill walks a dashboard from idea to deployable Genie prompts through three approval gates:

| Gate | Deliverable |
|------|-------------|
| **1. Plan** | Context analysis and dashboard architecture (pages, sections, layout, filters) |
| **2. Design Review** | Wireframe/mockup, design rationale, global filter flow |
| **3. Build Prompts** | Databricks AI/BI Genie prompts and setup instructions, ready to deploy |

It gathers context (audience, data sources, KPIs, filters), proposes an architecture, iterates on a wireframe with you, and then emits a prompt catalog you paste widget-by-widget into a Databricks AI/BI dashboard.

## Repository layout

```
.claude-plugin/
├── plugin.json          Plugin manifest
└── marketplace.json     Marketplace catalog (this repo is its own marketplace)
skills/
└── genie-dashboard-design/
    ├── SKILL.md                          The three-gate workflow skill
    ├── assets/design-template.md         Gate 2 design checklist & wireframe template
    ├── assets/prompt-style-guide.md      Gate 3 style guide for unambiguous Genie prompts
    └── references/genie-dashboard-prompts.md   Complete worked example (Tuva synthetic data)
```

New skills go in `skills/<skill-name>/SKILL.md` and become available to all installers as `/genie-dashboard-design:<skill-name>` on their next plugin update.

## Versioning

`plugin.json` deliberately omits `version`, so the plugin tracks the latest commit — installers pick up changes automatically. Once the toolkit stabilizes, add an explicit `"version"` to control rollout.

## Key principles

1. **Clarity first** — every prompt carries exact table paths, join logic, and aggregation rules.
2. **No double-counting** — distinct IDs, max-per-claim, and grain are always explicit.
3. **Explicit metric definitions** — e.g., "Denial rate = (paid = 0 or null) / total claims".
4. **KPIs first, drill-downs second** — designed for executives glancing and analysts digging.
