# Manual and generic workflow

Eclipse remains useful without native agents.

1. An architect or human creates an approved plan and task contract.
2. Validate it with `eclipse validate task.json --kind task` and add it to a run.
3. Give that JSON plus the smallest referenced context to any capable worker.
4. Require a result JSON; validate and ingest it.
5. Give the requirement, plan, task, result, actual diff, and evidence to an independent reviewer.
6. Validate and ingest the review.
7. Render status/handoff views.

Model fields remain preferences or null; effective identity should be unavailable unless the external host supplies trusted metadata. Desired permissions remain documented policy when the host cannot enforce them.
