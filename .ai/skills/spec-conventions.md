# Skill: Spec — Conventions

The OpenSpec format and folder model used by this repo. **Reference skill** — read it when
writing or validating any spec, delta, proposal, or change. The lifecycle skills
(`spec-propose`, `spec-design`, `spec-tasks`, `spec-implement`, `spec-archive`) all assume it.

## When to use

Before writing a living spec, a change proposal, or a spec delta — and whenever you need to
validate that an artifact is well-formed.

## Folder model (root is `specs/`)

```
specs/
  project.md                       # stable project context (read first)
  specs/                           # LIVING TRUTH — what IS built
    <capability>/spec.md           # one folder per capability
  changes/                         # PROPOSALS — like DB migrations
    <change-id>/
      proposal.md                  # Why / What Changes / Impact
      design.md                    # technical decisions (optional)
      tasks.md                     # ordered, test-first tasks
      specs/<capability>/spec.md   # DELTAS: ## ADDED|MODIFIED|REMOVED Requirements
    archive/
      YYYY-MM-DD-<change-id>/       # shipped changes (deltas already applied to ../../specs)
```

- **Living specs** (`specs/specs/`) describe current truth. They never contain ADDED/MODIFIED
  markers. They are edited **only** by `spec-archive` applying a change's deltas.
- **Changes** (`specs/changes/`) are the unit of work. Everything a request needs — intent,
  design, tasks, and the spec deltas — lives in one change folder, the durable memory of the
  decision (the "migration").

## Capability naming

- Lowercase, hyphenated, noun-led, behavior-oriented: `student-management`, `course-catalog`,
  `grading-api`, `auth-tokens`. One capability = one coherent area of behavior.

## Change-id naming

- Lowercase, hyphenated, **verb-led**: `add-student-endpoint`, `update-grading-service`,
  `remove-legacy-auth`, `fix-attendance-filter`. Unique within `specs/changes/` (+ archive).

## Requirement & scenario format (living specs and ADDED/MODIFIED deltas)

```markdown
### Requirement: <Behavior Name>

The system SHALL <observable behavior>.

#### Scenario: <Scenario Name>

- GIVEN <precondition>
- WHEN <action>
- THEN <observable outcome>
- AND <additional outcome, optional>
```

Keywords: `SHALL`, `SHALL NOT`, `MUST`, `MUST NOT` (RFC 2119). Scenarios MUST be GIVEN / WHEN / THEN.

## Spec deltas format

Inside `specs/changes/<change-id>/specs/<capability>/spec.md`:

```markdown
# Delta: <Capability Name>

## ADDED Requirements

### Requirement: <New Requirement>
...

## MODIFIED Requirements

### Requirement: <Updated Requirement>
...

## REMOVED Requirements

### Requirement: <Requirement Name Being Removed>
```
