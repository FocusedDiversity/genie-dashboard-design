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

The core skill runs a dashboard through the six **HELIX** activities, producing versioned artifacts in your working repo under `docs/helix/` and pausing at a stakeholder gate after each:

| # | Activity | Artifacts | Gate question |
|---|----------|-----------|---------------|
| 01 | **Frame** | dashboard-brief, widget-inventory (W-### ids) | Is this the right dashboard? |
| 02 | **Design** | theme selection, **HTML mockup** (browser-viewable, Databricks look & feel), design-decisions | Is this what it should look like? |
| 03 | **Test** | widget-test-plan — baseline SQL executed *before any prompt exists* | Do we know what correct means? |
| 04 | **Build** | prompt-catalog — one Genie prompt per widget, traceable to its test | Are the prompts written to spec? |
| 05 | **Deploy** | deployment-guide with recorded PASS/FAIL verification | Does the live dashboard pass? |
| 06 | **Iterate** | iteration-log — feedback, drift re-checks, next-cycle scope | Spiral again or close? |

Test-before-Build is the core discipline: Genie writes SQL nondeterministically, so deterministic baseline queries — written and run first — are the contract its output must match.

## Repository layout

```
.claude-plugin/
├── plugin.json          Plugin manifest
└── marketplace.json     Marketplace catalog (this repo is its own marketplace)
workflows/
├── resources/           Shared resources
│   └── themes/          Theme catalog (wanderbricks, clinical-slate, executive-minimal):
│                        <id>.json (palette authority) + seed.<id>.lvdash.json (themed starter)
└── activities/          HELIX artifact pack (format-compatible with the HELIX repo)
    ├── 01-frame/        GATE.yaml + dashboard-brief, widget-inventory
    ├── 02-design/       GATE.yaml + dashboard-mockup (HTML), design-decisions
    ├── 03-test/         GATE.yaml + widget-test-plan
    ├── 04-build/        GATE.yaml + prompt-catalog
    ├── 05-deploy/       GATE.yaml + deployment-guide
    └── 06-iterate/      GATE.yaml + iteration-log
skills/
└── genie-dashboard-design/
    ├── SKILL.md                          The six-activity workflow skill (orchestration map)
    ├── assets/design-template.md         Legacy ASCII wireframe template (superseded by the HTML mockup artifact)
    ├── assets/prompt-style-guide.md      Style authority for Build's Genie prompts
    └── references/genie-dashboard-prompts.md   Complete worked example (Tuva synthetic data)
```

Each artifact folder follows the HELIX four-file convention: `template.md` (structure), `prompt.md` (generation rules), `example.md` (quality bar), `meta.yml` (identity, output location, validation). The canonical mockup example is `workflows/activities/02-design/artifacts/dashboard-mockup/example-appointment-analytics.html` — open it in a browser. Design starts by picking one of three themes (see `workflows/resources/themes/README.md`); the mockup and the deployed dashboard are both built from that choice.

New skills go in `skills/<skill-name>/SKILL.md` and become available to all installers as `/genie-dashboard-design:<skill-name>` on their next plugin update.

## Versioning

`plugin.json` deliberately omits `version`, so the plugin tracks the latest commit — installers pick up changes automatically. Once the toolkit stabilizes, add an explicit `"version"` to control rollout.

## Key principles

1. **Clarity first** — every prompt carries exact table paths, join logic, and aggregation rules.
2. **No double-counting** — distinct IDs, max-per-claim, and grain are always explicit.
3. **Explicit metric definitions** — e.g., "Denial rate = (paid = 0 or null) / total claims".
4. **KPIs first, drill-downs second** — designed for executives glancing and analysts digging.



## Features to Be Added

1. **Ask User About Existing Requiremetnt Document Dpfront** — every session should start with asking the user if they have a pre-existing design document they would like to start from?
2. **Check for latest AI/BI Genie Features that may impact development process or final product.** — Newly released features that may impact dashboards need to be figured in.
3. **Check for Patterns on Existing Dashbaords** — New dashbaords being added to a set of existing dashbaords should check those existing to aim to math those design patterns first - then fall back to best practices if noe exist. A prompt of the user should confirm if existing dashbaords exist to try to match.
4. **Enhance Dashbaord Mode** — New Tabs being added to existing dashbaords.  A new mode to add a new tab to an existing dashbaord.  Match the existing, factor in new datasets, etc. and add to an existing just a new tab.