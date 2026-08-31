# V02-REAL-011 independent architecture review

## Outcome

**Changes required; return to architect.** The plan identifies and fixes most cross-cutting model, migration, API, timezone-source, rendering, localization, and compatibility decisions, but the embedded implementation contract still delegates two contradictory form/error boundaries. It is not safe to issue as written.

This review is bound to packet SHA-256 `e4eb05717f868453a3ef8da5a088df3e11ba97e632dfec76a2f2f05efbc9f86a`, architect-output SHA-256 `ef03f0ce13af0d0f16605e1bc404c5456d37339aaaec62af939e3c7898af7916`, embedded plan revision 1/digest `f222cf2050f0b539ebe217ce907298e4a6e98c54d98bd783cd81e7a838f7fa5d`, and clean checkout `a975ef64864354867c88e0ed3a17ba7d17dca752`. All embedded context-manifest file digests match the checkout.

## Criterion verdicts

| Criterion | Verdict | Direct evidence |
|---|---|---|
| Database migration and public representation changes are identified | Satisfied | The plan fixes `User.timezone` as non-null `String(64)` with ORM/database default `UTC`, a new revision after sole head `834b1a697901`, existing-row backfill without timestamp rewrites, and an additive `timezone` field in all existing `User.to_dict()` representations with optional validated create/update input. |
| Timezone source and invalid-zone behavior are fixed | Partially satisfied | Authenticated viewer ownership, IANA/pytz validation, UTC fallback, API 400 behavior, and corrupt-data handling are fixed. The invalid profile-form presentation and mutation/commit boundary conflict with the checkout and authorized scope, as detailed below. |
| No local worker improvises the cross-cutting design | Unsatisfied | A worker cannot meet the required visible localized `SelectField` error within the stated template scope, and must reinterpret the invalid-submit “no commit/no mutation” promise around the existing request hook. |

## Findings

### ARCH-011-01 — Major — invalid-contract

- **Path/symbol:** `app/templates/bootstrap_wtf.html::form_field`, `EditProfileForm.timezone`
- **Relevant criteria:** timezone invalid-zone behavior; no worker improvisation; embedded AC-02 and AC-04
- **Observed evidence:** The plan requires a tampered timezone to re-render with a localized field error. The baseline macro's `SelectField` branch renders only the label and select control; unlike its text/default branches, it never renders `field.errors`. The Task Contract permits edits to `app/main/forms.py` but lists `app/templates/bootstrap_wtf.html` only as read context and explicitly forbids editing it; `app/templates/edit_profile.html` is not writable either.
- **Impact:** The ordinary `SelectField` implementation cannot satisfy the visible field-error contract. A worker would have to violate scope, silently weaken acceptance, or invent an unplanned custom widget/flash presentation.
- **Exact correction:** Freeze the error-presentation design and revise write scope accordingly. Prefer authorizing the shared SelectField macro to render escaped errors with invalid styling, then require a response-level test proving the localized error is visible. If a profile-only rendering path is chosen instead, explicitly authorize and specify that template. Reissue the task after the scope and criterion agree.
- **Disposition:** architect

### ARCH-011-02 — Major — architecture-escalation

- **Path/symbol:** `app/main/routes.py::before_request`, `edit_profile`
- **Relevant criteria:** timezone invalid-zone behavior; backward compatibility; embedded AC-02
- **Observed evidence:** The architecture says an invalid/tampered form “performs no commit,” and AC-02 says invalid form values are rejected “without mutation.” In the pinned checkout, every authenticated request first updates `current_user.last_seen` and calls `db.session.commit()` in `before_request`, before `edit_profile` validates the form. The plan also declares last-seen behavior unchanged and out of scope.
- **Impact:** Literal acceptance is impossible without changing an explicitly preserved compatibility behavior, while interpreting the promise as “no timezone/profile-field mutation and no edit-profile commit” is narrower than the written contract. The worker is left to choose that semantic boundary.
- **Exact correction:** State explicitly that invalid timezone input must leave `timezone`, `username`, and `about_me` unchanged and must not cause an additional edit-profile transaction, while the pre-existing request-level `last_seen` update remains unchanged; adjust evidence language accordingly. If truly zero commit/mutation is required, redesign and authorize the request-hook change before delegation.
- **Disposition:** architect

## Positive architecture assessment

Apart from these findings, the plan appropriately fixes viewer-versus-author ownership, IANA validation, corrupt-row fallback without GET repair, UTC storage/comparison/export invariants, additive API compatibility, the shared post/message render path, locale/timezone separation, one-writer ownership, migration ordering, forbidden production effects, and concrete stop conditions. The checkout supports those repository assumptions, and every embedded reference digest is current.

## Validation and residual risk

No implementation or worker result exists, so implementation criteria and validation commands are not reviewed as completed. The repository remained clean. Residual risk is the unresolved form error/transaction contract; implementation must remain unauthorized until a revised architecture/task closes both findings.

Reviewer permissions: desired read-only; repository use was observational and the checkout remained clean; mechanical read-only enforcement is unverified.

