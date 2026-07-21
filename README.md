# FINESE SCHOOL — offline-first learning platform

Learn Python, AI, SQL, NoSQL, MCP, Power BI, Machine Learning, Deep Learning,
Data Visualization, 22+ Python libraries, and Git/GitHub — in depth, with
real code and real examples, entirely offline. Bring your own AI key any
time you want to go beyond the lesson.

Built with **Flask + Jinja templates + vanilla HTML/CSS/JS**. No React, no
build step, no external CDNs — open `app.py` and it just runs.

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000**.

That's it — every lesson is bundled into the app itself, so once a topic
page has loaded once, it keeps working with your Wi-Fi off.

## What's actually in here

- **12 core topics, 81 lessons total**: Python, AI, SQL, NoSQL, MCP,
  Power BI, Machine Learning, Deep Learning, Data Visualization, 22 Python
  libraries (NumPy through Pydantic), Git/GitHub, and a bonus Data
  Structures & Algorithms track.
- Every lesson has the same rich shape: a one-line hook, a real
  explanation (not a one-paragraph stub), a runnable code example, a
  real-world scenario, a best-practices list, a common-pitfalls list, and
  a set of **premade prompts** you can click to ask an AI assistant to go
  deeper on exactly that lesson.
- Each core topic gets its **own accent color** the moment you open it
  (see `src/content/registry.py` — one hex code per topic drives the
  whole page's theme via a CSS custom property).
- An optional **"AI Study Partner" panel** on every topic page lets a
  visitor paste their *own* API key and pick from **8 providers**
  (OpenAI, Anthropic, Google Gemini, Groq, Mistral, Cohere, Hugging Face,
  and Ollama for a fully local/offline model) to ask follow-up questions.
  Keys are sent straight from the browser to `/api/ask`, used once, and
  never written to disk — see `src/providers.py`.
- Reading progress is tracked per-lesson in the browser's `localStorage`
  (no account, no server-side tracking) and shown as a progress bar per
  topic and a percentage on each home page card.
- A print stylesheet means "Save as PDF" from the browser's print dialog
  produces a clean lesson document — no extra dependency like
  `wkhtmltopdf` required.

## Project structure

```
finese_school/
├── app.py                     Flask routes (pages + JSON API)
├── requirements.txt
├── .env.example
├── src/
│   ├── providers.py           Multi-provider AI dispatch (bring-your-own-key)
│   └── content/
│       ├── registry.py        The single source of truth: topic id, name,
│       │                      icon, color, description -> content module
│       ├── python_core.py     8 lessons
│       ├── ai_core.py         6 lessons
│       ├── sql_core.py        6 lessons
│       ├── nosql_core.py      6 lessons
│       ├── mcp_core.py        5 lessons
│       ├── powerbi_core.py    5 lessons
│       ├── ml_core.py         5 lessons
│       ├── dl_core.py         5 lessons
│       ├── dataviz_core.py    4 lessons
│       ├── pylibs_core.py     22 libraries
│       ├── git_core.py        5 lessons
│       └── dsa_core.py        4 lessons (bonus topic)
├── templates/
│   ├── base.html
│   ├── index.html             Home page: hero + topic grid
│   ├── topic.html             Single-page-per-topic lesson viewer
│   └── 404.html
└── static/
    ├── css/style.css          Whole design system, one file, no CDN
    └── js/app.js              Lesson switching, progress, AI panel — vanilla JS
```

## Adding a new lesson or topic

Every lesson is a plain Python `dict` — no build step, no database
migration, just edit a file and refresh:

```python
dict(
    id="unique-slug",
    title="Lesson Title",
    hook="One punchy sentence that sells why this matters.",
    explanation="Paragraph one.\n\nParagraph two. Use `backticks` for inline code.",
    code=dict(lang="python", label="What this snippet shows", src="print('hi')"),
    example="A real-world scenario where this applies.",
    best_practices=["Do this.", "And this."],
    pitfalls=["Watch out for this."],
    prompts=["A question a learner could ask an AI to go deeper."],
)
```

Add it to the right `SUBTOPICS` list in `src/content/*_core.py`, and it
appears automatically — the sidebar, the progress tracker, and the AI
panel all read from that one list.

To add a brand-new *topic*, create `src/content/<name>_core.py` with a
`SUBTOPICS` list in the same shape, import it and add one entry to the
`TOPICS` list in `src/content/registry.py` (pick a hex color and an
emoji icon) — nothing else needs to change.

## The AI assistant, honestly

The lessons themselves need no AI and no internet. The AI panel is a
genuinely optional layer on top, for when a learner has a question the
pre-written lesson doesn't answer. It:

- Never requires a key from you as the operator — there's nothing to
  configure server-side, and no shared/company API key is baked in.
- Sends the visitor's key directly to the provider they picked, per
  request, and does not log or persist it anywhere (`src/providers.py`
  keeps it in a local variable for the duration of one function call).
- Supports **Ollama** as a provider with `needs_key: False` — if a
  learner has Ollama running locally, the AI panel works with zero
  internet connection and zero API key, matching the platform's
  offline-first philosophy end to end.

## Deploying

For anything beyond local use, run behind a real WSGI server instead of
Flask's dev server:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Set `FLASK_DEBUG=0` (the default when using gunicorn directly) — Flask's
debugger must never be enabled on a publicly reachable deployment.

## What this intentionally does *not* include yet

This is a v1 content set, not a claim that every one of these topics is
exhaustively finished — each core topic currently has 4-8 deep lessons
(81 total), which is enough to genuinely learn the fundamentals of every
listed subject, but a subject like SQL or Machine Learning could easily
support another 20 lessons each. The architecture is built so that's just
more entries in a Python list, not a redesign — tell me which topic to
go deeper on next and I'll extend it in the same format.
