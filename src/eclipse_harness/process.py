"""Bounded subprocess capture for diagnostics and local Git operations."""

from __future__ import annotations

import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Sequence


@dataclass(frozen=True)
class BoundedProcess:
    returncode: int
    stdout: str
    stderr: str


def run_bounded(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
    timeout: int = 60,
    output_limit: int = 65536,
) -> BoundedProcess:
    process = subprocess.Popen(
        tuple(command),
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    truncated = {"stdout": False, "stderr": False}

    def drain(name: str, stream: BinaryIO) -> None:
        while True:
            chunk = stream.read(8192)
            if not chunk:
                break
            remaining = output_limit - len(buffers[name])
            if remaining > 0:
                buffers[name].extend(chunk[:remaining])
            if len(chunk) > remaining:
                truncated[name] = True

    assert process.stdout is not None and process.stderr is not None
    threads = [
        threading.Thread(target=drain, args=("stdout", process.stdout), daemon=True),
        threading.Thread(target=drain, args=("stderr", process.stderr), daemon=True),
    ]
    for thread in threads:
        thread.start()
    try:
        returncode = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        raise
    finally:
        for thread in threads:
            thread.join()

    def render(name: str) -> str:
        value = buffers[name].decode("utf-8", errors="replace")
        return value + ("\n[output truncated]" if truncated[name] else "")

    return BoundedProcess(returncode, render("stdout"), render("stderr"))
