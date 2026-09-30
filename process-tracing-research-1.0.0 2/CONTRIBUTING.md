# Contributing

Changes should preserve the distinction between theoretical diagnosticity, empirical source quality, and source dependence.

1. Add or revise a failing test before changing validator behavior.
2. Keep `SKILL.md` as a router; move detailed method material to `references/`.
3. Verify every DOI, title, author, year, and empirical attribution against an original or official metadata source.
4. Do not add copyrighted full text or confidential research material.
5. Run `python3 -m unittest discover -s tests -v`, `python3 scripts/validate_skill.py .`, and the mini-case/invalid-fixture audits.
6. Update `CHANGELOG.md` and `VERSION` for user-visible changes.
7. Keep examples explicit about whether they are real, reconstructed, or fictional.
