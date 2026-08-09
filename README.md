# WortWerk 🇩🇪

A small CLI tool for practicing German vocabulary and articles.

WortWerk is a personal project I'm building alongside my journey of learning German. The goal is to create a simple tool that I can actually use while learning.

## Features

* Vocabulary management
* Vocabulary filtering and sorting
* German article practice
* Interactive quizzes
* CEFR level-based practice
* Colored CLI interface

## Requirements

* Python 3.10+
* SQLite

No external database server is required.

## Installation

Clone the repository and install the project dependencies:

```bash
git clone https://github.com/AmirmasoudCS/WortWerk.git
cd WortWerk
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

To see the available commands and options:

```bash
python -m scripts.cli -h
```

### Vocabulary Management

| Command                    | Alias                 | Functionality                            |
| :------------------------- | :-------------------- | :--------------------------------------- |
| `--help`                   | `-h`                  | Show help messages                       |
| `init`                     | —                     | Initialize the database                  |
| `add`                      | —                     | Add a new word                           |
| `list`                     | —                     | List vocabulary                          |
| `list --help`              | `list -h`             | Show help for the list command           |
| `list --article <article>` | `list -art <article>` | Filter by article                        |
| `list --level <level>`     | `list -lev <level>`   | Filter by level                          |
| `list --sort <method>`     | `list -s <method>`    | Sort by ID, alphabetical order, or level |
| `list --reverse`           | `list -rev`           | Reverse the sort order                   |
| `delete <id>`              | —                     | Delete a word by ID                      |
| `edit <id>`                | —                     | Edit a word by ID                        |

For example:

```bash
python -m scripts.cli list --sort alphabetical
```

## Practice

Start a practice session with:

```bash
python scripts/practice.py
```

Practice sessions allow you to select the number of words and CEFR levels to practice. Words are shuffled for each session, and you can answer article questions using either the article itself or its corresponding number.

Practice results are not saved.

## Project Status

WortWerk is an ongoing personal project that will evolve alongside my German-learning journey.
