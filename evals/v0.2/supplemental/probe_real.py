"""Dependency-free behavioural probes for frozen supplemental real candidates."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def expect_value_error(callable_: object, message: str) -> None:
    try:
        callable_()  # type: ignore[operator]
    except ValueError as error:
        if str(error) != message:
            raise AssertionError(f"wrong error: {error!s}") from error
    else:
        raise AssertionError("ValueError was not raised")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_id")
    parser.add_argument("source_root", type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(args.source_root / "src"))

    if args.case_id == "V02-SUP-REAL-001":
        from itsdangerous.encoding import int_to_bytes

        expect_value_error(lambda: int_to_bytes(-1), "num must be non-negative")
        assert int_to_bytes(0) == b""
        assert int_to_bytes(2**64 - 1) == b"\xff" * 8
    elif args.case_id == "V02-SUP-REAL-002":
        from itsdangerous.encoding import bytes_to_int

        expect_value_error(
            lambda: bytes_to_int(b"\xff" * 9),
            "bytestr must contain at most 8 bytes",
        )
        assert bytes_to_int(b"\xff" * 8) == 2**64 - 1
    elif args.case_id == "V02-SUP-REAL-003":
        from itsdangerous.encoding import base64_decode, base64_encode
        from itsdangerous.exc import BadData

        try:
            base64_decode("mañana")
        except BadData:
            pass
        else:
            raise AssertionError("non-ASCII str did not raise BadData")
        assert base64_decode(base64_encode("ok")) == b"ok"
    else:
        raise ValueError(f"unknown case: {args.case_id}")

    print("ECLIPSE_ACCEPTANCE_EVIDENCE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
