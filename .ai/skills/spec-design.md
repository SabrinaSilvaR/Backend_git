# Skill: Spec — Design

Create the technical blueprint for a change (`specs/changes/<change-id>/design.md`).
Skip for trivial changes.

## When to use

When a change introduces new Django models, modifies database schema, touches serialization,
alters business services, or introduces new API contracts.

## Procedure

1. **Review proposal and deltas:** Read `proposal.md` and the delta specs.
2. **Technical architecture:**
   - **Database & Models:** fields, relationships (ForeignKey, ManyToMany), indexes, nullability.
   - **Serializers:** fields exposed, input validation rules, read-only fields.
   - **Views & Routing:** APIView vs ViewSet, HTTP methods, permissions, URL paths.
   - **Services & Transactions:** service layer functions, atomic blocks (`@transaction.atomic`).
   - **Security & Permissions:** authentication classes, permission classes.
3. **Save design:** Under `specs/changes/<change-id>/design.md` using `.ai/templates/design.template.md`.
4. **Next step:** `/spec-tasks`.
