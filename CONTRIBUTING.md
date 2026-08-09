# Contributing to WortWerk 🇩🇪

Thank you for your interest in contributing to WortWerk!

WortWerk is a personal project I'm building alongside my journey of learning German. Contributions, suggestions, bug reports, and ideas are welcome.

## 🛠️ Getting Started

Before contributing, make sure you have:

* Python 3.10 or newer
* Git
* SQLite

Clone the repository:

```bash
git clone https://github.com/AmirmasoudCS/WortWerk.git
cd WortWerk
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database:

```bash
python -m scripts.cli init
```

You can check that the CLI is working with:

```bash
python -m scripts.cli -h
```

## 🌱 Creating a Branch

Please create a separate branch for your changes rather than working directly on `main`.

Some examples:

```text
feature/search
feature/statistics
feature/quiz-modes
fix/article-validation
docs/update-readme
```

A branch should focus on one feature, fix, or improvement whenever possible.

## 💻 Making Changes

When working on WortWerk, please try to follow the existing project structure and coding style.

Some general guidelines:

* Keep functions focused on a single responsibility.
* Reuse existing utilities instead of duplicating functionality.
* Keep database operations inside the repository layer.
* Keep CLI presentation and formatting inside the appropriate formatter or CLI modules.
* Reuse constants from `config/constants.py` rather than defining duplicate values.
* Keep user-facing messages clear and concise.
* Avoid introducing unnecessary dependencies.

If you are unsure where a change belongs, feel free to open an issue and discuss it before implementing the change.

## 🧪 Testing Your Changes

Before opening a Pull Request, make sure your changes work locally.

At minimum, test the relevant CLI functionality manually.

For example:

```bash
python -m scripts.cli -h
python -m scripts.cli list
python -m scripts.cli add
python -m scripts.cli edit <id>
python -m scripts.cli delete <id>
python scripts/practice.py
```

If your change affects an existing feature, make sure that the existing functionality still works as expected.

If automated tests are added to the project in the future, contributions should also pass the project's test suite.

## 📝 Commit Messages

Please use short and descriptive commit messages.

Examples:

```text
Add vocabulary search
Fix article validation
Add practice statistics
Improve vocabulary table
Update README
```

Try to describe **what the commit changes**, rather than using vague messages such as:

```text
fix stuff
update
changes
asdf
```

## 📤 Pull Requests

When your changes are ready:

1. Push your branch to your fork.
2. Open a Pull Request against the `main` branch.
3. Provide a clear title describing the change.
4. Briefly explain what you changed.
5. Mention any relevant issues.
6. Make sure the project still works locally.

For example:

```text
Title:
Add vocabulary search command

Description:
Adds a new search command that allows users to search
German words and English translations.

Related issue:
Closes #15
```

Small fixes and documentation improvements can usually be submitted directly as Pull Requests.

For larger features or significant changes, it is recommended to open an issue first so the idea can be discussed before implementation.

## 🔍 Pull Request Review

Pull Requests may be reviewed before being merged.

During review, changes may be requested to:

* Improve code structure.
* Fix bugs.
* Add missing validation.
* Improve documentation.
* Follow existing project conventions.

If changes are requested, simply update your branch and push the new commits. The Pull Request will update automatically.

## 🐛 Reporting Bugs

If you find a bug, please open a GitHub Issue.

Try to include:

* What you were trying to do.
* What you expected to happen.
* What actually happened.
* The command you used.
* Any relevant error messages.
* Steps to reproduce the problem.

For example:

```text
Command:
python -m scripts.cli list --level A1

Expected:
Only A1 vocabulary should be displayed.

Actual:
Words from other levels are also displayed.
```

## 💡 Feature Requests

Feature ideas are welcome.

Before implementing a significant new feature, consider opening an issue describing:

* What the feature would do.
* Why it would be useful.
* How you think it could work.

This is especially useful for larger changes that could affect the existing CLI or database structure.

## 🇩🇪 Vocabulary Contributions

Since WortWerk is also a German-learning project, contributions involving German vocabulary are welcome.

When suggesting vocabulary, please provide accurate information where possible, including:

* German word
* English translation
* Article
* Plural form
* CEFR level

Please avoid submitting duplicate or questionable vocabulary entries.

## 📜 License

By contributing to WortWerk, you agree that your contributions will be licensed under the same license as the project.

See the [LICENSE](LICENSE) file for details.

---

Thank you for helping improve WortWerk! 🇩🇪

Whether you're fixing a bug, improving the CLI, adding a new quiz mode, contributing vocabulary, or simply suggesting an idea, every contribution is appreciated.
