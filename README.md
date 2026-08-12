<div align="center">

![WortWerk German Flag](./assets/images/german_flag/german2.jpg)

# WortWerk

**A small CLI tool for practicing German vocabulary, articles, and translations.**


*WortWerk is a personal project I'm building alongside my journey of learning German. The goal is to create a simple tool that I can actually use while learning.*

</div>
</br>


## 📊 Current Vocabulary

The current WortWerk vocabulary dataset is organized by German article and CEFR level:

| Article | A1 | A2 | B1 | B2 | C1 | C2 | Total |
| :------ | --: | --: | --: | --: | --: | --: | ----: |
| der     | 24 | 0 | 0 | 0 | 0 | 0 | 24 |
| die     | 30 | 0 | 0 | 0 | 0 | 0 | 30 |
| das     | 29 | 0 | 0 | 0 | 0 | 0 | 29 |
| **Total** | **83** | **0** | **0** | **0** | **0** | **0** | **83** |

> **Dataset snapshot:** August 2026  
> The vocabulary dataset is continuously growing alongside my German-learning journey. Run `python -m scripts.wortwerk stats` to view the current statistics.

## ✨ Features

- Vocabulary management
- Vocabulary filtering and sorting
- Vocabulary search
- German → Article practice
- German → English practice
- English → German practice
- German → Plural practice
- CEFR level-based practice
- Practice accuracy tracking
- Practice session history
- Per-word practice history
- Completed and unfinished session tracking
- Practice session timer
- Colored CLI interface


## 🛠️ Requirements

* Python 3.10+
* SQLite

No external database server is required.

## 📦 Installation

Clone the repository and install the project dependencies:

```bash
git clone https://github.com/AmirmasoudCS/WortWerk.git
cd WortWerk
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

## 🚀 Getting Started

To see the available commands and options:

```bash
python -m scripts.worwerk -h
```

### Vocabulary Management

| Command                    | Alias                 | Functionality                            |
| :------------------------- | :-------------------- | :--------------------------------------- |
| `--help`                   | `-h`                  | Show help messages                       |
| `init`                     | -                     | Initialize the database                  |
| `add`                      | -                     | Add a new word                           |
| `list`                     | -                     | List vocabulary                          |
| `list --help`              | `list -h`             | Show help for the list command           |
| `list --article <article>` | `list -art <article>` | Filter by article                        |
| `list --level <level>`     | `list -lev <level>`   | Filter by level                          |
| `list --sort <method>`     | `list -s <method>`    | Sort by ID, alphabetical order, or level |
| `list --reverse`           | `list -rev`           | Reverse the sort order                   |
| `delete <id>`              | -                     | Delete a word by ID                      |
| `edit <id>`                | -                     | Edit a word by ID                        |
| `stats`                    | -                     | Show vocabulary statistics               |
| `search <query>`           | -                     | Search for a word or translation         |

For example:

```bash
python -m scripts.wortwerk list --sort alphabetical
```

## 📝 Practice

Start a practice session with:

```bash
python -m scripts.practice_mode
```

Practice sessions allow you to select the number of words and CEFR levels to practice. Words are shuffled for each session, and article questions can be answered using either the article itself or its corresponding number.

Practice results are not saved.

## 🤝 Contributing

WortWerk is a personal learning project, but contributions and suggestions are welcome.

If you would like to contribute, please see the [CONTRIBUTING.md](./CONTRIBUTING.md) file.

## ⚖️ License

WortWerk is licensed under the MIT License.

See the [LICENSE](./LICENSE) file for the full license text.

## 📌 Project Status

WortWerk is an ongoing personal project that will evolve alongside my German-learning journey.

[🛣️ Roadmap](./features.md)
