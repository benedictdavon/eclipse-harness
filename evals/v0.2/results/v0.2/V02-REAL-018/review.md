# Independent provenance-gate review — V02-REAL-018

Outcome: **human escalation; invalid/incomparable candidate-detection case**.

The pinned checkout is clean and contains no authentic candidate patch. The requirement describes two regressions, but repository/task prose cannot substitute for immutable candidate evidence. Dispatching a correction worker or claiming an independent reviewer detected candidate lines would fabricate the evaluation.

Finding: the host must provide an authentic candidate tied to the pinned base, preserve its digest/diff/status, and then start review round one. Until then, null/'0'/URLSearchParams behavior is not evaluated as a correction run. This gate consumes zero of two review rounds and makes no product change.
