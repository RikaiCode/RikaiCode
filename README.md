# RikaiCode

**Advanced Repository Flattener, Context Generator & Intelligent Grader.**


*Flattening for AI, Context for understanding, and Grading for quality*

RikaiCode is a sophisticated, browser-based tool designed to turn complex codebases into structured, actionable data. Whether you need to feed code into an LLM, audit a project's quality, or simply understand a new architecture, RikaiCode provides the insights you need in a beautiful, dark-themed interface.

![License](https://img.shields.io/badge/license-AGPL%203.0-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-brightgreen)
![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-orange)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

---

## ✨ Key Features

- **Multi-Source Input:** Seamlessly analyze public GitHub/GitLab repositories or upload local files/ZIPs.
- **AI-Powered Analysis:** Integrates with GLM-4.7-Flash to provide architectural summaries and code explanations.
- **Intelligent Grading:** A unified scoring system (A++ to C) based on popularity, activity, maintenance, and static code quality.
- **Security Heuristics:** Automatically scans for hardcoded secrets, API keys, and potential vulnerabilities.
- **Visual Insights:** Generates interactive treemaps, pie charts, and commit heatmaps.
- **One-Click Export:** Export your entire flattened codebase to TXT, JSON, PDF, DOCX, or HTML.

---

## 💡 Use Cases

RikaiCode is versatile and built for developers, security researchers, and data scientists.

1.  **LLM Context Preparation:**
    Flatten entire repositories into a single text file (TXT/JSON) to use as context for Large Language Models like ChatGPT, Claude, or Gemini. It strips away unnecessary binaries and formats the code perfectly for AI consumption.

2.  **Code Quality & Grading:**
    Get an instant "Health Score" for any public repository. Analyze commit frequency, issue ratios, and maintenance activity before using an open-source dependency.

3.  **Security Audits:**
    Run quick heuristic scans to detect hardcoded API keys, AWS secrets, or private keys before pushing code to a public platform.

4.  **Architecture Onboarding:**
    New team members can visualize the file structure, detect dependencies, and read AI-generated summaries to understand a project's architecture in minutes rather than hours.

---

## 📖 How to Use

1. **Select Source:** Choose between GitHub URL, GitLab URL, or Upload Files.
2. **Analyze:** 
   - If using a URL, click "Fetch Repository".
   - If uploading, drag and drop your files.
3. **Explore:** View the repository grade, architecture diagram, security alerts, and code statistics.
4. **AI Insights:** Expand the "Rikai AI Analysis" section to generate architectural summaries.
5. **Export:** Use the export buttons at the bottom to download the flattened context.


---


## 🌐 Online vs. Offline Usage

RikaiCode offers flexible deployment options to suit your workflow.

### ☁️ Run Online (Streamlit Cloud)
You can deploy RikaiCode on Streamlit Community Cloud for quick, accessible analysis from anywhere.
*   **Best for:** Small to medium repositories, quick checks, and shared usage.
*   **Note:** Online deployments may have timeout limits for very large repositories.

### 💻 Run Locally (Offline)
For power users and large-scale analysis, hosting RikaiCode locally on your machine is recommended.
*   **Best for:** Huge repositories (10,000+ lines), private codebases, and heavy AI analysis tasks.
*   **Privacy:** Your code stays on your machine. No data is uploaded to third-party servers (unless you explicitly use the AI analysis features).
*   **Performance:** No execution time limits; handle massive ZIP files and deep scanning without interruption.

---

## 🛠️ Installation & Setup

Follow these steps to run RikaiCode locally on your machine.

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/aurumz-rgb/RikaiCode.git
cd RikaiCode
```

### Step 2: Create a Virtual Environment (Recommended)
This keeps your project dependencies isolated.

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Dependencies
Install all required libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key (Optional)
To enable AI features, you need a ZhipuAI API key.

1. Create a file named `.env` in the project root folder.
2. Add your API key to the file:
   ```env
   ZHIPUAI_API_KEY=your_actual_api_key_here
   ```
3. Save the file.


Once the setup is complete, launch the app using the Streamlit command:

```bash
streamlit run app.py
```

The application will open automatically in your default web browser at `http://localhost:8501`.

---

## 🔗 Acknowledgements

![ZAI](assets/GLM.png)

Z.ai GitHub: [zai-org](https://github.com/zai-org)

I gratefully acknowledge the developers of **GLM (Z.ai)** for providing the  open-source AI model used in RikaiCode.  

For more information, please see the [GLM-4.7-Flash Hugging Face](https://huggingface.co/zai-org/GLM-4.7-Flash).



---


## License

<a href="https://www.gnu.org/licenses/agpl-3.0">
  <img src="https://upload.wikimedia.org/wikipedia/commons/0/06/AGPLv3_Logo.svg" width="170" alt="AGPL v3 License"/>
</a>

This project is licensed under the AGPL 3.0 License - see the [LICENSE](LICENSE) file for details.

---

## 📨 Contact

Questions, feedback, or collaboration ideas? Reach out at [pteroisvolitans12@gmail.com](mailto:pteroisvolitans12@gmail.com) or open an issue on GitHub.

Contributions are always welcome!

---

<p align="center">Made with 🤍 by <strong>Aurumz</strong></p>