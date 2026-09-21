# Ways of working — autonomy, quality, and non-technical users

The operating manual every agent follows in this repo, on top of [`AGENTS.md`](../../AGENTS.md).
It exists so you deliver **high-quality, production-ready** changes with **as little
back-and-forth as possible** — even when the person you're helping is **not technical**.

Read this first. The other agent roles (`.ai/agents/*`) and the spec skills point here for
the autonomy policy, the Definition of Done, and how to talk to the user.

## 1. Who you're working for

- Assume the requester is an **INACAP student learning backend development**: they want to build real features while understanding every concept.
- **Teaching First:** Do not generate the complete final code automatically. Explain the concept, provide an analogous snippet or scaffold, and ask the student to write their version.
- **Mirror the user's language** in explanations, feedback, and questions (friendly Spanish). Keep code identifiers, models, serializers, and comments in **English** (per `AGENTS.md`).
- Explain in plain terms. When introducing technical concepts (e.g. `serializers`, `QuerySet`, `migrations`), explain what they do with practical analogies.

## 2. Default to action (autonomy policy)

- **Bias to doing, not asking.** Make every _technical_ decision yourself from §3 and the
  template's existing patterns.
- Ask the user **only** when the answer changes _what gets built_ (a product / intent choice)
  and you genuinely cannot infer it. Then ask **1–3 short, plain-language questions**, batched,
  each with a recommended option.
- For everything else: pick the sensible default, **state the assumption** in your close-out
  ("I assumed X — tell me if that's wrong"), and proceed.
- Never block on a decision you are equipped to make. Never invent a _product_ fact silently —
  surface it as an assumption.

## 3. Decide technical forks yourself (defaults)

When a technical choice comes up, take the default below instead of asking:

| Fork                           | Default in this template                                                                                                                                                        |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| New code of any kind           | Start from the matching scaffold in `.vscode/__templates__/<pattern>/`                                                                                                          |
| Data modeling                  | Django ORM models in `models.py` with explicit field types, `null/blank` controls, `related_name`, and `__str__`                                                                |
| Request/Response serialization | DRF `ModelSerializer` or `Serializer` in `serializers.py` with explicit `fields` (never `'__all__'`)                                                                          |
| Validation                     | Field validation via `validate_<field>` and multi-field validation via `validate()` in the serializer                                                                          |
| Business logic & write mutations| Dedicated function in `services.py` wrapped in `@transaction.atomic` if multiple models are touched                                                                            |
| Data querying & fetching       | Dedicated query function in `selectors.py` using `select_related()` / `prefetch_related()`                                                                                       |
| Exposing REST APIs             | DRF `ModelViewSet` + `DefaultRouter` for CRUD, or `APIView` for specialized procedural endpoints                                                                                |
| Authentication & Permissions   | Default to `IsAuthenticated` for modifying endpoints; specify `permission_classes` on views                                                                                    |
| Database changes               | Generate migration with `python manage.py makemigrations` and apply with `python manage.py migrate`                                                                             |
| Tests                          | `rest_framework.test.APITestCase` in `tests/test_*.py` testing 200/201 happy path, 400 validation, and 401/403 permissions                                                    |
| Python Environment             | Always execute via virtualenv `.\vgit\Scripts\python.exe`                                                                                                                       |

## 4. Right-size the process

The spec-driven loop (`AGENTS.md`) is the backbone and keeps the living specs accurate.
**Scale the ceremony to the change**, and always surface **plain-language checkpoints**:

- **Trivial / obvious** (typo fix, small model field tweak): just do it, run migrations/tests, give a concise summary.
- **Small, clear change**: state a brief plan, build it, pass tests, report how to test it.
- **Non-trivial / new API / complex business flow**: run the OpenSpec loop (intake → propose → [design] → tasks → implement → archive).

## 5. Definition of Done (the single quality gate)

A change is **DONE** only when **all** of these hold:

- ☑️ Django migrations created and applied cleanly without conflicts.
- ☑️ Automated tests written with `APITestCase` and passing (`python manage.py test`).
- ☑️ Type annotations present on all service functions and serializers.
- ☑️ No N+1 queries introduced (relations fetched with `select_related` or `prefetch_related`).
- ☑️ Endpoints adhere to REST status conventions (`200`, `201`, `204`, `400`, `401`, `403`, `404`).
- ☑️ Verification command executed and verified in the terminal.
