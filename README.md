<div align="center">

# 🕸️ TGV-DarkINT

### *Learn the dark web's vocabulary and tradecraft without ever going there.* 🔦

[![CI](https://github.com/TheGr8Val/TGV-DarkINT/actions/workflows/ci.yml/badge.svg)](https://github.com/TheGr8Val/TGV-DarkINT/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9+-pink?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Alpha-teal?style=flat-square)]()
[![Author](https://img.shields.io/badge/by-thegr8val-ff69b4?style=flat-square)](https://github.com/TheGr8Val)

> 🧠 An interactive, colourful **terminal trainer** that teaches analysts the terminology, ecosystem and
> tactics, techniques and procedures (TTPs) behind dark-web threat activity, **plus a beginner's guide to your very
> first (safe) time on Tor**.

</div>

---

## ✨ Why this exists

Dark-web intel is a core skill for threat hunters and CTI analysts, but the first steps are intimidating, and
the wrong first step can burn your identity. TGV-DarkINT gives you the vocabulary, the detection angle and a
safe-start playbook, using **100% synthetic data**. 🛡️

> 🔒 **The tool itself never connects to Tor or the internet.** The Tor module is *guidance*: you do the browsing
> yourself, in your own prepared environment.

## 📚 What you learn

| 🧩 Module | 📖 Topic |
|---|---|
| **M1** | 🌐 Surface vs deep vs dark web |
| **M2** | 🏪 Ecosystem and service types: markets, forums, privacy services |
| **M3** | 🎯 TTPs from these ecosystems, mapped to MITRE ATT&CK, with a detection-engineering exercise |
| **M4** | 🕵️ An OSINT workflow simulation using synthetic intel |
| **M5** | 🧅 **Your first time on Tor: safe setup and navigation** |

Plus a 🏁 final quiz and a 🛠️ practical exercise. Every TTP ships with a detection hypothesis, data sources and a synthetic log indicator.

## 🧅 New to Tor? Start with M5

> Do this module **before** you touch Tor.

**🧰 Pick your setup**

| Option | Best for | Heads up |
|---|---|---|
| 🧅 **Tor Browser** (dedicated machine/profile) | Quick, low-risk reading | Your host OS is still in the loop |
| 💿 **Tails** (live USB) | Sensitive one-off sessions, zero local traces | Everything is forgotten at shutdown, even your notes |
| 🧱 **Whonix** (Gateway + Workstation VMs) | Repeatable investigations with tools and snapshots | Heavier setup; revert snapshots after each session |
| 🔐 **VPN + Tor** | Hiding Tor use from your ISP, or policy-required egress | Shifts trust to the VPN provider. Not magic anonymity |

**🚀 Your first session**

1. 🧪 Prepare a clean environment (Tails or Whonix recommended) with no personal accounts
2. ✅ Launch Tor Browser and verify at `check.torproject.org`; set security level to **Safer/Safest**
3. 🦆 Start on **DuckDuckGo** and search for the **Ahmia** search engine
4. 🔎 Search Ahmia for keywords tied to your research objective
5. 🗺️ Search Ahmia for **hidden wikis** and **onion directories** to learn how the ecosystem is organised. Treat every copy as *unverified*
6. 🔗 Cross-check onion addresses against reputable public sources before relying on them
7. 📝 Observe, document with defanged URLs, then close out (New Identity, revert snapshot or power off Tails)

**🚫 Never:** log in to personal accounts, maximize the window, torrent, open downloads while online, buy anything,
or save/share illegal content. If you hit CSAM, leave immediately and report it (IWF, NCMEC, local police). ⚖️

## 📦 Install

```bash
git clone https://github.com/TheGr8Val/TGV-DarkINT.git
cd TGV-DarkINT
pip install -r requirements.txt   # just `rich`, for the UI
pip install .
```

Requires Python 3.9+. The only dependency is [rich](https://github.com/Textualize/rich), for the colourful UI. 🎨

## 🎮 Usage

```bash
tgv-darkint                 # 🕹️  interactive menu
tgv-darkint modules         # 📚 list modules
tgv-darkint show M5         # 🧅 read the first-time-on-Tor guide
tgv-darkint quiz M5         # 🧠 module quiz
tgv-darkint quiz final      # 🏁 final assessment
tgv-darkint exercise        # 🛠️  practical exercise
tgv-darkint validate        # ✅ check the training data
tgv-darkint --plain show M3 # 📄 no colours/emoji (also automatic when piped)
tgv-darkint --data my.json  # 🧪 use your own content file
```

`python -m tgv_darkint` works too.

## 🧩 Custom content

Training content is one JSON file ([trainer.json](src/tgv_darkint/data/trainer.json)). Copy it, edit it, and run it
with `--data`. `tgv-darkint --data my.json validate` checks the structure, including that every quiz answer index is valid.

## 🛡️ Safety and ethics

- 🧪 Synthetic data only: IPs, users and log lines are made up for teaching
- 📴 No network access of any kind
- 🎓 Educational use only. Follow the laws and organisational policy that apply to you
- 🤝 Observation only. Never purchase, register or engage with threat actors unless you are in an authorized, legally reviewed role

## 🧑‍💻 Development

```bash
pip install -r requirements-dev.txt
pip install -e .
pytest
ruff check .
```

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) and [CHANGELOG.md](CHANGELOG.md).

## 📜 License

[MIT](LICENSE) © 2026 thegr8val 💜
