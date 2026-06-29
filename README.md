<div align="center">

# IRL Besty™ ☠️✨

### One tiny mark. One hidden message. Maximum suspicious cuteness.

A warm amber terminal ritual for hiding text inside zero-width characters carried by an ordinary-looking emoji or symbol.

[![PyPI](https://img.shields.io/pypi/v/irl-besty?style=flat-square&color=E47C55&label=PyPI)](https://pypi.org/project/irl-besty/)
[![Python](https://img.shields.io/pypi/pyversions/irl-besty?style=flat-square&color=D7C0AA)](https://pypi.org/project/irl-besty/)
[![License](https://img.shields.io/github/license/Dev2Creator/irl-besty?style=flat-square&color=614B39)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Dev2Creator/irl-besty?style=flat-square&color=3478F6)](https://github.com/Dev2Creator/irl-besty/stargazers)

[Install](#install) · [Explore](#what-is-inside) · [Commands](#commands) · [Format](#how-the-secret-mark-works) · [Safety](#security-note)

</div>

---

    ██████╗ ███████╗███████╗████████╗██╗   ██╗
    ██╔══██╗██╔════╝██╔════╝╚══██╔══╝╚██╗ ██╔╝
    ██████╔╝█████╗  ███████╗   ██║    ╚████╔╝
    ██╔══██╗██╔══╝  ╚════██║   ██║     ╚██╔╝
    ██████╔╝███████╗███████║   ██║      ██║
    ╚═════╝ ╚══════╝╚══════╝   ╚═╝      ╚═╝

IRL Besty turns a terminal window into a tiny secret-message workshop. Choose text or a UTF-8 file, pick a cover mark, add an optional key, and receive something that looks like a single emoji while carrying an invisible payload.

## Install

    pip install --upgrade irl-besty

Open the interactive ritual:

    besty

Use a number or slash-style path such as `/encode`, `/text-encode`, or `/rollback`.

## What is inside

| Path | What you get |
|---|---|
| File encode | Hides a UTF-8 text file inside a `.besty` mark |
| File decode | Restores the hidden message to `.decoded.txt` |
| Text encode | Produces a copyable secret mark directly in the terminal |
| Text decode | Reads a pasted Besty mark |
| Cover selector | 24 emoji and symbol carriers |
| Optional key | Deterministic byte shifting based on your passphrase |
| Shared identity | Optional first-run greeting from the IRL profile system |
| Rollback | Interactive selection from older PyPI releases |

The interface uses Rich panels, a keyboard-driven command list, warm burnt-orange colors, and the same compact ritual language as IRL Wisdom.

## Commands

Start interactively:

    besty

Direct file mode:

    besty encode secret.txt --password "your key" --emoji "💌"
    besty decode secret.besty --password "your key"

Package maintenance:

    besty update
    besty rollback
    besty rollback 2.0.7 --yes

The interactive menu also exposes text encode/decode without requiring a temporary file.

## How the secret mark works

Besty converts each UTF-8 byte into zero-width Unicode characters:

| Character | Role |
|---|---|
| Zero-width space | Binary `0` |
| Zero-width non-joiner | Binary `1` |
| Zero-width joiner | Byte separator |
| Cover mark | Visible carrier placed before the payload |

When a key is supplied, Besty derives a repeatable pseudo-random byte offset from SHA-256 of that key. Decoding requires the same key.

Some apps, websites, clipboard tools, and social platforms remove zero-width characters. If that happens, the hidden payload cannot be recovered. Test the destination before trusting it.

## Security note

IRL Besty is steganographic obfuscation for playful, low-stakes secret sharing. It is **not audited cryptography**, does not provide authenticated encryption, and should not be used for passwords, recovery codes, legal evidence, financial data, or anything whose exposure could harm someone.

For sensitive files, use a maintained encryption tool designed for that job.

## The Moai update ritual

Ask pip for the newest release:

    besty update

On Windows, close other running `besty` terminals before updating so the launcher can be replaced.

## The Moai rollback ritual

Choose an older version interactively:

    besty rollback

Or install a known release:

    besty rollback 2.0.7 --yes

Manual pinning also works:

    pip index versions irl-besty
    pip install --upgrade irl-besty==2.0.7

## How it works

    besty
    ├── argparse direct commands
    ├── Rich terminal rendering
    ├── Questionary-style interactive paths
    ├── UTF-8 byte conversion
    ├── zero-width Unicode payloads
    └── delayed rollback helper

Besty reads and writes local files only during encode/decode. Version checks and package updates contact PyPI.

## Development

    git clone https://github.com/Dev2Creator/irl-besty.git
    cd irl-besty
    python -m pip install -e .
    besty

Build a release:

    python -m build

## Author

Created by **Anika Mukherjee**

Email: [cuteypieanika@gmail.com](mailto:cuteypieanika@gmail.com)

GitHub: [@Dev2Creator](https://github.com/Dev2Creator)

## Copyright, trademark, and license

Copyright © 2026 Anika Mukherjee. All rights reserved.

**IRL Besty™** is a trademark of Anika Mukherjee.

The source code is licensed under the [GNU Affero General Public License v3 or later](LICENSE).

---

<div align="center">

The secret stays quiet. The cover mark remains suspiciously adorable. 🗿

</div>
