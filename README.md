# 🤖 Refactor Bot: Autonomous Code Maintenance Agent

Refactor Bot is an **agentic AI-powered solution** designed to autonomously maintain and optimize software repositories. Built entirely on GitHub Actions, it functions as a **self-directed collaborator** that formats code, cleans up unused logic, injects license headers, visualizes architecture, and tracks dependencies — all without human intervention.

This project was created for a hackathon focused on **Agentic AI**, where solutions must demonstrate autonomous decision-making and task execution. Refactor Bot embodies this vision by acting as a **digital steward** of codebases, continuously improving them with minimal human input.

---

## 🔨 What It Builds

Refactor Bot is a **fully functional prototype** of an AI agent that:

- 🧠 **Thinks**: Analyzes code structure, dependencies, and history
- 🧹 **Acts**: Executes formatting, cleanup, and documentation tasks
- 📈 **Improves**: Enhances readability, maintainability, and transparency
- 🔁 **Decides**: Chooses what to fix, when to commit, and how to document

---

## ⚙️ Autonomous Workflows

Each workflow is a self-contained agentic task that runs on a schedule or manually. Together, they form a **maintenance ecosystem**:

| Workflow                  | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `cleanup-unused.yml`      | Removes unused imports and variables using Ruff and Autoflake               |
| `license-header.yml`      | Injects missing license headers into source files                           |
| `auto-format.yml`         | Formats code with Black, Ruff, and Prettier                                 |
| `dependency-manifest.yml` | Generates a dependency tree using `pipdeptree` and commits it               |
| `code-graph.yml`          | Creates module and call graph diagrams using AST and Graphviz               |
| `changelog.yml`           | Parses git history and updates `CHANGELOG.md` using Conventional Commits    |

Each workflow **commits directly to `main`**, making decisions and executing tasks without requiring pull requests or approvals.

---

## 🧠 Agentic Intelligence

Refactor Bot is not just automation — it's **autonomy**. It:

- **Identifies dead code** and removes it
- **Detects missing documentation** and fills it in
- **Visualizes architecture** to aid human understanding
- **Tracks dependencies** to surface complexity
- **Summarizes history** to create living documentation

These behaviors reflect **real-world agentic collaboration**, where AI acts as a proactive teammate rather than a passive tool.

---

## 🌍 Real-World Relevance

Refactor Bot addresses challenges faced by every developer:

- **Code rot** from unused logic and inconsistent formatting
- **Missing documentation** that slows onboarding
- **Opaque architecture** that hinders collaboration
- **Untracked dependencies** that introduce risk

By autonomously solving these problems, Refactor Bot becomes a **digital maintainer** — ideal for open-source projects, internal tools, and educational codebases.

---

## 🚀 Getting Started

1. **Fork this repo** or copy the `.github/workflows/` and `scripts/` folders into your own
2. **Enable GitHub Actions**
3. Watch Refactor Bot go to work — no setup, no tokens, no approvals

---

## 🧪 Tech Stack

- **GitHub Actions** — agentic execution engine
- **Black, Ruff, Prettier** — formatting and linting
- **Autoflake** — cleanup
- **Graphviz + AST** — code visualization
- **pipdeptree** — dependency analysis
- **Python** — orchestration and scripting

---

## 🏁 Hackathon Alignment

Refactor Bot is a prototype of an **Agentic AI-powered solution** that:

- ✅ Performs autonomous decision-making and task execution
- ✅ Demonstrates workflow automation with minimal human input
- ✅ Solves real-world software maintenance challenges
- ✅ Acts as a collaborative agent in developer ecosystems

---

## 📄 License

MIT — free to use, fork, and extend.

---

## 🙌 Built With Love

Exploring the future of **Agentic AI**.  
Refactor Bot is your repo’s silent partner — always watching, always improving.

## 📄 License

MIT
