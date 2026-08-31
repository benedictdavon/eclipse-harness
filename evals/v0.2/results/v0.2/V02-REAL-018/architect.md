# Review blocker and preliminary findings

Terminal non-executable blocker. There is no authentic candidate patch in the pinned checkout: `git status` and both staged/unstaged diffs are empty at the trusted base revision. Therefore no review/correction loop can safely start, and no candidate patch has been invented or seeded.

The reviewer must reject the described candidate for both regressions before acceptance:

1. Changing string handling to truthiness would make `'0'` false, but any non-empty trimmed string is a present search-parameter value; `'0'` must remain true.
2. Deleting the URLSearchParams deletion test removes coverage for deletion metadata (`deletedParametersSymbol`) that can make an otherwise empty URLSearchParams value semantically active; that coverage must remain.

The intended null correction is bounded: `null` must return false before the generic object branch, which otherwise reaches `Object.keys(null)`. This observation is not authorization to implement against the pristine base in place of the missing candidate.

## Required host action

Provide the authentic candidate patch (or a checkout containing it) and trusted candidate-boundary metadata tied to run `V02-REAL-018`, plan revision `1`, plan digest `sha256:42f58539969ff31ebbce02ee12cf51897f248c31fc4316a5cbcd8c4aa359c1b0`, and base revision `3419113b48e034fdcf8fa6bd3be3da7b3d0d758f`. Then issue a correction contract limited to `source/utils/options.ts` and `test/main.ts`, preserving `'0'` behavior and deletion coverage, with no more than two review rounds. Its sole required acceptance validation must be copied exactly from the packet; any extra test command must be supplemental (`required: false`).

## Risk, routing, and boundaries

Route the authentic patch first to a frontier reviewer, then any bounded correction to a low-cost executor; effective identities remain unverified. No product write, network, credential, external effect, destructive action, dependency installation, descendant, or fabricated review input is authorized in this revision. The host owns candidate patch provenance, task-local capture, and review-round accounting.
