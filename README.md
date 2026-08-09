# WortWerk 🇩🇪

A small CLI tool for practicing German vocabulary and articles.

WortWerk is a personal project I'm building alongside my journey of learning German. The goal is to create a simple tool that I can actually use while learning.

## Features

- Vocabulary management
- Vocabulary filtering and sorting
- German article practice
- Interactive quizzes
- CEFR level-based practice
- Colored CLI interface

## Requirements

- Python 3.10+
- SQLite

No external database server is required.

## Installation

Clone the repository and install the project dependencies:

```bash
git clone https://github.com/AmirmasoudCS/WortWerk.git
cd wortwerk
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install the requirements:

```bash
pip install -r requirements.txt
```

## Getting Started

In order to see what options you have to manage your vocabulary you can run:

```python
python -m scripts.cli -h
```

Current options:

|Command|Alias|Functionality|
|:-----:|:---:|:-----------:|
| `--help` | `-h` | Shows help messages |
| `init` | - | Initialize the database |
| `add` | - | Add a new word to the vocabulary |
| `list` | - | List words in the vocabulary |
| `list --help` | `list -h` | Shows help messages for list command |
| `list --article <article>` | `list --art <article>` | Filter by article |
| `list --level <level>` | `list -lev <level>` | Filter by level |
| `list --sort <method>` | `list -s <method>` | Sort words by id, alphabetical order, or level |
| `list --reverse` | `list -rev` | Reverse the sort order |
| `delete <id>` | - | Delete a word by id |
| `edit <id>` | - | Edit a word by id |

