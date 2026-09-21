# Skill: Spec — Propose

Turn an idea into a concrete change folder under `specs/changes/<change-id>/` containing
`proposal.md` and spec deltas (`specs/<capability>/spec.md`).

## When to use

First required step of the SDD loop. Input: user request or `idea.md`.

## Procedure

1. **Pick `<change-id>`:** Verb-led, lowercase hyphenated (e.g. `add-student-endpoint`).
2. **Identify affected capabilities:** Look in `specs/specs/` or identify a new capability name.
3. **Write `proposal.md`:** Using `.ai/templates/proposal.template.md`. Detail Why, What Changes, Capabilities affected, and Impact.
4. **Write spec deltas:** In `specs/changes/<change-id>/specs/<capability>/spec.md` using `.ai/templates/delta.template.md` (`## ADDED / MODIFIED / REMOVED Requirements`).
5. **Next step:** `/spec-design` (if technical choices are involved) or `/spec-tasks`.
