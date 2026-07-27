# Generating a Genie Prompt Catalog

Write `docs/helix/04-build/prompt-catalog.md` from `template.md`. Inputs: the
approved inventory, design-decisions, and the executed widget-test-plan. The
style authority is `skills/genie-dashboard-design/assets/prompt-style-guide.md`.

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
