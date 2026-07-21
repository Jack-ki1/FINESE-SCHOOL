"""Artificial Intelligence foundations subtopics."""

SUBTOPICS = [
    dict(
        id="what-is-ai",
        title="What Is Artificial Intelligence?",
        hook="AI is a moving target by definition — every time a capability becomes routine, people stop calling it AI and start calling it software.",
        explanation=(
            "Artificial Intelligence is the broad field of building systems that perform tasks which normally "
            "require human-like judgment: recognizing images, understanding language, planning, or making "
            "decisions under uncertainty. It's an umbrella term, not a single technique — a chess engine using "
            "hand-coded rules from the 1990s and a modern language model trained on billions of documents are both "
            "'AI', despite having almost nothing in common under the hood.\n\n"
            "Practically, AI systems fall into two very different categories: narrow AI, which is extremely good at "
            "one task and has no capability outside it (spam filters, recommendation engines, image classifiers), "
            "and the hypothetical general AI (AGI), which would match human-level reasoning across arbitrary "
            "tasks. Every AI system in production today, including the largest language models, is narrow AI — "
            "impressively broad in what it can talk about, but not what researchers mean by 'general'."
        ),
        code=dict(
            lang="python",
            label="A trivially 'narrow AI' rule-based system, for contrast",
            src=(
                "# Not machine learning at all — but historically this counted as AI\n"
                "def is_spam(email_text: str) -> bool:\n"
                "    spam_signals = ['win a free', 'click here now', 'act immediately']\n"
                "    text = email_text.lower()\n"
                "    return any(signal in text for signal in spam_signals)\n\n"
                "print(is_spam('Click here now to win a free iPhone!'))  # True"
            ),
        ),
        example=(
            "A hospital triage tool that flags high-risk patients from vitals is 'AI' in the same sense a large "
            "language model is — both are software making judgment calls a human used to make alone — even though "
            "one might be a simple decision tree and the other a billion-parameter neural network."
        ),
        best_practices=[
            "When someone says 'AI', ask what technique is actually underneath — rules, classical ML, or deep learning.",
            "Treat 'AGI' and 'AI' as different claims; almost everything shipped today is narrow AI.",
            "Judge an AI system by its evaluation results on real data, not by how impressive its demos look.",
        ],
        pitfalls=[
            "Assuming every AI system 'understands' — most are pattern-matchers, however sophisticated.",
            "Conflating a chatbot being fluent in language with it being reliably correct.",
        ],
        prompts=[
            "What's the real difference between AI, machine learning, and deep learning?",
            "Give three examples of narrow AI I use every day without noticing.",
            "Why is AGI still considered unsolved even with today's large language models?",
        ],
    ),
    dict(
        id="ai-ml-dl-hierarchy",
        title="AI vs ML vs DL: The Hierarchy",
        hook="These three terms nest inside each other like Russian dolls, and mixing them up is the single most common AI vocabulary mistake.",
        explanation=(
            "Artificial Intelligence is the outermost category: any system that mimics intelligent behavior, "
            "including hand-coded rules with no learning involved at all. Machine Learning is a subset of AI where "
            "the system learns patterns from data instead of following rules a human wrote — a spam filter that "
            "improves by seeing labeled examples of spam is ML; the earlier keyword-matching version was not.\n\n"
            "Deep Learning is a subset of ML that specifically uses neural networks with multiple layers "
            "('deep' refers to layer count, not intelligence) to learn hierarchical representations — early layers "
            "learn edges and simple patterns, later layers combine them into faces, words, or concepts. Every deep "
            "learning system is machine learning, and every machine learning system is AI, but the reverse isn't "
            "true — a linear regression model is ML but not deep learning, and a rule-based expert system is AI "
            "but not ML at all."
        ),
        code=dict(
            lang="python",
            label="Classical ML (not deep learning) still counts as ML",
            src=(
                "from sklearn.linear_model import LogisticRegression\n"
                "from sklearn.datasets import load_breast_cancer\n\n"
                "X, y = load_breast_cancer(return_X_y=True)\n"
                "model = LogisticRegression(max_iter=5000)\n"
                "model.fit(X, y)\n"
                "print('Accuracy:', model.score(X, y))\n"
                "# This is ML — it learned from data — but it's not deep learning:\n"
                "# there's no neural network or multiple learned layers here."
            ),
        ),
        example=(
            "A bank's fraud detection system might use a gradient-boosted tree (ML, not deep learning) for "
            "transaction scoring while its customer-support chatbot uses a transformer-based language model "
            "(deep learning) — both are 'AI', but at very different layers of the same hierarchy."
        ),
        best_practices=[
            "When evaluating a vendor's 'AI-powered' claim, ask specifically whether it's rules, classical ML, or deep learning.",
            "Reach for classical ML first on structured/tabular data — it's often more accurate and interpretable than deep learning there.",
            "Reserve deep learning for problems with unstructured data: images, audio, text, and complex sequences.",
        ],
        pitfalls=[
            "Assuming 'deep learning' is always the better or more advanced choice — it isn't, for structured data.",
            "Using 'AI' and 'machine learning' interchangeably when writing technical documentation.",
        ],
        prompts=[
            "Give a concrete example of a task where classical ML beats deep learning.",
            "Why does 'deep' in deep learning refer to layers, not smartness?",
            "Where does reinforcement learning fit into this hierarchy?",
        ],
    ),
    dict(
        id="neural-networks-101",
        title="Neural Networks 101",
        hook="A neural network is just weighted sums and nonlinear functions, stacked and trained until the weights encode something useful.",
        explanation=(
            "At its simplest, a neural network is a chain of layers, each made of neurons that compute a weighted "
            "sum of their inputs, add a bias, and pass the result through a nonlinear activation function (like "
            "ReLU or sigmoid). Without the nonlinearity, stacking layers would collapse mathematically into a "
            "single linear function — the nonlinearity is what lets the network model curved, complex decision "
            "boundaries instead of only straight lines.\n\n"
            "Training a network means adjusting every weight so the network's output gets closer to the correct "
            "answer, using a loss function to measure how wrong it currently is, and backpropagation with gradient "
            "descent to figure out which direction to nudge each weight. This happens over many passes through the "
            "training data (epochs) until the loss stops meaningfully improving."
        ),
        code=dict(
            lang="python",
            label="The smallest possible neural network, by hand",
            src=(
                "import numpy as np\n\n"
                "def relu(x):\n"
                "    return np.maximum(0, x)\n\n"
                "# 2 inputs -> 1 hidden neuron -> 1 output, no framework needed\n"
                "weights_hidden = np.array([0.5, -0.3])\n"
                "bias_hidden = 0.1\n"
                "weight_output = 0.8\n"
                "bias_output = -0.05\n\n"
                "def forward(x):\n"
                "    hidden = relu(np.dot(x, weights_hidden) + bias_hidden)\n"
                "    output = hidden * weight_output + bias_output\n"
                "    return output\n\n"
                "print(forward(np.array([1.0, 2.0])))"
            ),
        ),
        example=(
            "A house price predictor with 10 input features (square footage, bedrooms, location score...) and one "
            "hidden layer of 16 neurons is the same forward-pass math as the toy example above, just wider and "
            "trained with real data instead of hand-set weights."
        ),
        best_practices=[
            "Understand the forward pass by hand once — it demystifies every framework you'll use afterward.",
            "Start with the smallest network that could plausibly work; add layers only when underfitting shows up.",
            "Normalize input features before training — unscaled inputs make gradient descent unstable.",
        ],
        pitfalls=[
            "Skipping the nonlinear activation function, which reduces a 'deep' network to a single linear layer mathematically.",
            "Assuming more layers always means better performance — it often just means slower training and overfitting.",
        ],
        prompts=[
            "Walk me through backpropagation step by step with numbers.",
            "Why does ReLU work better than sigmoid in most modern networks?",
            "What actually happens during one 'epoch' of training?",
        ],
    ),
    dict(
        id="prompt-engineering",
        title="Prompt Engineering Basics",
        hook="A language model's output quality often changes more from how you ask than from which model you use.",
        explanation=(
            "Prompt engineering is the practice of structuring input to a language model to reliably get the "
            "output you want. The core levers are: being explicit about format ('respond in JSON with these exact "
            "keys'), providing examples of the input/output pattern you want (few-shot prompting), and giving the "
            "model room to reason before answering ('think step by step' or chain-of-thought prompting), which "
            "measurably improves accuracy on multi-step problems.\n\n"
            "System prompts set persistent context and constraints ('you are a customer support agent, never "
            "discuss pricing') separately from the user's actual question, which keeps behavior consistent across "
            "a conversation. Context matters more than clever phrasing: a model given the actual document to "
            "summarize will outperform one asked to summarize from memory, every time — this is the entire premise "
            "behind retrieval-augmented generation (RAG)."
        ),
        code=dict(
            lang="python",
            label="Structuring a prompt for reliable, parseable output",
            src=(
                "system_prompt = (\n"
                "    'You are a support-ticket classifier. Respond with ONLY valid JSON, '\n"
                "    'no other text, using exactly these keys: category, urgency (low/medium/high).'\n"
                ")\n\n"
                "user_prompt = (\n"
                "    'Ticket: \"My payment was charged twice for the same order, '\n"
                "    'and I need this fixed before my card statement closes tomorrow.\"'\n"
                ")\n\n"
                "# Sent as separate system + user messages to the model's chat API\n"
                "messages = [\n"
                "    {'role': 'system', 'content': system_prompt},\n"
                "    {'role': 'user', 'content': user_prompt},\n"
                "]\n"
                "# Expected: {\"category\": \"billing\", \"urgency\": \"high\"}"
            ),
        ),
        example=(
            "A support ticket router that asks for strict JSON output can feed the model's response directly into "
            "a database or workflow engine, where a vague free-text prompt would require fragile string parsing "
            "to extract the same information."
        ),
        best_practices=[
            "Specify the exact output format you need — models follow explicit format instructions far more reliably than implied ones.",
            "Give 2-3 examples of the input/output pattern for anything even slightly ambiguous (few-shot prompting).",
            "Separate persistent instructions (system prompt) from the specific request (user prompt).",
        ],
        pitfalls=[
            "Asking a model to recall facts from memory when you could just give it the source document instead.",
            "Writing a vague prompt and blaming the model instead of tightening the instructions first.",
        ],
        prompts=[
            "Show me a before/after example of a vague prompt versus a well-engineered one.",
            "What is chain-of-thought prompting and when does it actually help?",
            "How does retrieval-augmented generation (RAG) reduce hallucination?",
        ],
    ),
    dict(
        id="generative-ai-llms",
        title="Generative AI & LLMs",
        hook="Large language models generate text one token at a time, predicting the most probable next piece based on everything before it.",
        explanation=(
            "A Large Language Model is trained on huge amounts of text to predict the next token (roughly a word "
            "or word-piece) given everything that came before it. Generation happens autoregressively: the model "
            "produces one token, appends it to the input, and predicts the next one, repeating until it produces a "
            "stop signal. This is why LLMs can 'get stuck' compounding an early mistake — each token is generated "
            "conditioned on the ones before it, including any errors.\n\n"
            "'Generative AI' is the broader category that includes LLMs (text) plus image models like diffusion "
            "models (Stable Diffusion, Midjourney-style systems), audio generation, and video generation — the "
            "common thread is creating new content rather than classifying or scoring existing content. "
            "Temperature is the key generation parameter: low temperature makes output more deterministic and "
            "conservative, high temperature makes it more varied and creative, at the cost of coherence."
        ),
        code=dict(
            lang="python",
            label="Calling an LLM API with generation parameters",
            src=(
                "import requests\n\n"
                "response = requests.post(\n"
                "    'https://api.openai.com/v1/chat/completions',\n"
                "    headers={'Authorization': f'Bearer {API_KEY}'},\n"
                "    json={\n"
                "        'model': 'gpt-4o',\n"
                "        'messages': [{'role': 'user', 'content': 'Explain gradient descent in one sentence.'}],\n"
                "        'temperature': 0.2,   # low = focused, deterministic\n"
                "        'max_tokens': 100,\n"
                "    },\n"
                "    timeout=30,\n"
                ")\n"
                "print(response.json()['choices'][0]['message']['content'])"
            ),
        ),
        example=(
            "A legal-document summarizer sets temperature near 0 for consistency across runs, while a creative "
            "writing assistant sets it higher to get varied, less predictable phrasing on each generation."
        ),
        best_practices=[
            "Lower the temperature for tasks needing consistency (classification, extraction, code); raise it for creative tasks.",
            "Treat LLM output as a draft requiring verification for anything factual, legal, or numerical.",
            "Set `max_tokens` deliberately — unconstrained generation costs more and can run long unnecessarily.",
        ],
        pitfalls=[
            "Trusting an LLM's confident tone as a proxy for correctness — fluency and accuracy are not the same thing.",
            "Not accounting for token limits when feeding in long documents, silently truncating important context.",
        ],
        prompts=[
            "Explain hallucination in LLMs and why it happens.",
            "What's the difference between a diffusion model and a language model?",
            "How does temperature actually change the token selection process?",
        ],
    ),
    dict(
        id="ai-ethics-bias",
        title="AI Ethics & Bias",
        hook="A model doesn't need to be malicious to cause harm — it just needs to faithfully reproduce biased patterns in its training data.",
        explanation=(
            "Machine learning models learn statistical patterns from their training data, including whatever "
            "societal biases are baked into that data. A hiring model trained on a company's historical hiring "
            "decisions will learn to replicate any past discrimination in those decisions unless it's specifically "
            "corrected for, because from the model's perspective, past decisions are simply 'ground truth' to "
            "match.\n\n"
            "Common failure categories include representation bias (training data underrepresents some group), "
            "measurement bias (proxies used for a target don't measure it fairly across groups), and feedback "
            "loops (a biased model's decisions become tomorrow's training data, compounding the bias over time). "
            "Mitigation isn't just a modeling problem — it requires auditing training data, testing model outputs "
            "across demographic slices, and often accepting a deliberate trade-off between raw accuracy and "
            "fairness constraints."
        ),
        code=dict(
            lang="python",
            label="A minimal fairness check across a sensitive attribute",
            src=(
                "import pandas as pd\n\n"
                "# predictions: 1 = approved, 0 = denied\n"
                "df = pd.DataFrame({\n"
                "    'group': ['A', 'A', 'B', 'B', 'A', 'B'],\n"
                "    'approved': [1, 1, 0, 0, 1, 0],\n"
                "})\n\n"
                "approval_rate = df.groupby('group')['approved'].mean()\n"
                "print(approval_rate)\n"
                "# A large gap here is a signal worth investigating, not proof of discrimination —\n"
                "# but it's exactly the kind of check that should run before a model ships."
            ),
        ),
        example=(
            "A resume-screening tool trained mostly on resumes from past hires at a historically homogeneous "
            "company learned to downrank resumes mentioning a women's college — a real, widely reported failure "
            "case that surfaced only after deployment, not during initial testing."
        ),
        best_practices=[
            "Test model performance and outcomes separately across demographic groups before deployment, not just overall accuracy.",
            "Document training data sources and known limitations (a 'model card') alongside the model itself.",
            "Keep a human in the loop for high-stakes decisions (hiring, lending, medical) rather than fully automating them.",
        ],
        pitfalls=[
            "Assuming a model is 'objective' simply because it's math instead of a human decision.",
            "Removing a sensitive attribute (like race) from the input while leaving in proxies that correlate with it (like zip code).",
        ],
        prompts=[
            "Explain a real, documented case of AI bias causing harm.",
            "What's the difference between fairness through unawareness and true fairness?",
            "How would I audit a model I didn't build for bias?",
        ],
    ),
]
