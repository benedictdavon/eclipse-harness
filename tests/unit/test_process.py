from __future__ import annotations

import sys

from eclipse_harness.process import run_bounded


def test_process_output_is_bounded() -> None:
    result = run_bounded(
        (sys.executable, "-c", "print('x' * 10000)"),
        timeout=5,
        output_limit=128,
    )
    assert result.returncode == 0
    assert "output truncated" in result.stdout
    assert len(result.stdout) < 200
