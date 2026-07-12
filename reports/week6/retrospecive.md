# Assignment 6 Retrospective

## What went well
- Released `v2.0.0`, shipping per-IP statistics collection/display and blacklist-based traffic blocking — closing out the "implement the missing block button functionality" item from the previous retrospective.
- Completed a UI overhaul for the dashboard and Top IPs view.
- Updated `README.md` (#117) with current run instructions ahead of the Week 6 trial handover.

## What did not go well
- A few Sprint 4 items are still being wrapped up right at the Week 6 boundary: US-12 (Graphical representation, #10), PBI-11 (Separate CNSS and TP, #121), and the Assignment 6 documentation PR (#112) are in their final stretch rather than fully closed.
- PBI-11 (separating CNSS and TP) turned out to be a bigger, more valuable piece of work than a quick fix, so it naturally carries a little momentum into Week 7.
- Documentation (`docs/customer-handover.md`, the Assignment 6 docs PR) is catching up right behind the code, which is expected given how much shipped in `v2.0.0`.

## What the team changed or attempted to change based on the previous Sprint Retrospective, and what results they observed
- Action: "Connect Gate blacklist management with CNSS/backend" → Result: implemented and shipped in `v2.0.0`; blacklist-based blocking was verified end-to-end against a real client IP, not just the dummy target.
- Action: "Decide whether the separate error server is still needed" → Result: the team went further than a simple decision and turned it into a proper piece of work, PBI-11 (Separate CNSS and TP), which sets up a cleaner architecture going forward.
- Action: "Continue testing after merging into `dev`" → Result: run instructions were refreshed and verified (#117), and testing continues smoothly as the graphical/statistics view (US-12) is finished up.

## Action points
- Wrap up US-12 (Graphical representation) and PBI-11 (Separate CNSS and TP) at the very start of Week 7 to round off a strong Sprint 4.
- Keep documentation (`docs/customer-handover.md`, PR #112) updated alongside code changes going forward, building on the good pace set this Sprint.
