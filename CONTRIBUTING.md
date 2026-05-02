
# Contributing to RikaiCode

Thank you for your interest in contributing to **RikaiCode**!
This project is an open-source tool designed to transform complex codebases into **AI-ready context, intelligent grades, and actionable insights**.

Contributions help improve code analysis accuracy, grading reliability, and user experience for developers and researchers.

---

## 🛠️ Ways to Contribute

You can contribute in the following ways:

* Fix bugs in GitHub/GitLab fetching or file parsing
* Add new features (e.g., new export formats, visualizations)
* Improve documentation or usage examples
* Fix broken links or UI glitches
* Enhance grading algorithms or security heuristics
* Optimize performance (especially for large repositories)

---

## Before You Start

* Check existing **Issues** to avoid duplicate work
* For major changes (e.g., changing the grading logic), open an issue first to discuss your idea
* Keep changes focused and minimal

---

## Development Setup

1. Fork the repository
2. Clone your fork:

```bash
git clone https://github.com/aurumz-rgb/RikaiCode.git
cd RikaiCode
```

3. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the app:

```bash
streamlit run app.py
```

---

## Project Structure Guidelines

When contributing:

* Keep logic modular (separate UI, repository processing, and grading logic)
* Maintain the **robust parsing pipeline** (handle encoding errors gracefully)
* Avoid breaking:

  * Repository fetching (GitHub/GitLab)
  * Static analysis & Grading system
  * Security scanning heuristics
  * Export functionality

---

## Coding Standards

* Use clear, readable Python code
* Follow **PEP8** conventions
* Write meaningful variable and function names
* Add comments where logic is complex (especially grading formulas or regex patterns)

---

## AI & API Contributions

Since RikaiCode integrates AI for analysis:

* Ensure compatibility with:
  * ZhipuAI (Current default)
  * *(Feel free to add support for OpenAI, Anthropic, Ollama, etc.)*

* Do not:
  * Hardcode API keys
  * Store sensitive user code data

* Prefer:
  * Config-driven model selection via `.env`
  * Graceful fallbacks if API limits are reached

---

## UI / Streamlit Contributions

* Keep UI clean, dark-themed, and developer-focused
* Avoid clutter — prioritize actionable insights
* Ensure a clear workflow (Input → Analysis → Export)
* Provide helpful progress bars or logs during heavy processing

---

## Continuous Integration (CI) Requirement

All contributions **must pass the repository’s Python CI workflow** before they can be merged.

* Ensure your code runs without errors
* Fix linting and formatting issues
* Make sure all tests (if present) pass

### Before submitting a PR:

Run checks locally if possible:

```bash
# Example (adjust based on repo setup)
pytest
```

If your PR fails CI:

* Review the GitHub Actions logs
* Fix the reported issues
* Push updates to your branch

**Pull requests that fail CI will not be merged.**

---

## Submitting a Pull Request

1. Create a new branch:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes

3. Commit clearly:

```bash
git commit -m "Add: short description of change"
```

4. Push your branch:

```bash
git push origin feature/your-feature-name
```

5. Open a Pull Request

---

## Pull Request Guidelines

* Describe **what** you changed and **why**
* Link related issues (if any)
* Keep PRs small, focused, and testable

---

## Reporting Issues

If you encounter problems, open an issue and include:

* Steps to reproduce
* Expected vs actual behavior
* Logs or screenshots (if applicable)
* Environment details (OS, Python version, Repository size analyzed)

