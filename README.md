<div align="center">

# TGV-DarkINT

### *Learn the dark web's vocabulary and tradecraft without ever going there.*

[![CI](https://github.com/TheGr8Val/TGV-DarkINT/actions/workflows/ci.yml/badge.svg)](https://github.com/TheGr8Val/TGV-DarkINT/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9+-pink?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Alpha-teal?style=flat-square)]()
[![Author](https://img.shields.io/badge/by-thegr8val-ff69b4?style=flat-square)](https://github.com/TheGr8Val)

</div>

TGV-DarkINT is an interactive command-line trainer that teaches analysts the terminology, ecosystem and
tactics, techniques and procedures (TTPs) tied to dark-web threat activity. Everything is **synthetic**:
the tool never connects to Tor, never fetches anything, and contains no illicit content.

## What you learn

| Module | Topic |
|---|---|
| M1 | Surface vs deep vs dark web |
| M2 | Dark-web ecosystem and service types (markets, forums, privacy services) |
| M3 | TTPs that originate in these ecosystems, mapped to MITRE ATT&CK, with a detection-engineering exercise |
| M4 | An OSINT workflow simulation using synthetic intel |

Plus a final quiz and a practical exercise. Each TTP includes a detection hypothesis, data sources and a synthetic log indicator.

## Who it is for

- SOC and threat-intel analysts new to dark-web sources
- Detection engineers turning TTPs into hypotheses and rules
- Trainers who need safe, ready-made material

## Install

```bash
git clone https://github.com/TheGr8Val/TGV-DarkINT.git
cd TGV-DarkINT
pip install .
```

Requires Python 3.9+. No third-party runtime dependencies.

## Usage

```bash
tgv-darkint                 # interactive menu
tgv-darkint modules         # list modules
tgv-darkint show M3         # read a module
tgv-darkint quiz M1         # take a module quiz
tgv-darkint quiz final      # final assessment
tgv-darkint exercise        # practical exercise
tgv-darkint validate        # check the training data
tgv-darkint --data my.json  # use your own content file
```

`python -m tgv_darkint` works too.

## Custom content

Training content is one JSON file ([trainer.json](src/tgv_darkint/data/trainer.json)). Copy it, edit it,
and run it with `--data`. `tgv-darkint --data my.json validate` checks the structure, including that every quiz
answer index is valid.

## Safety and ethics

- Synthetic data only. IPs, users and log lines are made up for teaching.
- No network access of any kind.
- Educational use only. Do not use what you learn here to access or interact with illicit services.
  Follow the laws and organisational policy that apply to you.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) and [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE) (c) 2026 thegr8val
