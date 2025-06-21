# 🤖 AI-Powered Content Creation Team

An autonomous multi-agent system built with the Qwen-Agent framework that researches, writes, reviews, and illustrates a complete blog post from a single topic prompt.

---

### 🎥 Live Demo / Video

*(**Recommendation:** Record a short screen capture of you using the Gradio UI. Upload it to YouTube or another platform and embed the link or GIF here. This is the most effective way to showcase your project.)*

**[Link to Live Demo or a GIF of the app in action]**

---

### ✨ Key Features

* **Multi-Agent Collaboration:** Utilizes a team of four specialized AI agents (Outliner, Writer, Reviewer, Image Generator) that work in sequence to produce a final article.
* **Dynamic Research:** The Writer Agent uses the Tavily Search API to gather real-time, relevant information, ensuring the content is timely and factual.
* **Autonomous Workflow:** The entire content creation pipeline is orchestrated from a single input topic, demonstrating end-to-end automation.
* **Custom Tool Integration:** Features a custom-built search tool (`TavilySearchTool`) to replace a buggy default, showcasing practical problem-solving and framework extension.
* **Interactive UI:** A user-friendly web interface built with Gradio allows for easy interaction without needing to use the command line.

---

### 🏗️ System Architecture

This project uses a pipeline architecture where the output of one agent becomes the input for the next.

```
[User Topic] -> [OutlineAgent] -> [Outline]
                                     |
                                     v
                  +------------------+------------------+
                  |                  |                  |
           [WriterAgent]      [WriterAgent]      [WriterAgent]  (Runs for each outline section)
                  |                  |                  |
                  +------------------+------------------+
                                     |
                                     v
                             [Combined Draft]
                                     |
                                     v
                              [ReviewerAgent]
                                     |
                                     v
                              [Polished Text]
                                     |
                                     v
[ImageAgent] -> [Image URL] -> [Final Article Assembly] -> [Save to .md file]
```

---

### 🚀 Getting Started

Follow these steps to set up and run the project locally.

#### **Prerequisites**

* Python 3.10+
* `uv` (or `pip`) for package installation
* API keys for:
    * Alibaba Cloud Dashscope (for the Qwen LLM)
    * Tavily Search API (for web research)

#### **1. Clone the Repository**

```bash
git clone [your-github-repo-url]
cd ai_content_team
```

#### **2. Set Up the Environment**

Create a virtual environment:

```bash
# Using uv
uv venv

# Activate it (on Windows)
.\.venv\Scripts\activate
```

#### **3. Install Dependencies**

```bash
uv pip install -r requirements.txt
```

#### **4. Configure API Keys**

Create a `.env` file in the project root and add your API keys:

```
DASHSCOPE_API_KEY="sk-your-dashscope-key"
TAVILY_API_KEY="tvly-your-tavily-key"
```

---

### Usage

You can run the project in two ways:

#### **1. Interactive Web UI (Recommended)**

Launch the Gradio application:

```bash
python app.py
```

Open your browser to the local URL provided (e.g., `http://127.0.0.1:7860`).

#### **2. Command-Line Interface**

Run the entire workflow from your terminal:

```bash
python main.py --topic "Your chosen topic here"
```

The final article will be saved as a markdown file in the `/outputs` directory.
