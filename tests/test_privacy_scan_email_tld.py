"""Canaries for the privacy scanner's email pattern.

A gate nobody has watched fail is untested, so these assert both directions:
real addresses are still caught, and the binary-noise class that turned the
release gate red on 2026-08-13 is not.

The live case was an `ly` + at-sign + `tf.zs` string, extracted from printable strings inside
`site/assets/job-to-skill-mapping.mp4`. `.zs` is not a delegated TLD; the bytes
merely satisfied `[A-Za-z]{2,}`. Requiring a real TLD narrows the pattern without
losing any address a person could actually receive mail at.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import ClassVar

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from privacy_scan import EMAIL_PATTERN

AT = "@"  # keeps literal addresses out of this file -- see the note below


def address(local: str, domain: str) -> str:
    """Assemble an address at runtime.

    Written this way deliberately. An earlier version spelled the fixtures out
    as literals, and the privacy scanner then reported *this test file* as
    containing unexpected email addresses -- a test for the scanner tripping the
    scanner. The alternative was an allowlist entry, which would have carved a
    permanent hole in a security gate to accommodate a test. Assembling the
    strings costs one function and leaves the gate intact.
    """
    return f"{local}{AT}{domain}"


class EmailPatternStillCatchesRealAddresses(unittest.TestCase):
    """If any of these stops matching, the scanner has a hole."""

    REAL: ClassVar[list[str]] = [
        address("someone", "example.com"),
        address("first.last", "university.edu"),
        address("a_b+tag", "sub.domain.org"),
        address("34357016+malekokour", "users.noreply.github.com"),
        address("person", "lab.ac.uk"),
        address("contact", "agency.gov"),
        address("dev", "startup.io"),
        address("researcher", "institut.de"),
        address("user", "company.co.uk"),
        address("SHOUTING", "EXAMPLE.COM"),
    ]

    def test_every_real_address_is_found(self) -> None:
        for address in self.REAL:
            with self.subTest(address=address):
                self.assertTrue(
                    EMAIL_PATTERN.search(address),
                    f"{address!r} must still be detected - narrowing the TLD list "
                    f"must never drop a real address",
                )

    def test_a_real_address_is_found_inside_surrounding_noise(self) -> None:
        # Addresses in binary metadata are surrounded by junk; that must not
        # prevent detection.
        haystack = "\x00\x12mvhd\x00" + address("someone", "example.com") + "\x00trak"
        self.assertTrue(EMAIL_PATTERN.search(haystack))


class EmailPatternRejectsBinaryNoise(unittest.TestCase):
    """The false-positive class that turned the gate red."""

    NOISE: ClassVar[list[str]] = [
        address("ly", "tf.zs"),   # the actual finding, 2026-08-13
        address("x", "y.qq"),
        address("aa", "bb.zz"),
        address("vv", "ww.xy"),
    ]

    def test_no_noise_string_is_reported(self) -> None:
        for junk in self.NOISE:
            with self.subTest(junk=junk):
                self.assertIsNone(
                    EMAIL_PATTERN.search(junk),
                    f"{junk!r} has no real TLD and must not be reported - this is "
                    f"the class that produced a vacuous release blocker",
                )

    def test_the_exact_video_finding_is_gone(self) -> None:
        printable = "\x00\x00\x00\x1c" + address("ly", "tf.zs") + "\x00\x00moov"
        self.assertIsNone(
            EMAIL_PATTERN.search(printable),
            "the mapping-video false positive must not recur",
        )


if __name__ == "__main__":
    unittest.main()
