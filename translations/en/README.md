<div align='center'>
  <img src="../../images/banner-v8.png" alt="AI Agent Tutorial" width="950px">
  <h1 style="margin-top: 15px;">🚀 The Most Systematic AI Agent Hands-on Crash Guide on the Internet (From Zero to Enterprise Deployment)</h1>
  <h4><b>ai-agents-from-zero</b></h4>
  <p><em>Continuously updating through 2026 · Aiming to build the <b>"strongest on Earth"</b> AI Agent tutorial — a one-stop learning path covering <b>systematic tutorials + runnable source code + interview question bank + enterprise-level hands-on projects + long-term tech stack updates</b>, fully aligned with the <b>training curriculum</b> and <b>job postings</b> for "AI Agent / LLM Application Development Engineer"</em></p>
</div>

<div align="center">

<!-- language-switch:start -->

[简体中文](../../README.md) · **English**

<!-- language-switch:end -->

![AI](https://img.shields.io/badge/AI-Agent-00c853?style=flat)
![Language](https://img.shields.io/badge/language-Chinese-2ea44f?style=flat)
![Stars](https://img.shields.io/github/stars/didilili/ai-agents-from-zero?logo=github&style=flat)
[![GitHub](https://img.shields.io/badge/GitHub-Project-181717?logo=github&logoColor=white)](https://github.com/didilili/ai-agents-from-zero/)
[![Read Online](https://img.shields.io/badge/在线阅读-点击访问-blue?logo=bookstack)](https://didilili.github.io/ai-agents-from-zero/#/)

[Quick Start](#quick-start) • [Tutorial Outline](%E6%95%99%E7%A8%8B%E7%9B%AE%E5%BD%95%E5%A4%A7%E7%BA%B2.md) • [Case Collection](%E6%95%99%E7%A8%8B%E6%A1%88%E4%BE%8B%E9%93%BE%E6%8E%A5%E6%B1%87%E6%80%BB.md#教程案例链接汇总源码与在线演示) • [Changelog](%E6%95%99%E7%A8%8B%E6%9B%B4%E6%96%B0%E6%97%A5%E5%BF%97.md) • [Interview Question Bank](AI%E6%99%BA%E8%83%BD%E4%BD%93%E4%B8%8E%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%E9%9D%A2%E8%AF%95%E9%A2%98%E5%BA%93.md) • [Beginner's Guide and FAQ](%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8%E4%B8%8E%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.md)

  <p>
    <a href="https://didilili.github.io/ai-agents-from-zero/#/">📚 Read Online</a>
  </p>

</div>

**📢 Update Notes**: **AI never stops, so the updates continue.** This repository will continue to evolve alongside the **AI large language model tech stack**, committed to being **open source, systematic, and continuously updated**. Models, frameworks, Agents, and hands-on projects will all be continuously refined and upgraded as the ecosystem evolves. It is not just about getting you started — it is about growing with you, from zero foundation to true real-world deployment.

Currently, the **Concepts section** has been fully updated, and two complete hands-on projects have also been completed: the `NL2SQL + LangGraph` hands-on project [Shopkeeper Data Q&A](%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/0-%E5%89%8D%E8%A8%80.md) ([source repository](https://github.com/didilili/shopkeeper-agent)) was completed on May 3. The `DeepAgents` multi-agent hands-on project [Deep Research](%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E6%B7%B1%E5%BA%A6%E7%A0%94%E6%90%9C/0-%E5%89%8D%E8%A8%80.md) ([source repository](https://github.com/didilili/deepsearch-agents)) was completed on May 17. You can click on the [Changelog](%E6%95%99%E7%A8%8B%E6%9B%B4%E6%96%B0%E6%97%A5%E5%BF%97.md) to see the latest repository updates.

There is a lot of LLM application content on the market, but most of it consists of fragmented posts, paid bootcamps, and so on. This repository is designed to let you systematically enter LLM application development without first spending thousands or even tens of thousands of yuan. If it helps you, please give it a **Star** ⭐~

---

## 🤝 Project Sponsorship

<table>
<tr>
<td width="220" align="center" valign="middle">
  <a href="https://passport.compshare.cn/register?referral_code=KyLCDhVe3j5E9o1XBWmIku&ytag=GPU_YY_YX_git_ai-agents-from-zero">
    <img src="../../images/sponsor-compshare-agent-plan.jpg" alt="Compshare" width="160">
  </a>
  <br>
  <sub>High cost-performance Agent Plan recommendation</sub>
</td>
<td valign="middle">

Thank you to <a href="https://www.compshare.cn/coding-plan"><strong>Compshare</strong></a> for sponsoring this project! Compshare is an AI cloud platform under UCloud. It focuses on monthly subscription and pay-per-use, cost-effective domestic model Agent Plan packages, starting as low as 49 yuan per month; it also provides officially relayed stable overseas models, supports integration with Claude Code, Codex, and API calls, and offers enterprises high concurrency, 7\*24 technical support, and self-service invoicing.

🎁 Users who register through <a href="https://passport.compshare.cn/register?referral_code=KyLCDhVe3j5E9o1XBWmIku&ytag=GPU_YY_YX_git_ai-agents-from-zero"><strong>this link</strong></a> will receive a free 5 yuan platform trial credit.

</td>
</tr>
</table>

---

## ✨ Tutorial Highlights

- **🌱 The first systematic open-source AI Agent tutorial on the Internet**: This is a long-term maintained roadmap for AI LLM application development. The market has no shortage of scattered posts or paid bootcamps, but truly systematic, continuously updated tutorials that cover **tutorials + source code + hands-on projects + interview question banks** for AI LLM application development are extremely rare. What this repository aims to do is make this path public, deep, and complete, growing with you from entry level, to advanced topics, and finally to hands-on projects.
- **🧭 One line connecting the full stack of LLM applications**: From large language models and prompts, to low-code (Coze/Dify) and code frameworks (LangChain/LangGraph), and then to enterprise-level RAG/Agent, fine-tuning, and engineering standards — organized uniformly by knowledge system, forming a **complete closed loop**, suitable for systematic mastery rather than fragmented bookmarking.
- **🐍 Focused on the Python ecosystem, directly targeting Agent engineering**: Many courses revolve around **Spring AI** and **langchain4j**, leaning more toward the Java tech stack. The main line of this tutorial focuses on **Python + LangChain + LangGraph**, directly aligning with the most commonly used engineering path for AI Agent / LLM application development today.
- **📘 Accessible to beginners, yet deep enough for engineers**: The entire tutorial is organized in a **progressive from basic to advanced** manner, first thoroughly explaining core concepts such as large language models, Agents, RAG, MCP, and Tool Calling, before moving into source code, frameworks, deployment, and project design. Less jargon and mysticism, more on "why it is designed this way, how the code runs, and how projects are delivered."
- **💼 Enterprise-level hands-on practice, benchmarked for "getting real work done"**: Centered on Shopkeeper Data Q&A, Deep Research, Shopkeeper Knowledge Base, and E-commerce Assistant, it connects intent parsing, multi-source knowledge, human handoff, review, and monitoring; placing **multi-route retrieval, evaluation, observability, cost, and guardrails** into real-world contexts for practice. You will have concrete material for your resume and project discussions, not vague generalities.
- **✅ Every case is held to the standard of "actually running"**: It does not just explain concepts or paste pseudo-code, but provides **runnable cases, source code, environment documentation, and common troubleshooting** wherever possible. Case content is organized based on the approach of actually running through them manually, helping you avoid pitfalls and get started quickly.
- **📚 Tutorial, source code, and interview preparation — a trinity that actually runs**: Not just "read through," but also "run through," and even more importantly, "answer well" — **runnable cases and source code**, **prompt templates**, and deployment approaches, refusing to "only talk about concepts." The interview question bank breaks down questions by the common competency areas found in **training programs and job postings**. A significant portion of the questions are compiled from **real interview questions at major companies**, publicly shared interview experiences, and high-frequency follow-up scenarios, making it suitable for career changers and new graduates to do focused review.
- **🚀 Facing 2026, continuously evolving and hardcore**: The tech stack and high-frequency question patterns will iterate with the ecosystem, aligned with the dimensions of ten-thousand-yuan-level training courses for "AI Application Development Engineer"; it not only tells you "what to learn," but also "how to do projects, how to present projects, and how to answer interview questions." If useful, **a Star is a tip ⭐**.

---

## 🛠 Tech Stack Overview

| Category             | Technology/Platform                                  | Description                                                                             |
| ---------------- | ------------------------------------------- | -------------------------------------------------------------------------------- |
| **LLM and Fundamentals** | LLM, Transformer, MoE, Self-Attention             | LLaMA/Qwen/GPT, multimodal, pre-training/fine-tuning/inference                                         |
| **Prompting and Orchestration**   | Prompt Engineering, Tool Calling, Skills            | Multi-turn dialogue, message templates, structured output, tool calling, skill-based capability accumulation                         |
| **Low-code Platforms**   | Coze, Dify                          | Workflows, Agents, knowledge bases, plugins, Python invocation, and localized deployment                             |
| **Development Frameworks**     | LangChain, LangGraph, DeepAgents            | Model I/O, Runnable / LCEL, Memory, Tools, Agents, graph-based workflows, multi-agent          |
| **Protocols and Communication**   | MCP (Model Context Protocol), A2A          | Function Calling, service decoupling, external tool integration, cross-Agent collaboration                          |
| **RAG and Retrieval**   | Vector databases, sparse retrieval, hybrid retrieval, BGE-Rerank  | Multi-route retrieval, reranking, knowledge graphs, RAGAS evaluation, advanced RAG optimization                            |
| **Documents and Multimodal** | MinerU, OCR                                 | Mixed text-image PDF parsing, device manuals, and after-sales guides                                            |
| **Deployment and Operations**   | Docker, Ollama, Xinference, vLLM            | Tencent Cloud/Alibaba Cloud, AutoDL, Coze local deployment                                             |
| **Fine-tuning and Training**   | PEFT, LoRA, QLoRA, DeepSpeed, Llama-Factory | Alpaca/ShareGPT data formats, Safetensors, keyword evaluation                                |
| **Programming and Tools**   | Python; Codex, Cursor                       | Primary language is Python; covers AI programming tools, Agent Skills, multi-model APIs, MCP integration and debugging      |
| **Job Search and Interview**   | Interview Question Bank                                    | Organized by job competency areas into **questions + answers**; aligned with similar **online training completion standards** and high-frequency **job posting** exam points |

---

## 🎯 What Will You Gain After Completing This?

- **Deployable project skills**, capable of independently delivering AI Agent applications (from environment setup to deployment), advancing from "only knowing how to call APIs" to engineering practices that can actually be put into production.
- **Systematic architectural articulation**, able to clearly explain the design and trade-offs of RAG, Agents, MCP, and more, and withstand follow-up questions in interviews and on resumes.
- **Interview and job posting alignment**, with a standalone [Interview Question Bank](AI%E6%99%BA%E8%83%BD%E4%BD%93%E4%B8%8E%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%E9%9D%A2%E8%AF%95%E9%A2%98%E5%BA%93.md), cross-linked with question numbers in the main text, organizing questions and answers by job competency areas, suitable for new graduates and career changers to consolidate their talking points.
- **Engineering and resume material**, with enterprise-oriented cases and terminology such as multi-route retrieval, observability, and cost, projects that can be demonstrated and written into resumes.
- **A searchable knowledge map**, with a systematic table of contents + case source code, aligned with the dimensions of common "Agent / Application Development" course outlines, making it easy to identify and fill gaps, and avoid the pitfall of "having only read articles but never run anything."
- **Clear job role alignment**, qualified for roles such as AI Application Development Engineer, AI Agent Engineer, AI Automation Process Developer, and AI Product Technical Lead; especially suitable for those with frontend / backend / product backgrounds transitioning into AI and Agent development.

---

## 📚 Tutorial Outline (Excerpt)

For complete navigation, see **[Tutorial Table of Contents](%E6%95%99%E7%A8%8B%E7%9B%AE%E5%BD%95%E5%A4%A7%E7%BA%B2.md)** and [online documentation](https://didilili.github.io/ai-agents-from-zero/#/).

> This outline is not a fixed table of contents. It will continue to evolve alongside the AI tech stack, with new core knowledge points, new frameworks, and new project practices being incorporated into this path.

### 01 Building Core LLM Capabilities

| Chapter Name                    | Content Summary                                                                         |
| --------------------------- | -------------------------------------------------------------------------------- |
| Understanding Large Language Models (LLMs) and Environment Preparation | Origins and development, relationship to AGI, characteristics and applicable scenarios of mainstream models, pre-training/fine-tuning/inference                   |
| LLM Architecture Principles              | Transformer, MoE, Self-Attention, LLaMA/Qwen/GPT, multimodal                               |
| LLM Scheduling Platforms              | Ollama, private model invocation, cloud/local deployment (AWS, Alibaba Cloud, etc.)                           |
| Prompt Engineering                  | Core principles and structure, Chain-of-Thought and Few-shot, multi-turn dialogue and memory, application in Agents and tool invocation |

### 02 Enterprise Low-Code Platform Development and Project Practice

| Chapter Name                  | Content Overview                                                                           |
| ------------------------- | ---------------------------------------------------------------------------------- |
| Coze Platform          | Interface and features, plugins/knowledge bases/workflows/agents, calling workflows from Python                           |
| Project 1: Merchant Operations Assistant      | Industry research PPT, viral video replication, marketing posters, selling point extraction, comment analysis                           |
| Dify AI Platform              | Workflows/Agents/knowledge bases, multiple cases (complaint classification, research reports, customer service analysis, comment analysis), Python invocation |
| Containerization Technology                | Docker core concepts, installation and common commands                                                    |
| Enterprise-grade LLM Deployment          | Tencent Cloud/Alibaba Cloud, Docker, Dify, AutoDL, Ollama, Xinference, Coze local deployment             |
| AI Coding Tool - Trae AI | Installation and usage, multi-model APIs, MCP integration                                                     |
| AI Coding Tool - Qoder   | Usage and debugging, project development                                                               |

### 03 Core LLM Development Frameworks

| Chapter Name                 | Content Overview                                                                    |
| ------------------------ | --------------------------------------------------------------------------- |
| LangChain Framework Principles and Applications | Model I/O, Prompt, Parser, Runnable / LCEL, Memory, Tools, Retrieval, Agent |
| LangGraph Framework Principles and Applications | Graph-based thinking, State/Node/Edge, persistent memory, streaming output, multi-agent and A2A             |
| MCP from Principles to Practice         | Comparison with Function Calling, communication mechanisms, workflow, Server deployment and custom development       |
| Cross-Agent Communication: A2A Protocol  | Relationship with MCP, messages and authentication, typical scenarios                                           |

### 04 Enterprise RAG / Agent Project Practice

| Chapter Name                                | Content Overview                                                                                                                                                                               |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Shopkeeper Knowledge Base                                | LangGraph RAG workflow, MinerU/OCR, vector+sparse+Neo4j multi-route retrieval, HyDE/BGE-Rerank, RAGAS evaluation                                                                                                |
| E-commerce Assistant                                | Intent parsing, multi-source knowledge bases, streaming replies, human handoff mechanism, conversation review, multi-channel and monitoring                                                                                                                     |
| [Shopkeeper Data Q&A](%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/0-%E5%89%8D%E8%A8%80.md) | Centered around natural language data querying, connecting a complete chain from MySQL data warehouse, metadata knowledge base, Qdrant vector retrieval, Elasticsearch field value retrieval, LangGraph workflow, SQL generation/validation/execution, FastAPI SSE, and frontend-backend integration                           |
| [Deep Research](%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E6%B7%B1%E5%BA%A6%E7%A0%94%E6%90%9C/0-%E5%89%8D%E8%A8%80.md) | Based on [DeepAgents](%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E6%B7%B1%E5%BA%A6%E7%A0%94%E6%90%9C/1-DeepAgents%E5%9F%BA%E7%A1%80%E4%B8%8E%E6%A0%B8%E5%BF%83%E6%A6%82%E5%BF%B5.md), build a multi-agent research system that connects web search, MySQL queries, RAGFlow knowledge base, file reading and generation, FastAPI APIs, and WebSocket real-time progress reporting |
| Market Compass                                | Scenario-based task decomposition, design and development from 0 to 1, stage goals and progress control, code review and results presentation                                                                                                           |

> **Recommended completed practical projects:**
>
> - [Shopkeeper Data Q&A](%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/0-%E5%89%8D%E8%A8%80.md)（[Source Repository](https://github.com/didilili/shopkeeper-agent)）：Not a simple SQL generation demo, but rather integrates `MySQL`、`LangGraph`、`Qdrant`、`Elasticsearch`、`FastAPI` and other knowledge points into a single runnable intelligent data query pipeline.
> - [Deep Research](%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E6%B7%B1%E5%BA%A6%E7%A0%94%E6%90%9C/0-%E5%89%8D%E8%A8%80.md)（[Source Repository](https://github.com/didilili/deepsearch-agents)）：Not an ordinary chat box, but rather a complete closed loop centered around open research tasks, combining main agent orchestration, sub-agent division of labor, multi-source material retrieval, file generation and delivery, and frontend-backend real-time interaction.

### 05 LLM Fine-tuning Practice

| Chapter                                                               | Content Overview                                                  |
| ------------------------------------------------------------------ | --------------------------------------------------------- |
| [28 Fine-tuning Overview](28-%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%BE%AE%E8%B0%83%E6%A6%82%E8%BF%B0%E4%B8%8E%E6%95%B4%E4%BD%93%E6%B5%81%E7%A8%8B.md)                      | Problem diagnosis, model types, baseline and keyword project workflow                  |
| [29 Data and Templates](29-%E5%BE%AE%E8%B0%83%E6%95%B0%E6%8D%AE%E5%87%86%E5%A4%87%E4%B8%8E%E5%AF%B9%E8%AF%9D%E6%A8%A1%E6%9D%BF.md)                      | Real JSONL, sample quality, cleaning and splitting, and conversation templates                  |
| [30 Training and Efficient Fine-tuning](30-%E6%A8%A1%E5%9E%8B%E8%AE%AD%E7%BB%83%E5%8E%9F%E7%90%86%E4%B8%8E%E9%AB%98%E6%95%88%E5%BE%AE%E8%B0%83.md)                  | Training parameters, VRAM calculation examples, LoRA and QLoRA                         |
| [31 LLaMA-Factory Fine-tuning Practice](31-LLaMA-Factory%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%E4%B8%8E%E5%BE%AE%E8%B0%83%E5%AE%9E%E6%88%98.md) | AutoDL single GPU / FP16, cleaned data training, logs and backups                |
| [32 Fine-tuning Effect Evaluation and Model Deployment](32-%E5%BE%AE%E8%B0%83%E6%95%88%E6%9E%9C%E8%AF%84%E4%BC%B0%E4%B8%8E%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md)          | Single-sample validation, 200-sample two-group prediction and scoring, export and standalone loading; vLLM optional |
| [33 Fine-tuning VRAM Optimization and Multi-GPU Training](33-%E5%BE%AE%E8%B0%83%E6%98%BE%E5%AD%98%E4%BC%98%E5%8C%96%E4%B8%8E%E5%A4%9A%E5%8D%A1%E8%AE%AD%E7%BB%83.md)          | Single-GPU VRAM troubleshooting, parallel division of labor, ZeRO and sprint log judgment               |

### 06 Major Tech Company Development Standards

| Chapter Name           | Content Overview                                                              |
| ------------------ | --------------------------------------------------------------------- |
| Enterprise LLM R&D Process | Technical research, solution and framework design, RAG and pipeline, evaluation and roles, project initiation and requirements documents |
| Current LLM Hot Topics     | Mainstream Agent/RAG technologies, cutting-edge and hot topic tracking                                    |

---

## 🏗️ Agent Project Architecture and Technical Architecture

![Agent Ecosystem Architecture Diagram](../../images/%E6%99%BA%E8%83%BD%E4%BD%93%E7%94%9F%E6%80%81%E6%9E%B6%E6%9E%84%E5%9B%BE.png)

---

<a id="quick-start"></a>

## 🚀 Quick Start

Use it together with the [online documentation](https://didilili.github.io/ai-agents-from-zero/#/). Want to get a case running right away? Follow these steps. For more detailed environment instructions, API applications, and common error handling, see [Getting Started and FAQ](%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8%E4%B8%8E%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.md).

1. **Clone the repository and enter the project directory**

   ```bash
   git clone https://github.com/didilili/ai-agents-from-zero.git
   cd ai-agents-from-zero
   ```

2. **Prepare the environment** (Python 3.10 recommended, supports 3.10–3.13)

   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate          # macOS/Linux
   # .venv\Scripts\activate           # Windows CMD
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   - Copy `.env-example` in the project root directory to `.env`
   - Fill in your API Key in `.env` (such as Qwen/Alibaba Bailian, DeepSeek, etc.), and the variable names must match the code (such as `aliQwen-api`, `QWEN_API_KEY`, `deepseek-api`)
   - For how to apply for keys on each platform, see [Getting Started and FAQ - How to Apply for API Keys on Each Platform](%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8%E4%B8%8E%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.md#_5、各-api-平台如何申请-key？)

4. **Run the first case in the project root directory**

   ```bash
   python 案例与源码-2-LangChain框架/01-helloworld/StandardDesc.py
   ```

   **Suggestion**: Run `python` in the **project root directory** for unified management of the virtual environment, dependencies, and output files. `load_dotenv()` in ordinary scripts usually automatically searches upward for `.env`; if you use an IDE, REPL, or debugger and cannot read the Key, please check its working directory configuration. If you do not want to use a cloud API, you can use [Ollama local models](%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8%E4%B8%8E%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.md#_54-不想用云-api：用本地-ollama（无需-key）) (no Key required).

If you encounter `ModuleNotFoundError`, API Key errors, cannot find `.env`, etc., please check [Getting Started and FAQ - Common Problems and Solutions](%E6%96%B0%E6%89%8B%E5%85%A5%E9%97%A8%E4%B8%8E%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.md#_6、常见问题与解决).

---

## 💬 Community

Want to discuss **AI programming, Agent / RAG practice, and interview experience** with more readers? Feel free to leave a comment on the [GitHub group application post](https://github.com/didilili/ai-agents-from-zero/issues/46) to apply to join the WeChat discussion group.

---

## 📖 About This Repository

- **Goal**: To create a **truly beginner-friendly, systematic, and continuously updated AI agent practical crash course**, which not only explains concepts clearly but also gets the cases running, taking you from zero to independently building **RAG / Agent / multi-agent** projects and articulating your own solutions and projects in engineering terms.
- **Technical Positioning**: Focus on the **Python agent development path**, with emphasis on **LangChain / LangGraph** and related engineering practices, **not following the Spring AI / langchain4j Java path**, making it more suitable for students who want to directly enter Python LLM application development.
- **Tutorial Source**: References **Shangguigu's "LLM Agent Crash Course"** and other course materials, and on this basis, combined with public documentation, community practices, and project experience, has been continuously **refactored, supplemented, and maintained**, gradually organized into a set of systematic learning materials for **Python agent application development**.
- **Interview Question Source**: A considerable portion of the question bank is compiled from **real interview questions from major tech companies**, public interview experiences, and high-frequency follow-up scenarios, and has been engineering-refactored in line with the chapter structure of this repository, making it more suitable for review from a project and system design perspective.
- **Content Composition**: **Systematic chapter notes** + **runnable case source code** + **[Interview Question Bank](AI%E6%99%BA%E8%83%BD%E4%BD%93%E4%B8%8E%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%E9%9D%A2%E8%AF%95%E9%A2%98%E5%BA%93.md)** (benchmarked against **comparable online training** and **social/campus recruitment JDs**).

---

## ⭐ Star History

![Star History Chart](https://api.star-history.com/image?repos=didilili/ai-agents-from-zero&type=date&legend=top-left)

---

**Repository English Name**: `ai-agents-from-zero` · **Repository Chinese Name**: 《AI Agent Practical Crash Course Guide: From Zero to Enterprise Deployment》
