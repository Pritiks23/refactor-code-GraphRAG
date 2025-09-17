
# 🧼 Refactor Bot

Autonomous code maintenance for Python and web-based repos — powered entirely by GitHub Actions.

## ✨ Features

- ✅ Auto-format code with Black, Ruff, and Prettier
- 🧹 Remove unused imports and variables
- 📊 Generate module and call graph diagrams
- 🕒 Auto-generate `CHANGELOG.md` from git history
- 🔁 All changes go through pull requests

## 🚀 Getting Started

1. **Fork this repo** or copy the `.github/workflows/` and `scripts/` folders into your own.
2. **Enable GitHub Actions** in your repo.
3. **Watch the automation** — PRs will appear on schedule or when triggered manually.

## 📁 Workflows

| Workflow               | Purpose                                | Trigger         |
|------------------------|----------------------------------------|-----------------|
| `auto-format.yml`      | Format code and open PR                | Mon/Thu         |
| `cleanup-unused.yml`   | Remove unused imports/vars and open PR | Tuesday         |
| `code-graph.yml`       | Generate diagrams and commit           | Wednesday       |
| `changelog.yml`        | Update `CHANGELOG.md` from history     | Thursday or tag |

## 📊 Diagrams

Generated SVGs are committed to `/diagrams/`:
- `code_graph_modules.svg`
- `code_graph_calls.svg`

## 🙌 Contributing

Want to add test coverage reports, dependency audits, or refactor suggestions? Open an issue or PR!

## 📄 License

MIT
