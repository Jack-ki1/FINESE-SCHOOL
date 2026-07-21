/* =========================================================================
   FINESE SCHOOL — app.js
   Vanilla JS, no build step, no frameworks. Runs on every page; each
   section below checks whether its DOM exists before doing anything,
   so this one file safely powers both index.html and topic.html.
   ========================================================================= */

(function () {
  "use strict";

  const PROGRESS_KEY = "finese_progress_v1";

  // -----------------------------------------------------------------------
  // Small helpers
  // -----------------------------------------------------------------------

  function escapeHtml(str) {
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  // Turns `inline code` markers in plain text into <code> tags, safely
  // (escapes everything else first, so no other HTML can leak in).
  function renderInlineCode(text) {
    const escaped = escapeHtml(text);
    return escaped.replace(/`([^`]+)`/g, "<code>$1</code>");
  }

  function loadProgress() {
    try {
      return JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}");
    } catch (e) {
      return {};
    }
  }

  function saveProgress(progress) {
    try {
      localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
    } catch (e) {
      /* localStorage unavailable (private browsing, etc.) — fail silently */
    }
  }

  function markRead(topicId, subtopicId) {
    const progress = loadProgress();
    if (!progress[topicId]) progress[topicId] = [];
    if (!progress[topicId].includes(subtopicId)) {
      progress[topicId].push(subtopicId);
      saveProgress(progress);
    }
    return progress;
  }

  function readCountFor(topicId) {
    const progress = loadProgress();
    return (progress[topicId] || []).length;
  }

  // -----------------------------------------------------------------------
  // Online / offline badges (present on every page)
  // -----------------------------------------------------------------------

  function updateNetBadge(el) {
    if (!el) return;
    const label = el.querySelector(".net-label");
    if (navigator.onLine) {
      el.classList.add("is-online");
      el.classList.remove("is-offline");
      if (label) label.textContent = "Online";
    } else {
      el.classList.add("is-offline");
      el.classList.remove("is-online");
      if (label) label.textContent = "Offline — lessons still work";
    }
  }

  function initNetBadges() {
    const badges = [
      document.getElementById("global-net-badge"),
      document.getElementById("ai-net-badge"),
    ].filter(Boolean);
    const refresh = () => badges.forEach(updateNetBadge);
    refresh();
    window.addEventListener("online", refresh);
    window.addEventListener("offline", refresh);
  }

  // -----------------------------------------------------------------------
  // Home page: per-topic progress percentage
  // -----------------------------------------------------------------------

  function initHomeProgress() {
    const rings = document.querySelectorAll(".topic-card-progress-ring[data-topic]");
    if (!rings.length) return;
    rings.forEach((ring) => {
      const topicId = ring.getAttribute("data-topic");
      const total = parseInt(ring.getAttribute("data-total"), 10) || 0;
      const read = readCountFor(topicId);
      const pct = total > 0 ? Math.round((read / total) * 100) : 0;
      const label = ring.querySelector(".progress-pct");
      if (label) label.textContent = pct + "%";
    });
  }

  // -----------------------------------------------------------------------
  // Topic page: lesson rendering + navigation
  // -----------------------------------------------------------------------

  function initTopicPage() {
    const shell = document.querySelector(".topic-shell");
    if (!shell) return;

    const topicId = shell.getAttribute("data-topic-id");
    const subtopics = JSON.parse(document.getElementById("subtopics-data").textContent || "[]");
    const providers = JSON.parse(document.getElementById("providers-data").textContent || "{}");
    const topicMeta = JSON.parse(document.getElementById("topic-meta").textContent || "{}");

    const contentEl = document.getElementById("lesson-content");
    const navItems = Array.from(document.querySelectorAll(".lesson-nav-item"));
    const progressFill = document.getElementById("topic-progress-fill");
    const progressLabel = document.getElementById("topic-progress-label");

    let currentIndex = 0;

    function subtopicById(id) {
      return subtopics.find((s) => s.id === id);
    }

    function renderLesson(subtopic, index) {
      const paragraphs = (subtopic.explanation || "")
        .split(/\n\n+/)
        .map((p) => `<p class="body-p">${renderInlineCode(p)}</p>`)
        .join("");

      const bestPractices = (subtopic.best_practices || [])
        .map((b) => `<li>${renderInlineCode(b)}</li>`)
        .join("");

      const pitfalls = (subtopic.pitfalls || [])
        .map((p) => `<li>${renderInlineCode(p)}</li>`)
        .join("");

      const promptChips = (subtopic.prompts || [])
        .map((p) => `<button class="prompt-chip" type="button">${escapeHtml(p)}</button>`)
        .join("");

      const code = subtopic.code || {};
      const codeBlock = code.src
        ? `
        <div class="code-block">
          <div class="code-head">
            <span>${escapeHtml(code.label || code.lang || "example")}</span>
            <button class="copy-btn" type="button">Copy</button>
          </div>
          <pre><code>${escapeHtml(code.src)}</code></pre>
        </div>`
        : "";

      const exampleBlock = subtopic.example
        ? `
        <div class="example-box">
          <strong>Real-world example</strong>
          <p>${renderInlineCode(subtopic.example)}</p>
        </div>`
        : "";

      const prevBtn = index > 0
        ? `<button class="btn" type="button" data-nav="prev">← ${escapeHtml(subtopics[index - 1].title)}</button>`
        : `<span></span>`;
      const nextBtn = index < subtopics.length - 1
        ? `<button class="btn btn-primary" type="button" data-nav="next">${escapeHtml(subtopics[index + 1].title)} →</button>`
        : `<span></span>`;

      contentEl.innerHTML = `
        <article class="lesson">
          <h2>${escapeHtml(subtopic.title)}</h2>
          ${subtopic.hook ? `<p class="lesson-hook">${renderInlineCode(subtopic.hook)}</p>` : ""}
          ${paragraphs}
          ${codeBlock}
          ${exampleBlock}
          <div class="two-col">
            <div class="best-practices">
              <h3>✅ Best practices</h3>
              <ul>${bestPractices || "<li>—</li>"}</ul>
            </div>
            <div class="pitfalls">
              <h3>⚠️ Common pitfalls</h3>
              <ul>${pitfalls || "<li>—</li>"}</ul>
            </div>
          </div>
          ${promptChips ? `
          <div class="prompts-box">
            <h3>🎯 Go deeper — premade prompts for the AI panel</h3>
            <div class="prompt-chips">${promptChips}</div>
          </div>` : ""}
          <div class="lesson-nav-footer">${prevBtn}${nextBtn}</div>
        </article>
      `;

      // Copy button
      const copyBtn = contentEl.querySelector(".copy-btn");
      if (copyBtn && code.src) {
        copyBtn.addEventListener("click", async () => {
          try {
            await navigator.clipboard.writeText(code.src);
            copyBtn.textContent = "Copied";
            copyBtn.classList.add("is-copied");
            setTimeout(() => {
              copyBtn.textContent = "Copy";
              copyBtn.classList.remove("is-copied");
            }, 1400);
          } catch (e) {
            /* clipboard API unavailable — no-op */
          }
        });
      }

      // Premade prompt chips -> fill the AI question box
      contentEl.querySelectorAll(".prompt-chip").forEach((chip) => {
        chip.addEventListener("click", () => {
          const questionEl = document.getElementById("ai-question");
          if (questionEl) {
            questionEl.value = chip.textContent;
            questionEl.focus();
            questionEl.scrollIntoView({ behavior: "smooth", block: "center" });
          }
        });
      });

      // Prev/next lesson buttons
      contentEl.querySelectorAll("[data-nav]").forEach((btn) => {
        btn.addEventListener("click", () => {
          const dir = btn.getAttribute("data-nav");
          selectLesson(dir === "next" ? index + 1 : index - 1);
        });
      });

      window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
    }

    function updateProgressUI() {
      const progress = loadProgress();
      const readIds = progress[topicId] || [];
      const pct = subtopics.length ? Math.round((readIds.length / subtopics.length) * 100) : 0;
      if (progressFill) progressFill.style.width = pct + "%";
      if (progressLabel) progressLabel.textContent = `${readIds.length} / ${subtopics.length} read`;
      navItems.forEach((item) => {
        const id = item.getAttribute("data-subtopic-id");
        const check = item.querySelector(".lesson-check");
        if (check) check.classList.toggle("is-done", readIds.includes(id));
      });
    }

    function selectLesson(index) {
      if (index < 0 || index >= subtopics.length) return;
      currentIndex = index;
      const subtopic = subtopics[index];
      renderLesson(subtopic, index);
      navItems.forEach((item) => {
        item.classList.toggle("is-active", item.getAttribute("data-subtopic-id") === subtopic.id);
      });
      markRead(topicId, subtopic.id);
      updateProgressUI();
    }

    navItems.forEach((item, i) => {
      item.addEventListener("click", () => selectLesson(i));
    });

    updateProgressUI();
    if (subtopics.length) selectLesson(0);

    // -----------------------------------------------------------------
    // AI assistant panel
    // -----------------------------------------------------------------
    initAiPanel(topicId, topicMeta, providers, () => subtopics[currentIndex]);
  }

  // -----------------------------------------------------------------------
  // AI assistant panel logic (topic page only)
  // -----------------------------------------------------------------------

  function initAiPanel(topicId, topicMeta, providers, getCurrentSubtopic) {
    const providerSelect = document.getElementById("provider-select");
    const modelSelect = document.getElementById("model-select");
    const apiKeyField = document.getElementById("api-key-field");
    const apiKeyInput = document.getElementById("api-key-input");
    const socraticToggle = document.getElementById("socratic-toggle");
    const chatEl = document.getElementById("ai-chat");
    const questionEl = document.getElementById("ai-question");
    const sendBtn = document.getElementById("ai-send");

    if (!providerSelect || !modelSelect) return;

    function populateModels() {
      const pid = providerSelect.value;
      const info = providers[pid] || { models: [], needs_key: true };
      modelSelect.innerHTML = info.models
        .map((m) => `<option value="${escapeHtml(m)}">${escapeHtml(m)}</option>`)
        .join("");
      apiKeyField.style.display = info.needs_key ? "" : "none";
    }

    providerSelect.addEventListener("change", populateModels);
    populateModels();

    function appendMessage(role, text) {
      const div = document.createElement("div");
      div.className = "ai-msg ai-msg-" + role;
      div.textContent = text;
      chatEl.appendChild(div);
      chatEl.scrollTop = chatEl.scrollHeight;
      return div;
    }

    async function sendQuestion() {
      const question = (questionEl.value || "").trim();
      if (!question) return;

      const provider = providerSelect.value;
      const model = modelSelect.value;
      const apiKey = apiKeyInput.value.trim();
      const needsKey = (providers[provider] || {}).needs_key;

      if (needsKey && !apiKey) {
        appendMessage("error", `${providers[provider].label} needs an API key — paste yours above first.`);
        return;
      }
      if (!navigator.onLine && provider !== "ollama") {
        appendMessage("error", "You're offline. Switch to Ollama (local) or reconnect to the internet.");
        return;
      }

      appendMessage("user", question);
      questionEl.value = "";
      sendBtn.disabled = true;
      const pending = appendMessage("pending", "Thinking…");

      const subtopic = getCurrentSubtopic ? getCurrentSubtopic() : null;

      try {
        const resp = await fetch("/api/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            provider,
            model,
            api_key: apiKey,
            question,
            topic_id: topicId,
            subtopic_id: subtopic ? subtopic.id : "",
            socratic: !!socraticToggle.checked,
          }),
        });
        const data = await resp.json();
        pending.remove();
        if (!resp.ok) {
          appendMessage("error", data.error || "Something went wrong.");
        } else {
          appendMessage("assistant", data.answer);
        }
      } catch (e) {
        pending.remove();
        appendMessage("error", "Network error reaching the server. Are you offline?");
      } finally {
        sendBtn.disabled = false;
      }
    }

    sendBtn.addEventListener("click", sendQuestion);
    questionEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendQuestion();
      }
    });
  }

  // -----------------------------------------------------------------------
  // Boot
  // -----------------------------------------------------------------------

  document.addEventListener("DOMContentLoaded", () => {
    initNetBadges();
    initHomeProgress();
    initTopicPage();
  });
})();
