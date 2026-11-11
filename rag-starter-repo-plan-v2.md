# rag-starter — Repo Blueprint v2 (Critical Revision)

> The fastest path from "I've heard of RAG" to "I use RAG at work every day" — no ML background required.

---

## Critical Review of v1

Before the improved plan, here's what was wrong with the first draft and what the competitive landscape reveals.

### What v1 got right

- Local-first default (genuine differentiator — most repos assume OpenAI keys)
- Progressive disclosure (three tiers)
- Workflow-first orientation (real problems, not academic demos)
- Expected output files (reduces beginner anxiety)

### What v1 got wrong

**1. Identity crisis: tutorial repo vs. framework vs. awesome-list**

v1 tried to be all three. It had tutorial-style walkthroughs, framework-like abstractions (config.yaml, pluggable backends), and reference-list energy (the "swap your stack" section). Repos that try to serve everyone serve no one. The competitive analysis makes this clear: NirDiamant's RAG_Techniques (26k+ stars) owns the "comprehensive technique catalogue" niche. LangChain's rag-from-scratch (official) owns "learn the framework." mrdbourke's simple-local-rag owns "one-file local pipeline." pguso's rag-from-scratch owns "understand internals with no frameworks."

**The gap is not another technique catalogue or framework tutorial.** The gap is: "I'm a PM/analyst/writer. I want RAG working on MY documents in 15 minutes and I want to understand enough to customise it."

**2. Too much surface area at launch**

Six workflows, two UIs, four tiers, an MCP server — that's a 3-month project before launch, not a v0.1. Repos gain stars by shipping something small that works perfectly, then expanding. v1's scope would delay launch indefinitely.

**3. LangChain dependency is a risk for beginners**

LangChain is powerful but notoriously unstable between versions, has heavy dependencies, and adds abstraction layers that obscure what's happening. For a repo whose principle is "explain decisions, not just steps," hiding RAG behind LangChain chains contradicts the mission. pguso's JS-based rag-from-scratch proved you can build everything with minimal dependencies and get better educational value.

**Revision:** Tier 1 should be zero-framework (raw Python + ChromaDB + Ollama). Tier 2 introduces LangChain/LlamaIndex as an upgrade path.

**4. The stack table was indecisive**

"LangChain (slim) or LlamaIndex" is exactly the kind of "or" that paralyzes beginners. The principle was "one golden path" but the table hedged. Same with "Unstructured / PyMuPDF" — pick one, footnote the other.

**5. Missing: the "bring your own docs" onramp**

The single most important user action is "I pointed this at MY files and got answers." v1 mentioned it in CUSTOMIZE.md but buried it. This should be front and centre — step 2 of the quickstart, not an appendix.

**6. Workflow selection was guesswork**

"Contract comparison" and "email digest" are niche. The first workflows should cover the broadest possible audience: personal notes/docs, work documents (PDF/DOCX), and a codebase. Everything else is v0.2+.

**7. Star projections were optimistic without a content flywheel**

100 stars in week 1 from a cold-start HN post is realistic only if the repo has a killer demo GIF, a companion blog post, and launches on a weekday morning US time. The plan listed growth levers but didn't sequence them into a launch checklist.

**8. No "zero-install" path**

Even with Ollama, setup requires Python, pip, and model downloads. For true beginners (analysts, writers), offering a Google Colab notebook as a zero-install entry point would dramatically widen the funnel. Multiple successful repos (NirDiamant, mrdbourke) use Colab as their primary onramp.

---

## Finalised Name: `rag-starter`

### Why this name wins

| Criterion | `rag-starter` | `rag-kickstart` | `everyday-rag` | `rag-for-humans` |
|---|---|---|---|---|
| Immediately clear intent | Yes — "starter" signals beginner-friendly | Yes but "kickstart" implies more effort | Less clear — sounds like a daily newsletter | Playful but vague |
| SEO/discoverability | "RAG starter" is a natural search query | "RAG kickstart" is less commonly searched | Weak — "everyday" is generic | Moderate |
| Avoids name collisions | No existing repo with this exact name | Multiple "kickstart" repos exist | Risk of collision with content brands | Low collision risk |
| Scales with maturity | "Starter" works even as repo grows (starter kit, starter pack) | "Kickstart" ages poorly as repo matures | Stays relevant | Gets awkward at scale |
| Memorable in conversation | "Just use rag-starter" | "Check out rag-kickstart" | "Try everyday-rag" | "Look at rag-for-humans" |

**Tagline:** "Your first RAG pipeline. Running in 15 minutes. On your own documents."

**GitHub topics:** `rag`, `retrieval-augmented-generation`, `ollama`, `beginner-friendly`, `local-llm`, `chromadb`, `ai-tools`

---

## Revised Design Principles

1. **Zero-framework first.** Tier 1 uses raw Python + ChromaDB + Ollama. No LangChain. No LlamaIndex. Every line of code is visible and explained. Frameworks are introduced in Tier 2 as an upgrade path, not a prerequisite.

2. **Working on YOUR docs in 15 minutes.** Step 1 runs a pre-loaded demo. Step 2 (immediately after) shows how to point it at a local folder. The "bring your own docs" moment is the product, not the demo.

3. **Local-first, cloud-optional, Colab-available.** Three entry points: (a) local with Ollama for power users, (b) Colab notebook for zero-install beginners, (c) API-key path for cloud LLM users. All three reach the same outcome.

4. **Ship small, expand weekly.** v0.1 launches with exactly one workflow (personal knowledge base), one UI (Streamlit), and one tutorial path. New workflows are added post-launch based on issues and community requests.

5. **Show the plumbing.** Every script includes a `--verbose` flag that prints what's happening at each RAG stage: loading → chunking → embedding → storing → retrieving → generating. Beginners need to see the pipeline, not just the output.

6. **Explain tradeoffs, not just choices.** Don't just say "we use ChromaDB." Say: "ChromaDB: zero config, works from pip install, stores everything in a local folder. Tradeoff: not suitable for millions of documents. When you outgrow it: see the Qdrant/Pinecone migration guide."

---

## Revised Default Stack

| Layer | Choice | Why this, not that |
|---|---|---|
| LLM (local) | Ollama + `llama3.1:8b` | One binary, one command (`ollama pull`). Runs on 8GB VRAM. Qwen alternative documented in FAQ. |
| LLM (cloud) | OpenAI `gpt-4o-mini` | Cheapest high-quality option. Anthropic Claude documented as alternative. Swap is a 1-line env var change. |
| Embeddings | `nomic-embed-text` via Ollama | Same Ollama binary handles both LLM and embeddings. No second model server. No API key. |
| Vector store | ChromaDB | `pip install chromadb`. No Docker. No account. File-based persistence. |
| Document loading | PyMuPDF (`pymupdf4llm`) | Handles PDF, the #1 format people want to search. Markdown/text handled natively. DOCX via `python-docx` (added as needed, not upfront). |
| Text splitting | Manual recursive splitter (50 lines) | No framework dependency. Beginner sees exactly how chunking works. LangChain splitter documented as alternative. |
| Interface | Streamlit | Single Python file. `pip install streamlit && streamlit run app.py`. No React, no build step. |
| Runtime | Python 3.10+ | 3.10 not 3.11 — widens compatibility, especially for Colab. |

### What's deliberately excluded from v0.1

- No LangChain/LlamaIndex (Tier 2)
- No Docker requirement
- No database server
- No TypeScript/Node path
- No multi-modal (images)
- No reranking
- No agentic RAG

Each of these becomes a clearly scoped addition in later versions.

---

## Revised Repository Structure

```
rag-starter/
├── README.md                         # The product — see README Strategy below
├── LICENSE (MIT)
├── CONTRIBUTING.md
├── CHANGELOG.md
│
├── quickstart/
│   ├── install.sh                    # macOS/Linux: installs Python deps + pulls Ollama model
│   ├── install.ps1                   # Windows PowerShell equivalent  
│   ├── requirements.txt              # Minimal: chromadb, pymupdf4llm, ollama, streamlit
│   ├── check.py                      # Health check: "✓ Python ✓ Ollama ✓ Model ✓ ChromaDB"
│   └── my_first_rag.py              # <80 lines. Loads sample docs, queries, prints answer.
│
├── bring-your-own-docs/
│   ├── README.md                     # "Point this at any folder and start asking questions"
│   ├── index_folder.py               # Indexes a local folder (PDF, MD, TXT)
│   ├── query.py                      # CLI: ask questions, get answers with source references
│   └── app.py                        # Streamlit UI wrapping the same pipeline
│
├── how-it-works/
│   ├── README.md                     # Visual walkthrough of the RAG pipeline
│   ├── 01-loading.md                 # What happens when you feed it a PDF
│   ├── 02-chunking.md                # Why we split documents and how
│   ├── 03-embedding.md               # What vectors are (without the math)
│   ├── 04-retrieval.md               # How similarity search finds relevant chunks
│   ├── 05-generation.md              # How the LLM uses retrieved context
│   └── architecture.svg              # Single visual: the full pipeline
│
├── guides/
│   ├── use-cloud-llm.md              # Swap Ollama for OpenAI/Anthropic (3 lines of code)
│   ├── use-langchain.md              # Same pipeline rebuilt with LangChain (Tier 2)
│   ├── use-llamaindex.md             # Same pipeline rebuilt with LlamaIndex (Tier 2)
│   ├── improve-results.md            # Practical tuning: chunk size, overlap, top-k, prompts
│   ├── add-docx-support.md           # Extending the loader for Word documents
│   └── migrate-vector-db.md          # When to move from ChromaDB to Qdrant/Pinecone
│
├── notebooks/
│   ├── rag_starter_colab.ipynb       # Zero-install: runs entirely in Google Colab
│   └── rag_starter_local.ipynb       # Jupyter version of the local pipeline
│
├── sample-docs/                      # 5-8 markdown files (public domain content)
│   ├── README.md                     # What these docs are and why they were chosen
│   ├── climate-basics.md
│   ├── remote-work-guide.md
│   ├── project-management-101.md
│   └── ...
│
├── reference/
│   ├── glossary.md                   # RAG jargon → plain English (25 terms max)
│   ├── troubleshooting.md            # Top 10 issues with solutions
│   └── faq.md                        # "Do I need a GPU?" "Can I use this at work?" etc.
│
├── tests/
│   ├── test_check.py                 # Verifies the health check works
│   ├── test_indexing.py              # Verifies document indexing
│   └── test_retrieval.py             # Verifies retrieval returns relevant results
│
└── .github/
    ├── workflows/ci.yml
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   ├── workflow_request.md        # "I want RAG for [use case]"
    │   └── beginner_question.md       # Low-barrier issue type
    └── PULL_REQUEST_TEMPLATE.md
```

### What changed from v1

- **Removed the numbered tier folders.** `00-setup`, `01-your-first-rag`, etc. felt like a bootcamp syllabus. Replaced with intent-based folders: `quickstart/`, `bring-your-own-docs/`, `how-it-works/`, `guides/`.
- **Removed `02-workflows/` with six sub-folders.** The "bring-your-own-docs" approach is the universal workflow. Specific use cases (meeting notes, research, contracts) become blog posts or community-contributed guides, not launch scope.
- **Added `notebooks/`.** The Colab notebook is the zero-install funnel that the v1 completely lacked.
- **Added `how-it-works/`.** Dedicated educational content separated from runnable code. This is what makes the repo more than a boilerplate generator.
- **Moved framework content to `guides/`.** LangChain and LlamaIndex are documented as upgrade paths, not the default.
- **Removed `04-build-your-own/` entirely.** MCP server, agentic RAG, production patterns — all post-v1.0 scope. Including them at launch is scope creep that delays shipping.

---

## README Strategy (Revised)

The README must convert a visitor into a star in under 60 seconds. Every element earns its place.

### Above the fold (first screen)

```
# rag-starter

Your first RAG pipeline. Running in 15 minutes. On your own documents.

[BADGE: Stars] [BADGE: License MIT] [BADGE: Python 3.10+] [BADGE: Open in Colab]

> Search your documents with AI — locally, privately, for free.
> No ML experience required. No API keys needed.

[GIF: 10-second demo showing a question asked → answer returned with source]
```

### Second screen

```
## Get started (pick your path)

🚀 **Fastest (zero install):** Open in Google Colab → [button]

💻 **Local (recommended):**
   git clone https://github.com/salahuddin-s/rag-starter && cd rag-starter
   pip install -r quickstart/requirements.txt
   ollama pull llama3.1:8b
   python quickstart/my_first_rag.py

☁️ **Cloud LLM:** Same steps, but set OPENAI_API_KEY and skip Ollama.
   See guides/use-cloud-llm.md
```

### Third screen

```
## Use it on YOUR documents

python bring-your-own-docs/index_folder.py ~/my-notes/
python bring-your-own-docs/query.py "What were the key decisions from last quarter?"

Or launch the visual interface:
streamlit run bring-your-own-docs/app.py
```

### Below the fold

- "How does it work?" → link to `how-it-works/`
- "Ready for more?" → link to `guides/`
- "Contributing" → link to CONTRIBUTING.md
- "FAQ" → link to `reference/faq.md`

### What the v1 README had that this removes

- No "What can I build with this?" grid (premature — there's one workflow at launch)
- No "I already know some of this" jump links (confusing for the target audience)
- No below-the-fold stack rationale (moved to `how-it-works/`)
- No star-history badge at launch (looks desperate on a new repo)

---

## The Colab Notebook: The Secret Growth Weapon

This is the single biggest omission in v1. Here's why it matters:

- **Zero friction.** No Python install, no Ollama, no terminal commands. Click a link, press "Run All," see RAG working.
- **Mobile-friendly discovery.** Someone sees the repo on their phone, clicks Colab, runs it during lunch break. Stars the repo.
- **Shareability.** "Hey, try this notebook" is easier to share than "clone this repo and install these dependencies."
- **Classroom adoption.** Instructors can assign it as a lab exercise. This is how mrdbourke's repo scaled.

The Colab notebook uses OpenAI or Groq (free tier) for the LLM and embeddings, since Ollama can't run in Colab. It should include:

1. A pre-loaded sample dataset
2. The same pipeline as the local version (same functions, same variable names)
3. A cell where users paste their own text or upload a file
4. Clear comments explaining every step

---

## Competitive Positioning Map

| Repo | Stars | Audience | Format | Local? | Our differentiation |
|---|---|---|---|---|---|
| NirDiamant/RAG_Techniques | 26k | ML engineers | Jupyter notebooks (technique catalogue) | No (OpenAI-dependent) | We're workflow-first, not technique-first. We solve "search my docs," they teach "how does HyDE work." |
| langchain-ai/rag-from-scratch | ~3k | LangChain users | Notebooks + video | No | We're framework-agnostic at Tier 1. We don't require learning LangChain first. |
| pguso/rag-from-scratch | ~1k | Developers (JS) | JavaScript modules | Yes | We're Python (bigger RAG ecosystem) and target non-developers. |
| mrdbourke/simple-local-rag | ~4k | ML learners | Notebooks | Yes | We're more opinionated (one path, not options) and ship a UI. |
| KalyanKS-NLP/rag-zero-to-hero | ~2k | ML students | Markdown + notebooks | Mixed | We focus on daily utility, not comprehensive coverage. |
| **rag-starter (ours)** | 0 (launch) | Knowledge workers, PMs, analysts, students | Scripts + UI + Colab | Yes (default) | Only repo optimised for non-engineers who want RAG on their own docs in 15 min. |

### Our unique claims (things no competitor does)

1. **"Bring your own docs" is step 2, not an afterthought.** Every other repo demos on pre-loaded data and leaves "use your own files" as an exercise.
2. **`--verbose` pipeline visibility.** No other beginner repo prints what each RAG stage is doing in real time.
3. **Three entry points (local / Colab / cloud).** Most repos force one path. We meet users where they are.
4. **A 25-term glossary written for non-engineers.** "Embedding" explained as "a way to turn text into a list of numbers that captures meaning, like GPS coordinates for ideas."
5. **Health check script.** `python check.py` tells you exactly what's missing before you hit a cryptic error.

---

## Launch Sequence (Revised)

v1 listed growth levers but didn't operationalize them. Here's the sequenced checklist:

### Pre-launch (Week -1)

- [ ] Repo is public with README, quickstart, bring-your-own-docs, how-it-works, Colab notebook
- [ ] GIF recorded showing the full quickstart flow (10 seconds)
- [ ] Blog post draft: "I built a personal knowledge base with RAG in 15 minutes — here's how"
- [ ] 10 issues created and labelled `good-first-issue` (typo fixes, add DOCX support, improve glossary entries, add a sample doc, translate a guide)
- [ ] Tested on macOS, Windows (PowerShell), Ubuntu, and Google Colab

### Launch day

- [ ] Post on r/LocalLLaMA (this community loves local-first AI tools)
- [ ] Post on r/LangChain and r/MachineLearning (cross-audience)
- [ ] Hacker News "Show HN" (weekday, ~10am EST for max visibility)
- [ ] Share on LinkedIn with the blog post
- [ ] Tweet thread with the GIF

### Week 1-2

- [ ] Respond to every issue and PR within 24 hours (signals active maintenance)
- [ ] Submit to awesome-rag, awesome-llm, awesome-ollama lists
- [ ] Post Colab link in relevant Discord servers (Ollama, ChromaDB, AI communities)

### Month 1

- [ ] Publish `guides/use-langchain.md` and `guides/use-llamaindex.md`
- [ ] Add first community-requested workflow as a guide
- [ ] Tag v0.2.0 release

### Month 2-3

- [ ] Add evaluation module (how to measure if RAG is working well)
- [ ] Add hybrid search guide
- [ ] Add MCP server guide (expose your RAG as a tool for Claude Desktop)
- [ ] Reach out to Ollama and ChromaDB teams for README mentions

### Star targets (revised — more conservative)

| Milestone | Timeline | Depends on |
|---|---|---|
| 50 stars | Week 1 | Reddit + HN launch lands |
| 200 stars | Month 1 | Blog post shared, Colab notebook circulates |
| 1,000 stars | Month 3 | Awesome-list inclusion + organic word-of-mouth |
| 3,000 stars | Month 6 | Becomes the default "start here" recommendation |
| 5,000+ stars | Year 1 | Community contributions, course/tutorial references |

---

## Revised Roadmap

| Version | Scope | Ship by |
|---|---|---|
| v0.1.0 | Quickstart + bring-your-own-docs + Streamlit UI + Colab notebook + how-it-works docs + glossary | Launch |
| v0.2.0 | LangChain guide + LlamaIndex guide + DOCX support + improve-results guide | Launch + 4 weeks |
| v0.3.0 | Evaluation module + hybrid search guide + chunk size experiments | Launch + 8 weeks |
| v0.4.0 | MCP server guide + agentic RAG guide + migration guides (Qdrant, Pinecone) | Launch + 12 weeks |
| v0.5.0 | Multi-modal (images + text) + community workflow contributions | Launch + 16 weeks |
| v1.0.0 | Stable interfaces, comprehensive tests, CI/CD, docs site, translations | Launch + 6 months |

---

## Content Quality Benchmarks

Every piece of content in the repo must pass these checks before merge:

1. **The copy-paste test.** Can someone with only Python installed copy the commands from the README and get a result? Test on a fresh machine.
2. **The jargon test.** Does any sentence use a term not defined in the glossary? If so, either define it or rewrite the sentence.
3. **The "so what" test.** Does every section answer "why should I care?" before "how does it work?"
4. **The 15-minute test.** Time the full quickstart from clone to first query. If it exceeds 15 minutes, something needs simplifying.
5. **The screenshot test.** Does every workflow have a visual showing what success looks like?

---

## TPM Portfolio Angle (Revised)

The v1 angle was solid but generic. Here's how to sharpen it:

- **Measurable product outcomes.** Track time-to-first-query (target: <15 min), Colab completion rate, and issue response time. These become portfolio metrics: "I reduced onboarding friction from 45 min to 12 min through three iterations of the quickstart flow."
- **Architecture Decision Records.** The `how-it-works/` folder doubles as ADR documentation. Every stack choice has a recorded "why this, not that" — this is exactly what JetBrains and FAANG interviewers ask about.
- **Community management as PM practice.** Issue triage, feature prioritisation based on community requests, release management, contributor onboarding — all legible PM work.
- **Cross-functional storytelling.** "I designed this for non-engineers" is a stronger narrative than "I built a RAG repo." It demonstrates user empathy and audience-aware product design.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Ollama has a breaking change | Medium | High (breaks quickstart) | Pin Ollama version in install script, test weekly |
| ChromaDB API changes | Medium | Medium | Pin version in requirements.txt, add migration notes |
| Someone launches a very similar repo | High | Medium | Ship first, ship with better docs, differentiate on "non-engineer" audience |
| Low engagement at launch | Medium | Low | Colab notebook provides a second launch vector; blog post provides a third |
| Scope creep delays launch | High | High | v0.1 scope is locked: quickstart + bring-your-own-docs + Colab. Nothing else merges before launch. |
| Sample docs have licensing issues | Low | High | Use only public domain or CC0 content. Write original sample docs if needed. |
