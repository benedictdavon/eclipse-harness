# v0.2 evaluation campaign

This directory contains the frozen skill-hardening campaign. `campaign.json` identifies the baseline, policy, host mode, controlled cases, pinned real repositories, and real tasks. The first v0.2 branch commit is the evaluation freeze.

`controlled/fixtures/` contains deterministic seed repositories. `results/baseline/` and `results/v0.2/` preserve raw role outputs, patches, command logs, and scorer reports. Evaluation scripts validate and aggregate artifacts only; they do not execute agents, schedule work, manage git, or own workflow state.

Do not change a frozen case after the baseline. Classify an evaluation flaw and mark the affected comparison invalid or incomparable.
