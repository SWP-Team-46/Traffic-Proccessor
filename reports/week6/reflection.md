## Reflection Artifact

### Learning points
- Learned to implement and wire up blacklist-based IP blocking end-to-end (Gate → CNSS), including verifying it against a real client instead of only the dummy target.
- Learned to maintain and display per-IP statistics with a time window, including the Top IPs view, as part of the dashboard/UI overhaul shipped in `v2.0.0`.
- Learned that separating architecture concerns (CNSS vs. TP) is more involved than expected: the Docker networking friction from the previous Sprint has grown into a dedicated PBI (PBI-11: Separate CNSS and TP) rather than a quick fix.

### Validated assumptions
- IP-based blocking is stable and demonstrable end-to-end: a client added to the blacklist no longer reaches CNSS.
- Per-IP statistics collection and the Top IPs dashboard work against real traffic, not just the dummy target.
- The existing Docker-based deployment (`docker compose up --build`) remains a workable basis for a Week 6 trial release, even though the CNSS/TP components are not yet split.

### Needs clarification
- Fine-tuning the scope of the CNSS/TP separation (PBI-11) so Week 7 focuses on the highest-value part of that split first.
- Confirming with the customer whether the graphical/statistics view (US-12) is a nice-to-have or a priority for their trial, so we can sequence Sprint 5 accordingly.
- Refining how we present the Gate ↔ CNSS architecture during the Week 6 customer meeting so the improvements are easy to follow.

### Planned response
- Carry the final polish on US-12 (Graphical representation) and PBI-11 (Separate CNSS and TP) into the start of Week 7, building directly on the solid `v2.0.0` foundation.
- Keep `docs/customer-handover.md` and the Assignment 6 documentation PR (#112) in sync with the current `v2.0.0` behavior so the trial experience matches the docs.
- Use the Week 6 customer meeting to validate the release with the customer and use their input to fine-tune Sprint 5 priorities.
