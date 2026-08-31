# V02-REAL-011 terminal result

**Status:** architecture revision required; embedded worker task not authorized

The architecture successfully identifies the schema migration, additive public user representation, viewer-owned timezone source, strict invalid-zone policy, UTC compatibility invariants, shared post/message render path, localization boundary, and single-writer ownership. However, the embedded task cannot yet satisfy its own invalid-form contract without worker improvisation:

1. The current shared `SelectField` macro does not display field errors, while the relevant templates are outside or forbidden by the write scope.
2. The promised zero-commit/zero-mutation invalid submission conflicts with the preserved `before_request` hook, which updates and commits `last_seen` before form validation.

Return the plan to the architect to authorize and specify error rendering and to define invalid-submit atomicity precisely. No implementation or worker delegation is authorized until the revised task closes both boundaries.

