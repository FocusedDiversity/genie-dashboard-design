# Generating a Genie Prompt Catalog

Write `dashboards/<slug>/docs/helix/04-build/prompt-catalog.md` from
`template.md`. Inputs: the approved inventory, design-decisions, and the
executed widget-test-plan. The style authority is `assets/prompt-style-guide.md`.

## Process

1. One prompt per W-###, in inventory order, titled exactly as the inventory.
2. Copy dedupe/null/grain language from design-decisions into each governed
   prompt verbatim — do not paraphrase; paraphrase is where Genie drift starts.
3. Tag each prompt with the T-### that verifies it.
4. Define datasets, including extra same-SQL datasets where filter scoping
   requires independent filter widgets (document the reason).
5. Pre-write fallback views for widgets whose checks involve window functions
   or multi-step baselines — these are the widgets Genie most often gets
   wrong, and Deploy needs the fallback ready, not improvised.

## Rules (from the style guide — the gate checks these)

- Full three-part table paths in every prompt; exact column names.
- Aggregation named: "count of distinct claim_id", never "count of claims".
- Explicit join logic, null handling, and formatting (currency, percent,
  decimal places, sort order).
- No prompt invents a metric definition — definitions are Frame/Design
  authority; a prompt that needs a new rule sends you back a gate.
- If Frame's Source Documents table lists a data dictionary, its field names
  and definitions outrank paraphrase, same as design-decisions language — copy
  them verbatim rather than restating in your own words.
- Same for a supplied Tableau workbook: reuse its worksheet field captions and
  titles for widget titles/metric names where they match the approved
  inventory. Never reuse a Tableau calculated field's formula as prompt
  logic — its baseline in widget-test-plan is the authority; the prompt states
  what Test already verified, not what Tableau's formula said.

## Restyle cycles

If the brief's Source Documents table lists a Lakeview dashboard export, no
new prompts exist — see `assets/restyle-cycle.md`. The catalog documents the
dashboard as built rather than proposing anything new:

- Reverse-engineer one entry per W-### from that widget's dataset query and
  field list (run `list_dashboard_structure.py --sql` for the query text), and
  mark each one `unchanged (restyle)`.
- Reuse the live widget's title verbatim. A restyle renames nothing, so a
  title that differs from the inventory is a mining error to fix, not a
  rewrite to make.
- Record the target `uiSettings.theme` block — the exact JSON to apply, taken
  from `workflows/resources/themes/<id>.json`. In a restyle that block is the
  build output, and Deploy applies it verbatim.
- A widget whose logic you cannot reconstruct from the file gets an entry
  saying so. The "no widget skipped" rule holds here exactly as in a new
  build; an unreconstructable widget is a gate conversation, not an omission.
