<div align="center">
    <h1>ctxgen</h1>
    <p>A sleek CLI tool to bundle your source code into a single text file for AI context windows.</p>
    <p>
        <img src="https://img.shields.io/badge/version-v2.0.0-4c1?style=flat-square"/>
        <img src="https://img.shields.io/badge/status-stable-2ea44f?style=flat-square"/>
        <img src="https://img.shields.io/badge/platform-Linux-FCC624?style=flat-square&logo=linux&logoColor=black"/>
        <img src="https://img.shields.io/badge/maintenance-active-1f6feb?style=flat-square"/>
        <img src="https://img.shields.io/badge/language-Python-3572A5?style=flat-square&logo=python&logoColor=white"/>
        <img src="https://img.shields.io/badge/license-MIT-6e7781?style=flat-square"/>
    </p>
</div>

---

## Overview

**ctxgen** eliminates the tedious task of copying and pasting individual source files when providing project context to AI models. Whether you need to feed an entire codebase or just a few specific files into an LLM, ctxgen scans your workspace, presents a clear directory tree, lets you interactively toggle what matters, and outputs a neatly delimited text file ready for your prompt — in seconds.

> [!NOTE]  
> Easily pack your project repository into a clean, structured prompt context for ChatGPT, Claude, Gemini, or any other LLM.

---

## Table of Contents

- [Showcase](#showcase)
- [Features](#features)
- [Interactive Controls](#interactive-controls)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Author](#author)
- [License](#license)

---

## Showcase

<p align="center">
  <em>The tool recursively discovers all eligible files matching your parameters, displays a visual directory tree structure, and opens an interactive checkbox selection menu.</em><br>
  <img src="./assets/screenshots/screenshot-001.png" alt="Interactive file picker showing the directory tree view and interactive checkbox prompt" width="600"/><br><br>
  <em>After confirming your selection, files are seamlessly bundled into a structured text document alongside rich metric statistics.</em><br>
  <img src="./assets/screenshots/screenshot-002.png" alt="Terminal screen showcasing successful bundle execution of selected files into the target output text document" width="600"/><br><br>
</p>

---

## Features

- **Smart Workspace Scanning** — Automatically filters out noisy directories (`.git`, `node_modules`, `venv`, `__pycache__`, etc.) out of the box.
- **Visual Directory Tree View** — Renders a clean hierarchical tree using Rich before file selection for full structural visibility.
- **Interactive Checkbox Selector** — Easily select, toggle, or batch-select files using arrow keys and hotkeys powered by InquirerPy.
- **Extension Filtering** — Isolate exactly what you need by targeting specific extensions (e.g., only `.py` or `.ts` files).
- **Binary Safety Guardrails** — Safe processing that bypasses non-text and binary files preventing corrupted outputs.
- **Tech Purple CLI Theme** — Modern ANSI interface with custom panels, real-time progress indicators, and dynamic metrics reporting.

---

## Interactive Controls

When selecting files in the CLI interactive menu, use the following keybindings:

| Keybinding | Action                                      |
|:-----------|:--------------------------------------------|
| `Space`    | Toggle selection for the focused file       |
| `Ctrl + A` | Toggle selection for **all** eligible files |
| `↑` / `↓`  | Move selection cursor up and down           |
| `Enter`    | Confirm selection and start bundling        |
| `Ctrl + C` | Abort operation gracefully                  |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/avieira-dev/ctxgen.git
cd ctxgen
```

### 2. Set up a virtual environment & install dependencies

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install rich InquirerPy
```

> [!NOTE]  
> If you prefer installing dependencies system-wide or user-wide instead of using a `venv`, you can run `pip install rich InquirerPy --user`.

### 3. Make the script executable

```bash
chmod +x ctxgen
```

> [!TIP]  
> The root `ctxgen` script acts as the entry-point runner, bootstrapping the internal source modules automatically.

### 4. Create a global symlink (Linux / macOS)

```bash
sudo ln -s "$(pwd)/ctxgen" /usr/local/bin/ctxgen
```

Once linked, `ctxgen` is available system-wide from any terminal session.

> [!NOTE]  
> To uninstall, simply remove the symlink:  
> sudo rm /usr/local/bin/ctxgen

---

## Usage

Run the tool using the `txt` command followed by any optional flags:

### Command Structure

```bash
ctxgen generate txt [options]
```

### Quick Examples

```bash
# 1. Run with defaults (Scans current folder, saves to <folder-name>.txt in CWD)
ctxgen generate txt

# 2. Scan a specific folder, filter extensions
ctxgen generate txt -d ~/Projects/my-app -e .py .js

# 3. Scan current folder but save the output package into a custom local file
ctxgen generate txt -o ./my-prompt-context.txt
```

### Available Options

| Flag    | Short | Default                | Description                                                    |
|---------|-------|------------------------|----------------------------------------------------------------|
| `--dir` | `-d`  | `.` *(Current folder)* | Target directory path to scan.                                 |
| `--out` | `-o`  | `<dir-name>.txt`       | Custom output path for the bundled text file in the CWD.       |
| `--ext` | `-e`  | *None (All files)*     | Space-separated list of extensions to include (e.g., .py .js). |

---

## Project Structure

```plaintext
ctxgen/
├── src/
│   └── ctxgen/
│       ├── __init__.py
│       ├── cli.py
│       ├── core.py
│       ├── main.py
│       └── utils/
│           └── messages.py
├── .gitignore
├── ctxgen
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## Author

**Alexandre Vieira**  
GitHub: [@avieira-dev](https://github.com/avieira-dev)

---

## License

Distributed under the [MIT License](LICENSE). See `LICENSE` for details.