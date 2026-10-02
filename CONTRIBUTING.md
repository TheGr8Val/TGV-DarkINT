# Contributing to TGV-DarkINT

Thanks for helping out. TGV-DarkINT is an open-source project by [thegr8val](https://github.com/TheGr8Val).

## Reporting bugs and requesting features

Open an issue with the matching template. Include OS, Python version, the exact command, and the full output.
**Never paste real credentials, victim data, or live malware samples into an issue.**

Security problems go through [SECURITY.md](SECURITY.md), not public issues.

## Development setup

```bash
git clone https://github.com/TheGr8Val/TGV-DarkINT.git
cd TGV-DarkINT
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
ruff check .
```

## Pull requests

1. Branch from `main` (`feat/...`, `fix/...`, `docs/...`).
2. Add or update tests for any behaviour change. CI runs `pytest` and `ruff` on Python 3.9 to 3.13.
3. Update [CHANGELOG.md](CHANGELOG.md) under an `Unreleased` heading.
4. Keep PRs focused. Use conventional commit prefixes (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).

## Code style

- Python 3.9+, type hints on public functions, `ruff` clean.
- No new runtime dependencies without discussion (the project is stdlib-only on purpose).
- Contributions are licensed under the MIT License of this repository.
