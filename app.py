"""
FINESE SCHOOL v2 — Flask entry point.

Routes:
  GET  /                          Home: grid of every core topic
  GET  /topic/<topic_id>          A topic's single-page notebook (all its
                                   subtopics, pre-loaded, fully offline)
  GET  /api/topics                JSON registry (used by the frontend + handy for testing)
  POST /api/ask                   Optional "online AI assistant" — bring your own key
  GET  /api/providers              JSON list of supported AI providers/models
  GET  /api/health                 Simple health check
"""

import os
from flask import Flask, render_template, jsonify, request, abort

from src.content import registry
from src import providers

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    topics = registry.TOPICS
    return render_template(
        "index.html",
        topics=topics,
        total_subtopics=registry.total_subtopic_count(),
    )


@app.route("/topic/<topic_id>")
def topic_page(topic_id):
    topic = registry.get_topic(topic_id)
    if not topic:
        abort(404)
    subtopics = registry.get_subtopics(topic_id)
    return render_template(
        "topic.html",
        topic=topic,
        subtopics=subtopics,
        all_topics=registry.TOPICS,
        providers=providers.PROVIDERS,
    )


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", all_topics=registry.TOPICS), 404


# ---------------------------------------------------------------------------
# JSON API
# ---------------------------------------------------------------------------

@app.route("/api/topics")
def api_topics():
    return jsonify([
        {
            "id": t["id"],
            "name": t["name"],
            "icon": t["icon"],
            "color": t["color"],
            "tagline": t["tagline"],
            "description": t["description"],
            "subtopic_count": len(t["module"].SUBTOPICS),
        }
        for t in registry.TOPICS
    ])


@app.route("/api/providers")
def api_providers():
    return jsonify(providers.PROVIDERS)


@app.route("/api/health")
def api_health():
    return jsonify(status="ok", topics=len(registry.TOPICS), subtopics=registry.total_subtopic_count())


@app.route("/api/ask", methods=["POST"])
def api_ask():
    """
    Bring-your-own-key AI assistant. The key travels from the browser to
    this endpoint with the request and is used once, in memory, to call
    the chosen provider — it is never written to disk or logged.
    """
    data = request.get_json(silent=True) or {}

    provider = (data.get("provider") or "").strip()
    model = (data.get("model") or "").strip()
    api_key = (data.get("api_key") or "").strip()
    question = (data.get("question") or "").strip()
    topic_id = (data.get("topic_id") or "").strip()
    subtopic_id = (data.get("subtopic_id") or "").strip()
    socratic = bool(data.get("socratic", False))

    if not question:
        return jsonify(error="Ask something first — the question field is empty."), 400
    if provider not in providers.PROVIDERS:
        return jsonify(error=f"Unknown provider '{provider}'."), 400

    topic = registry.get_topic(topic_id)
    topic_name = topic["name"] if topic else "General"
    subtopic = registry.get_subtopic(topic_id, subtopic_id) if topic else None
    subtopic_title = subtopic["title"] if subtopic else None

    system_prompt = providers.build_system_prompt(topic_name, subtopic_title, socratic)

    try:
        answer = providers.ask(provider, api_key, model, system_prompt, question)
    except providers.ProviderError as e:
        return jsonify(error=str(e)), 502

    return jsonify(answer=answer)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
