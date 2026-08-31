# Review blocker and preliminary findings

Terminal non-executable blocker: the pinned checkout is clean with empty staged/unstaged diffs, so there is no authentic candidate to review or correct. No described candidate changes were invented.

A reviewer must reject all of these defects before acceptance:

1. Sorting only the root `readdir` result is insufficient. Root and `pre/` relative paths must be combined, sinceRef/ignored-file filtered, and then subjected to one deterministic ordering before read/parse mapping; otherwise cross-group result order remains structural and pre enumeration remains nondeterministic.
2. `README.md` matching must remain case-insensitive (`/^README\.md$/i`), so variants such as `readme.md` stay ignored.
3. Exact `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` entries must all remain ignored; removing `CLAUDE.md` admits repository instruction content as a changeset.

The base provides the intended ignore policy but not the requested deterministic final sort. That fact describes the correction target; it is not authorization to create a synthetic candidate or implement directly against the pristine base in a review-correction case.

## Required host action

Attach/apply the authentic candidate and provide trusted candidate-patch provenance bound to run `V02-REAL-030`, plan revision `1`, plan digest `sha256:7751656c537b2df175ec3d4aaa11b894b52a84c72568ca8a3423a16b4083f99b`, and base revision `b4dc91f545ff2afead214278b7b5ebc8d4e96322`. A future correction contract may write only `packages/read/src/index.ts` and `packages/read/src/index.test.ts`, preserve every ignore and sinceRef/pre behavior, test unsorted root+pre entries and ignored variants, and use at most two review rounds. Its only required validation must be the exact packet command; any Vitest command is supplemental (`required:false`).

## Routing and boundaries

Route authentic diff review to a frontier reviewer and bounded corrections to a low-cost executor. Effective identities/permissions are unverified. No product write, network, credentials, external effects, destructive actions, dependency installation, descendants, fabricated patch, or ignored-content weakening is authorized. Host owns patch provenance, boundary capture, and review budget.
