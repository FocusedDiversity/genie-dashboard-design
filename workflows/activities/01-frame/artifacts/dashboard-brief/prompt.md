# Generating a Dashboard Brief

Interview the stakeholder, then write `docs/helix/01-frame/dashboard-brief.md`
from `template.md`.

## Step Zero: Existing Requirements Intake

Before interviewing, ask the stakeholder: *"Do you have any existing
requirements documentation you'd like to start from — a data dictionary,
PRD, design mockups, wireframes, or other design docs? You can point me to
one or several — local file paths, pasted text, or links (Google Drive,
Notion, Confluence, SharePoint, etc.)."*

There is no upload widget in this environment, so be explicit about how to
hand docs over, and accept any number of them (zero, one, or many) — don't
assume a single file:

- **Local file paths** (repo or elsewhere on disk, including screenshots or
  exported images of a mockup) → read each with the file Read tool, which
  handles images as well as text.
- **Pasted text/markdown** → treat the pasted content itself as the doc.
- **Links** → fetch with WebFetch, or with the matching connector if one is
  authorized for this session (Google Drive, Notion, etc.); if a link can't be
  fetched, ask the stakeholder to paste the content or export it to a file
  instead of silently skipping it.

If any are supplied (however many, in whatever mix of forms):

- Read every one in full before writing anything.
- Extract what each one answers: PRDs/briefs → purpose, audience, success
  criteria; data dictionaries → field names, definitions, grain, known
  data-quality notes; mockups/wireframes/design docs → layout, tabs, widget
  types, visual style cues, filters.
- Use the interview below to fill what the docs leave open, and to *verify*
  what they claim rather than take it on faith — a data dictionary's stated
  grain still gets confirmed with DESCRIBE/LIMIT 1; a PRD's KPI still gets its
  numerator/denominator pinned with the stakeholder if the doc is ambiguous.
- Record every source doc in the brief's Source Documents table: name/location,
  type, and what was drawn from it. A claim traced to neither a doc nor an
  interview answer is a gap, not an assumption.
- If source docs conflict — with each other, with live data, or with the
  stakeholder's interview answers — don't silently pick one. Mark it
  `[NEEDS CLARIFICATION: <what conflicts and with what>]` and resolve with the
  stakeholder before the brief is finalized; the Frame exit gate already
  blocks on unresolved markers.

If no: proceed to Gather as normal and record "None provided" in Source
Documents.

This intake is not a one-time read — content from these docs should keep
surfacing downstream: widget-inventory mines any supplied mockup for candidate
widgets and layout, design-decisions reconciles any supplied style guide
against the theme catalog, and prompt-catalog reuses a data dictionary's exact
field names/definitions verbatim.

## Gather (ask, don't assume)

Skip questions a source document already answers — confirm them instead of
re-asking.

1. **Purpose**: what business problem, what decision does it enable
2. **Audience**: roles, frequency, glance vs. dig usage
3. **Data sources**: full `catalog.schema.table` paths, join keys, refresh cadence
4. **KPIs**: the metrics that matter, targets if any
5. **Filters**: what users slice by, sensible defaults
6. **References**: existing dashboards to match or replace, style constraints

## Verify before writing

- Confirm each named table exists (DESCRIBE or a LIMIT 1 query) and note its grain.
- For each rate/percentage metric, pin down numerator and denominator with the
  stakeholder — do not accept "% denied" without the rule for the denominator.
- For each source table, identify the double-counting risk (claim lines vs claims,
  reruns, multiple grains) and record the prevention rule.

## Rules

- State WHAT is measured, never HOW Genie will be prompted — prompt wording is
  the prompt-catalog's authority in Build.
- Unknowns get `[NEEDS CLARIFICATION: question]` inline. The Frame exit gate
  blocks while any marker remains.
- Metric definitions must be executable by a stranger: "distinct person_id per
  payer_type", not "member count".
