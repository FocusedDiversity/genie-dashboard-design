# Genie Dashboard Design

A **Claude Code plugin** — and a portable **Agent Skill** (CoPilot) — with tools for automating **Databricks AI/BI dashboard design** and generating the **prompts for Genie** that build each widget.

The repo is its own plugin marketplace, so Claude Code users install it once and the skills work in every repo they open. For **GitHub Copilot** (which has no marketplace), the same skill folder drops into a repo's `.github/skills/` — see [Using this with GitHub Copilot](#using-this-with-github-copilot).

# Summary 

A HELIX based Claude plugin built around the idea that metric rules / design decisions, etc. should exist in writing and get tested before Genie is ever asked to compute or build. This solution takes a user through a guided process of establishing requirements, design, user personas, etc. and then builds the data layer logic and tests and ultimately the dashboard (via genie prompts or Databricks CLI from VS code or an IDE).

The Process begins by asking the user how they would like to start the process:
1. As a 'blank slate' and the user is interviewed / asked clarification questions after initial prompt to build out the requirements / design, etc.
2. A User brings a formal requirements document to the session and uploads it, this is used to inform many of the decisions, design etc.
3. A User brings a formal requirements document and a wireframe / mockup to the session and uploads them, these are used to inform many of the decisions, design etc.
4. A user has an existing Tableau Dashboard file (.twb / .twbx) they would like to convert to a databricks dashboard. This file is used to deduce many aspects of the dashboard design.

Six activities, one spiral
The workflow runs a dashboard through six HELIX activities: Frame, Design, Test, Build, Deploy, Iterate. Each one writes versioned artifacts to docs/helix/ in the calling repo and ends at a gate the stakeholder has to explicitly approve before the next activity starts. It is a Claude Code plugin, installed once and invoked in any repo with a one-line prompt describing the dashboard, and every artifact it produces is a plain file under version control.

A single identifier runs through the whole spiral. The Frame stage assigns every widget a stable W-### id. The Design stage mockup tags each widget with that same id. Test writes a T-### check that verifies it. The Build stage writes the Genie prompt for it. The Deploy stage records that widget’s PASS or FAIL. Nothing enters the pipeline without a W-###, and nothing ships without a T-### that traces back to one, in either direction.


## Installation (one time, per person)

In any Claude Code session:

```
/plugin marketplace add FocusedDiversity/genie-dashboard-design
/plugin install genie-dashboard-design@focused-diversity
```

The repo is public — no credentials or special access required.

Then, in any repo, invoke the skill:

```
/genie-dashboard-design:genie-dashboard-design Members & claims dashboard for healthcare analytics
```

## Prerequisites

The workflow drives the Databricks CLI and runs real queries, so it expects:

| Requirement | Needed for | Notes |
|---|---|---|
| **Databricks workspace** | All activities | The dashboard is built and deployed here |
| **Databricks CLI with a configured profile** | Test, Deploy | `databricks auth login` — the workflow always asks which profile to use and never auto-selects one |
| **A SQL warehouse** | Test, Deploy | Test executes baseline queries against it before any Genie prompt is written |
| **Unity Catalog tables** to build against | Frame onward | Frame verifies every named table exists before writing the brief |
| **Python 3** | Tableau conversion only | `list_workbook_structure.py` uses only the standard library |
| **`tableauhyperapi`** | Tableau conversion only | `pip install tableauhyperapi` — needed solely to read a `.twbx`'s packaged `.hyper` extract |

The first four are required for a full cycle. The last two matter only if you start from an
existing Tableau workbook (Step Zero option 4).

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

## Using this with GitHub Copilot

Copilot has no plugin marketplace — `/plugin marketplace add` is a Claude Code command and will
fail in Copilot, even when Copilot is running Claude models. But Copilot supports **Agent Skills**
using the same `SKILL.md` format, so the skill itself ports directly. VS Code scans
`.github/skills/`, `.claude/skills/`, and `.agents/skills/` in a workspace.

Everyone starts by cloning this repo locally — it is only the source to install *from*, and never
needs to be pushed anywhere:

```bash
git clone https://github.com/FocusedDiversity/genie-dashboard-design
cd genie-dashboard-design
```

Then pick one of two install modes.

### Option A — Personal install (no repo permissions needed)

Installs to your user profile. The skill works in **every** repo you open, and nothing is added to
any project's git history — useful when you can't (or would rather not) commit to the team repo.

```bash
scripts/install-skill.sh --personal          # macOS / Linux / Git Bash
```
```powershell
.\scripts\install-skill.ps1 -Personal        # Windows PowerShell
```

Each person runs this once on their own machine. To update later, `git pull` this repo and re-run.

### Option B — Vendor into the team repo (everyone gets it on clone)

Installs into one repository and is committed there, so teammates need no setup at all — they just
pull. Requires commit access to that repo.

```bash
scripts/install-skill.sh /path/to/your-repo
```
```powershell
.\scripts\install-skill.ps1 C:\path\to\your-repo
```

Then commit it:

```bash
cd /path/to/your-repo
git add .github/skills/genie-dashboard-design
git commit -m "Add genie-dashboard-design skill"
```

**Serving both tools from one copy**: `.claude/skills/` is read by Copilot *and* Claude Code, so
installing there covers a mixed team with a single directory — add `--dir .claude/skills`
(or `-Dir .claude\skills`) to either command.

### Using it

In VS Code, open Copilot Chat in agent mode and either describe what you want ("build a members and
claims dashboard") — Copilot loads the skill by matching its description — or type `/` and pick
`genie-dashboard-design` explicitly. Artifacts are written to `docs/helix/` in whatever repo you
have open.

Agent Skills arrived in VS Code around version 1.108 — if the skill isn't picked up, check your VS
Code version and that agent mode is enabled.

## What the skill does

The core skill runs a dashboard through the six **HELIX** activities, producing versioned artifacts in your working repo under `docs/helix/` and pausing at a stakeholder gate after each:

| # | Activity | Artifacts | Gate question |
|---|----------|-----------|---------------|
| 01 | **Frame** | dashboard-brief, widget-inventory (W-### ids) | Is this the right dashboard? |
| 02 | **Design** | theme selection, **HTML mockup** (browser-viewable, Databricks look & feel), design-decisions | Is this what it should look like? |
| 03 | **Test** | widget-test-plan — baseline SQL executed *before any prompt exists* | Do we know what correct means? |
| 04 | **Build** | prompt-catalog — one Genie prompt per widget, traceable to its test | Are the prompts written to spec? |
| 05 | **Deploy** | deployment-guide with recorded PASS/FAIL verification | Does the live dashboard pass? |
| 06 | **Iterate** | iteration-log — feedback, drift re-checks, next-cycle scope; **stakeholder-inputs** — every question asked this cycle and what it changed | Spiral again or close? |

Test-before-Build is the core discipline: Genie writes SQL nondeterministically, so deterministic baseline queries — written and run first — are the contract its output must match.

### Starting from existing docs (or not)

Frame doesn't start with a blank page. Before the stakeholder interview, the workflow asks whether existing requirements or design material exists to start from — a data dictionary, PRD, mockups, wireframes, a style/brand doc, or an existing **Tableau workbook** (`.twb`/`.twbx`) — supplied as files, pasted text, or links. Whatever's supplied is logged in the brief's **Source Documents** table and reused as artifacts are produced, not just read once:

- **Frame** extracts purpose, audience, and success criteria from a PRD/brief, and field names/definitions/grain from a data dictionary — still verified against the live tables, not taken on faith. A supplied Tableau workbook (`.twb` or `.twbx`) is unpacked and its XML mined the same way (see `skills/genie-dashboard-design/assets/tableau-intake.md`): worksheets and dashboard layout, fields with their aggregations already decided, data source connections, and calculated fields (flagged, not ported as SQL). If the `.twbx` packages its own `.hyper` extract, its real schema/grain is read directly via a bundled script rather than trusted from the XML alone.
- **Design** reconciles a supplied style/brand doc or mockup against the theme catalog, recording a match, an override, or a gap rather than silently picking a catalog theme's color palette. A supplied mockup/wireframe (or a Tableau workbook's dashboard zones) seeds the HTML mockup's layout (tab structure, widget placement); chrome — colors, fonts, corner-radius — still comes from the selected catalog theme.
- **Test** treats a Tableau custom-SQL data source or calculated field as a draft only — its baseline still gets run and verified, never accepted on Tableau's authority.
- **Build** reuses a data dictionary's (or a Tableau workbook's) field names and metric definitions verbatim in the Genie prompts instead of paraphrasing them.
- Sources that conflict — with each other, with live data, or with the stakeholder's answers — are flagged `[NEEDS CLARIFICATION]` for the stakeholder rather than silently resolved.

If nothing is supplied, "None provided" is recorded and every artifact is built from scratch: Frame runs the full stakeholder interview, and Design's theme (color palette, typography, layout) is chosen from the catalog — `wanderbricks`, `clinical-slate`, `executive-minimal` — on fit to the brief alone.

The `01-frame` and `02-design` `GATE.yaml` files enforce this: their entry/exit requirements block until the stakeholder has actually been asked, any supplied docs are retained in the stage's artifact directory, and — when source docs exist — until that reuse is demonstrated in the artifacts rather than assumed.

## Repository layout

```
.claude-plugin/
├── plugin.json          Plugin manifest
└── marketplace.json     Marketplace catalog (this repo is its own marketplace)
scripts/
└── install-skill.sh     Vendors the skill into another repo (Copilot / team sharing)
skills/
└── genie-dashboard-design/   ← self-contained: this entire folder IS the skill
    ├── SKILL.md                          The six-activity workflow skill (orchestration map)
    ├── assets/design-template.md         Legacy ASCII wireframe template (superseded by the HTML mockup artifact)
    ├── assets/prompt-style-guide.md      Style authority for Build's Genie prompts
    ├── assets/tableau-intake.md          Mining guide for a supplied Tableau workbook (.twb/.twbx)
    ├── assets/list_workbook_structure.py Parses a .twb/.twbx's dashboards, worksheets, and calculated fields
    ├── assets/read_hyper_schema.py       Reads a packaged .hyper extract's real schema/grain (needs tableauhyperapi)
    ├── references/genie-dashboard-prompts.md   Complete worked example (Tuva synthetic data)
    └── workflows/
        ├── resources/           Shared resources
        │   └── themes/          Theme catalog (wanderbricks, clinical-slate, executive-minimal):
        │                        <id>.json (palette authority) + seed.<id>.lvdash.json (themed starter)
        └── activities/          HELIX artifact pack (format-compatible with the HELIX repo)
            ├── 01-frame/        GATE.yaml + dashboard-brief, widget-inventory
            ├── 02-design/       GATE.yaml + dashboard-mockup (HTML), design-decisions
            ├── 03-test/         GATE.yaml + widget-test-plan
            ├── 04-build/        GATE.yaml + prompt-catalog
            ├── 05-deploy/       GATE.yaml + deployment-guide
            └── 06-iterate/      GATE.yaml + iteration-log, stakeholder-inputs
```

Everything the skill needs lives under `skills/genie-dashboard-design/`, and every path inside it
(`workflows/…`, `assets/…`, `references/…`) resolves relative to that folder. That is what lets the
same directory be copied into another repo and work unchanged — see [Using this with GitHub
Copilot](#using-this-with-github-copilot).

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

1. **Check for Patterns on Existing Dashboards** — New dashboards being added to a set of existing dashboards should check those existing to aim to math those design patterns first - then fall back to best practices if none exist. A prompt of the user should confirm if existing dashboards exist to try to match.
2. **Enhance Dashboard Mode** — New Tabs being added to existing dashboards.  A new mode to add a new tab to an existing dashboard.  Match the existing, factor in new datasets, etc. and add to an existing just a new tab.

## License

Licensed under the Apache License, Version 2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE).

Copyright 2026 Synaptiq.

All example data in this repository is synthetic. The healthcare examples use the
[Tuva Project](https://thetuvaproject.com/) open-source data model; person-level values in the
mockups (names, MRNs, dates of birth) are fabricated for illustration and correspond to no real
individual.
