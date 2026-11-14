![EduGraphIQ](https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1f6feb,100:8957e5&height=180&section=header&text=EduGraphIQ&fontSize=42&fontColor=ffffff&animation=fadeIn)

<div align="center">

**Upload a study PDF. Watch it turn into a map of ideas — then ask the map questions.**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![Neo4j](https://img.shields.io/badge/Neo4j-4581C3?logo=neo4j&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama%203-F55036)

![Status](https://img.shields.io/badge/Status-Hackathon%20Build-orange)
![Era](https://img.shields.io/badge/Built-April%202025-blueviolet)

</div>

> *"A textbook is a list. Understanding is a graph. EduGraphIQ tries to turn the first into the second."*

---

## 📖 The Story

April 2025. A student, a pile of academic PDFs, and a GraphRAG hackathon deadline — the footer of this project's own homepage still says it plainly: *"Project by M S Abhishek & Team for GraphRAG Hackathon."*

The frustration behind it was specific: a 200-page PDF tells you everything in order, but an exam never asks in order. It asks how Chapter 3 connects to Chapter 9. So instead of building one more PDF summariser, this project asked a different question — **what if the PDF could draw you its own concept map?**

In two days of commits (14–15 April 2025), the experiment took shape: feed in an academic PDF, let an LLM pull out how concepts relate to each other, draw that as a graph you can actually explore, store the concepts in a real graph database, and bolt on a tutor chatbot that answers from the document you uploaded — not from the open internet.

It is a hackathon build, with hackathon edges. But the idea at its centre — *learn the connections, not just the pages* — is the same idea that later grew into the wider VidyaSathi family.

---

## 🎯 The Problem

- 📄 Study material arrives as flat PDFs — sequential, dense, and connection-blind.
- 🧠 Students memorise definitions but miss how concepts depend on each other, which is exactly what exams and vivas test.
- 🔍 Searching a PDF finds a word, not an idea. There is no map of *"learn this before that."*
- 💬 Generic chatbots answer from general knowledge, not from **your** syllabus, **your** notes, **your** PDF.

---

## 👥 Who It's For

- 🎓 **Students** staring at a long academic PDF the night before an exam, who need the structure before the details.
- 👩‍🏫 **Teachers and tutors** who want a quick visual skeleton of a chapter before teaching it.
- 🧑‍💻 **Builders curious about GraphRAG** — this is a small, readable example of LLM-driven concept extraction feeding a graph database.

---

## ✨ What It Does

*Everything below is taken from the code actually in this repository.*

- 📤 **PDF upload (Flask web app)** — `app.py` / `run.py` serve a Flask app (`templates/index.html`, titled *"EduGraphIQ – Smart Learning Assistant"*) where you upload an academic PDF to generate a knowledge graph.
- 🧩 **LLM concept extraction** — `main.py` loads a PDF with LangChain's `PyPDFLoader` (first 10 pages), splits it into 700-character chunks, and prompts Groq's **Llama 3 8B** to return concept relationships in the form `Concept A -> Concept B`.
- 🕸️ **A graph you can see two ways** — the extracted pairs are built into a NetworkX directed graph, drawn statically with Matplotlib and interactively with PyVis (`graph_interactive.html`).
- 🗄️ **Graph database storage** — `database/neo4j_connection.py` connects to **Neo4j Aura** and stores concepts as `:Concept` nodes joined by `:RELATED_TO` relationships, with helpers to create nodes, link concepts, and fetch them back.
- 💬 **A tutor that answers from your PDF** — `chatbot.py` takes a question plus the uploaded document's text and answers as a *"smart AI tutor helping students understand their study material"* (Groq, temperature 0.2 for grounded answers). Upload first, then ask — if no PDF is loaded, the app honestly replies *"Please upload a PDF first."*
- 🧪 **A second, lighter extraction path** — `app/routes.py` exposes an `/upload` endpoint that parses PDFs with PyMuPDF and pulls out up to 10 candidate concepts, showing the team experimenting with a non-LLM route alongside the main one.

---

## 🔑 USP

> **It doesn't summarise your PDF. It maps it.**

Summaries shrink text. EduGraphIQ restructures it — concepts become nodes, relationships become edges, and the result is stored in Neo4j as a queryable graph, not just drawn once and thrown away. The chatbot is grounded in the same uploaded document, so the map and the answers come from *your* material.

---

## 🛠️ Tech Stack

| Layer | Technology (verified in repo) |
|---|---|
| Language | Python |
| Web framework | Flask (`app.py`, `app/routes.py`, `run.py`) |
| LLM | Groq — Llama 3 8B (`llama3-8b-8192`) via LangChain (`langchain`, `langchain-community`) |
| PDF parsing | PyPDFLoader / PyPDF2, plus PyMuPDF (`fitz`) in the routes variant |
| Graph building | NetworkX (directed graph), Matplotlib (static), PyVis (interactive HTML) |
| Graph database | Neo4j Aura (`neo4j` driver, `database/neo4j_connection.py`, `test_neo4j.py`) |
| Text processing | NLTK (`punkt`) in `app/routes.py` |
| Config | `python-dotenv`, `.env` |

*Honest note: `requirements.txt` lists flask, PyPDF2, neo4j, python-dotenv, langchain, langchain-community and werkzeug — a few libraries the code also uses (groq, networkx, pyvis, PyMuPDF, nltk) aren't in it yet. See Future Plans.*

---

## 🚀 Future Plans

- 🔐 Move every API key and database credential into environment variables — the hackathon code hardcodes some of them, and rotating + removing them is step zero before any public revival.
- 📦 Complete `requirements.txt` so the project installs in one command.
- 🔗 Merge the two parallel extraction paths (the LangChain/Groq pipeline and the PyMuPDF route) into one clean flow.
- 🎯 Let users click a concept node and ask the tutor about *that concept specifically*.
- 📚 Support multi-PDF subjects, so a whole unit becomes one connected graph.

---

## 🔗 More

- 👤 Author profile: [github.com/MSAbhishek22](https://github.com/MSAbhishek22)
- 📚 The project this idea grew alongside: [VidyaSathi](https://github.com/MSAbhishek22/vidyasathi)

<div align="center">

*Built for a GraphRAG Hackathon, April 2025 — a small graph with a big idea: learn the connections.*

</div>

![footer](https://capsule-render.vercel.app/api?type=waving&color=0:8957e5,50:1f6feb,100:0d1117&height=120&section=footer)
