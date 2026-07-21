"""Artificial Intelligence subtopics — enriched schema."""

SUBTOPICS = [
    dict(
        id="what-is-ai",
        title="What Is AI, Really?",
        hook="'AI' gets used for everything from a thermostat's simple if-statement to a language model writing poetry — the actual definitions are more specific, and knowing them helps you cut through the marketing.",
        explanation=(
            "Artificial Intelligence, broadly, is the field of building systems that perform tasks normally "
            "requiring human intelligence — perception, reasoning, language, decision-making. That definition "
            "is intentionally broad, which is exactly why 'AI' gets applied to both a simple rule-based chatbot "
            "and a large language model; the term describes a goal, not one specific technique.\n\n"
            "AI is commonly split into Narrow AI (systems designed for one specific task — a chess engine, a "
            "spam filter, an image classifier — and genuinely excellent at that task while being useless "
            "outside it) and General AI, or AGI (a hypothetical system with human-like flexibility across "
            "essentially any intellectual task). Every AI system in wide use today, including the most "
            "advanced language models, is narrow AI in this technical sense — extremely capable and broad in "
            "what topics it can discuss, but still fundamentally a pattern-completion system, not a "
            "generally-reasoning mind with independent goals.\n\n"
            "Within AI, Machine Learning is the dominant modern approach: instead of hand-coding explicit "
            "rules ('if temperature > 30, turn on the fan'), you show the system many examples and let it "
            "learn the pattern statistically. Deep Learning is a specific family of ML techniques using "
            "multi-layer neural networks, responsible for most of the recent, highly visible progress in "
            "image recognition, language, and generative AI (covered in its own lesson).\n\n"
            "It's worth being precise about this hierarchy because casual usage blurs it constantly: not "
            "every 'AI feature' involves machine learning at all (a lot of simple automation is still "
            "rule-based), and not every ML system is deep learning (many practical business problems are "
            "still solved well by simpler, classical ML techniques)."
        ),
        deep_dive=(
            "The Turing Test (1950), proposed by Alan Turing, suggested that a machine could be considered "
            "'thinking' if a human evaluator couldn't reliably distinguish its text responses from a real "
            "person's. It was a genuinely useful philosophical framing for its time, but modern AI researchers "
            "generally treat it as a poor practical benchmark — a system can pass convincingly through clever "
            "pattern matching and conversational tricks without anything resembling human understanding "
            "underneath, and conversely, a genuinely capable system might fail the test by being too obviously "
            "non-human in style.\n\n"
            "'AI winters' refers to two historical periods (roughly the 1970s and late 1980s/early 1990s) when "
            "AI research funding and interest collapsed after earlier over-promising failed to deliver, "
            "followed by long stretches of comparatively quiet, less-hyped progress. The pattern of hype "
            "cycles followed by disillusionment is a recurring feature of AI's history worth keeping in mind "
            "when evaluating current claims — genuine progress and hype have coexisted throughout the field's "
            "entire history.\n\n"
            "'Intelligence' itself has no single agreed technical definition even in cognitive science, which "
            "is part of why arguments about whether a given system 'really' understands or is 'really' "
            "intelligent tend to be more about definitions than about any specific, testable property of the "
            "system."
        ),
        code=dict(
            lang="text",
            label="The nested relationship: AI > ML > DL",
            src=(
                "Artificial Intelligence  (the broad goal: human-like task performance)\n"
                "  |\n"
                "  +-- Rule-based / symbolic systems (explicit hand-coded logic)\n"
                "  |\n"
                "  +-- Machine Learning  (learn patterns from data, not hand-coded rules)\n"
                "        |\n"
                "        +-- Classical ML (decision trees, linear models, SVMs, ...)\n"
                "        |\n"
                "        +-- Deep Learning  (multi-layer neural networks)\n"
                "              |\n"
                "              +-- Large Language Models, image generation, etc."
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="Narrow AI vs. AGI — a quick contrast",
            src=(
                "Narrow AI (everything that exists today, in production):\n"
                "  - Excellent at a defined task or broad-but-bounded domain\n"
                "  - No independent goals; operates only when invoked\n"
                "  - Performance can be rigorously measured against a benchmark\n\n"
                "AGI (hypothetical, not yet achieved):\n"
                "  - Human-like flexibility across essentially any intellectual task\n"
                "  - Actively researched and debated, no consensus timeline\n"
                "  - No agreed, rigorous test for having been achieved"
            ),
        ),
        example=(
            "A customer support chatbot that only handles pre-scripted flows ('press 1 for billing') is not "
            "AI in the modern ML sense at all — it's rule-based automation — while a support chatbot that "
            "reads and responds to open-ended customer messages using a language model is narrow AI: broad in "
            "topic, but still a bounded task (responding to text), not general intelligence."
        ),
        best_practices=[
            "Ask 'what specifically is learning from data here?' when evaluating an 'AI-powered' product claim — it clarifies whether ML is actually involved or the term is being used loosely.",
            "Distinguish narrow AI (what exists today) from AGI (a research goal, not a current reality) when discussing AI capabilities or risks.",
            "Treat impressive demos with healthy skepticism about generalization — a system performing well on cherry-picked examples doesn't guarantee robust real-world performance.",
        ],
        pitfalls=[
            "Assuming any system marketed as 'AI' involves machine learning — a lot of automation is still simple, explicit rule-based logic.",
            "Treating today's most advanced language models as evidence of AGI having been achieved, when they remain narrow (bounded to text-based tasks) despite their broad topical range.",
            "Using the Turing Test as a rigorous modern benchmark for 'real' intelligence, when it's now understood to be gameable and not closely tied to genuine understanding.",
        ],
        glossary=[
            dict(term="Narrow AI", definition="AI systems designed for a specific task or bounded domain, however broad that domain's topics might be — everything in production use today."),
            dict(term="AGI (Artificial General Intelligence)", definition="A hypothetical AI with human-like flexibility across essentially any intellectual task; not yet achieved."),
            dict(term="Machine Learning", definition="An approach to AI where systems learn patterns from data rather than following explicit hand-coded rules."),
            dict(term="AI winter", definition="A historical period of reduced AI research funding and interest following unmet expectations from earlier hype."),
        ],
        faq=[
            dict(q="Is ChatGPT (or any large language model) AGI?", a="No, by the common technical definition — it's an extremely capable narrow AI system bounded to text-based (and increasingly multimodal) tasks, without the general, independent, cross-domain reasoning and goal-setting that AGI implies. Whether or how AGI might eventually be reached is an active, unresolved research question."),
            dict(q="What's the actual difference between AI and machine learning?", a="AI is the broad goal (systems performing tasks requiring human-like intelligence). Machine learning is one major approach to achieving that goal — learning patterns from data — as opposed to older, rule-based/symbolic AI approaches that don't involve learning from data at all."),
            dict(q="Why does 'AI' get used so loosely in marketing?", a="Because the term describes a broad goal rather than one specific, well-defined technique, it's easy to apply to almost anything that automates a decision — regardless of whether machine learning is actually involved."),
        ],
        quiz=[
            dict(
                question="Which of these is an example of narrow AI, not AGI?",
                options=["A hypothetical system with human-like reasoning across any task", "A language model that only operates on text-based tasks, however broad the topics", "Neither term applies to any current technology", "AGI is a synonym for narrow AI"],
                correct=1,
                explanation="Even the most advanced current AI systems are narrow AI — bounded to specific kinds of tasks (like text) despite covering a wide range of topics within that bound.",
            ),
        ],
        prompts=[
            "Is this specific product feature actually machine learning, or just rule-based automation?",
            "Explain the difference between narrow AI and AGI with concrete examples.",
            "What were the AI winters, and what caused them?",
            "Why is the Turing Test no longer considered a rigorous benchmark?",
        ],
    ),
    dict(
        id="ai-ml-dl-hierarchy",
        title="AI vs. ML vs. Deep Learning: The Hierarchy",
        hook="These three terms are nested, not interchangeable — every deep learning system is machine learning, every machine learning system is AI, but the reverse isn't true in either direction.",
        explanation=(
            "Machine Learning is a subset of AI focused specifically on systems that improve their performance "
            "on a task by learning from data, rather than following explicit rules a programmer wrote by hand. "
            "A spam filter that starts with zero rules and learns to distinguish spam from legitimate email by "
            "examining thousands of labeled examples is doing machine learning; a spam filter using a "
            "hand-written list of banned words is not, even though both could be marketed as 'AI-powered "
            "spam detection.'\n\n"
            "Classical machine learning covers a wide family of techniques — linear regression, decision "
            "trees, support vector machines, random forests — that generally work well on structured, tabular "
            "data with a moderate number of engineered features, and are covered in depth in the Machine "
            "Learning topic. These techniques often require meaningful feature engineering (deciding what "
            "aspects of the raw data the model should look at) as a separate step from training the model "
            "itself.\n\n"
            "Deep Learning is a subset of machine learning using neural networks with many layers ('deep' "
            "refers to the number of layers), and its defining advantage is the ability to learn useful "
            "features directly from raw, unstructured data (images, audio, text) without a human manually "
            "engineering those features first — a deep learning image classifier learns to detect edges, "
            "then shapes, then objects, entirely from the raw pixels, layer by layer.\n\n"
            "This is why deep learning became the dominant approach specifically for unstructured data domains "
            "(vision, language, audio) over the past decade, while classical ML techniques remain competitive, "
            "often preferable, and generally cheaper to train and run for structured, tabular business data — "
            "the choice isn't 'deep learning is always better,' it's 'match the technique to the data and the "
            "problem.'"
        ),
        deep_dive=(
            "Feature engineering — manually deciding which aspects of raw data a model should consider (like "
            "computing 'days since last purchase' from raw transaction timestamps) — is often the single "
            "highest-leverage activity in classical ML, frequently mattering more to final model performance "
            "than the specific algorithm chosen. Deep learning's ability to skip this step for unstructured "
            "data is genuinely transformative for images/audio/text, but tabular business data with a "
            "well-understood domain often still benefits more from thoughtful feature engineering plus a "
            "simpler model than from throwing a deep network at raw columns.\n\n"
            "The 'depth' in deep learning isn't just a marketing term — each additional layer in a neural "
            "network can, in principle, learn increasingly abstract representations built on top of the "
            "previous layer's output, which is why early layers of an image classifier tend to detect simple "
            "edges and textures, middle layers detect parts and shapes, and late layers detect whole "
            "recognizable objects, without anyone explicitly programming that hierarchy.\n\n"
            "The trade-off for deep learning's power is data and compute: it generally needs substantially "
            "more labeled training examples and computational resources than classical ML to reach strong "
            "performance, which is why classical ML remains the pragmatic default for problems with limited "
            "data or tight computational budgets, even when a deep learning approach might theoretically "
            "perform slightly better given unlimited data and compute."
        ),
        code=dict(
            lang="text",
            label="Same task, two different technique families",
            src=(
                "Predicting house prices from tabular data (sqft, bedrooms, location, ...):\n"
                "  -> Classical ML (e.g. gradient-boosted trees) is often the practical default:\n"
                "     fast to train, interpretable, doesn't need millions of examples\n\n"
                "Classifying whether a photo contains a cat:\n"
                "  -> Deep Learning (a CNN) is the practical default:\n"
                "     raw pixels have no pre-built 'features' to engineer;\n"
                "     the network learns edge/shape/object detectors on its own"
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="What each layer of a deep image classifier tends to learn",
            src=(
                "Layer 1 (closest to input):  edges, simple color gradients\n"
                "Layer 2-3:                   textures, simple shapes (curves, corners)\n"
                "Layer 4-6:                   object parts (an eye, a wheel, a wing)\n"
                "Final layers:                whole recognizable objects (a face, a car)\n\n"
                "-- No human programmed this hierarchy directly; it emerges from training\n"
                "-- on labeled images via backpropagation (see the Deep Learning topic)"
            ),
        ),
        example=(
            "A bank building a loan default predictor with 40 well-understood tabular features (income, "
            "credit history, loan amount) reaches strong, interpretable performance with a classical gradient-"
            "boosted tree model, while the same bank's document-processing pipeline — reading raw scanned loan "
            "applications — genuinely needs deep learning (OCR and language models), since there's no simple "
            "tabular feature set to hand-engineer from a scanned image."
        ),
        best_practices=[
            "Start with classical ML for structured, tabular data with a moderate number of features — it's often faster to build, cheaper to run, and easier to interpret.",
            "Reach for deep learning specifically for unstructured data (images, audio, raw text) where manual feature engineering isn't practical.",
            "Consider available labeled data volume before choosing deep learning — it generally needs substantially more examples than classical ML to perform well.",
            "Remember that 'more advanced' doesn't mean 'always better' — match the technique family to the actual data and constraints of the problem.",
        ],
        pitfalls=[
            "Defaulting to deep learning for every problem regardless of data type, when a simpler, cheaper classical ML model would perform just as well or better on structured data.",
            "Underestimating how much labeled data deep learning typically needs to reach strong performance compared to classical techniques.",
            "Assuming 'deep learning' and 'AI' are synonyms, when deep learning is one specific, relatively recent family of techniques within the much broader field of AI.",
        ],
        glossary=[
            dict(term="Classical machine learning", definition="ML techniques (linear models, decision trees, SVMs, etc.) that generally require manual feature engineering and work well on structured, tabular data."),
            dict(term="Feature engineering", definition="Manually deciding and computing which aspects of raw data a model should use as input, a major part of classical ML workflows."),
            dict(term="Neural network depth", definition="The number of layers in a neural network; each layer can learn increasingly abstract representations built on the previous layer's output."),
            dict(term="Unstructured data", definition="Data without a predefined tabular structure — images, audio, and raw text — where deep learning's ability to learn features directly is especially valuable."),
        ],
        faq=[
            dict(q="Is deep learning always better than classical machine learning?", a="No — it depends on the data type and available volume. Deep learning tends to win decisively on unstructured data (images, audio, text) given enough data, while classical ML is often just as good or better, and cheaper, on structured tabular business data."),
            dict(q="Why does deep learning need so much more data than classical ML?", a="Deep networks have far more learnable parameters and are learning both the features and the final decision function simultaneously from raw data, which generally requires many more examples to avoid overfitting compared to a classical model working from carefully hand-engineered features."),
            dict(q="Are ML and deep learning the same thing?", a="No — deep learning is a specific subset of machine learning using multi-layer neural networks. All deep learning is machine learning, but plenty of machine learning (like a decision tree or linear regression) isn't deep learning."),
        ],
        quiz=[
            dict(
                question="Which statement correctly describes the relationship between AI, ML, and deep learning?",
                options=["They're three unrelated fields", "Deep learning contains ML contains AI", "AI contains ML, and ML contains deep learning as a subset", "AI and ML are synonyms, deep learning is separate"],
                correct=2,
                explanation="The relationship is nested: AI is the broadest goal, machine learning is one major approach within AI, and deep learning is a specific family of techniques within machine learning.",
            ),
        ],
        prompts=[
            "Should this specific problem use classical ML or deep learning?",
            "Explain feature engineering with a concrete tabular data example.",
            "Why does deep learning need so much more training data than classical ML?",
            "What does each layer of a deep image classifier typically learn?",
        ],
    ),
    dict(
        id="prompt-engineering",
        title="Prompt Engineering",
        hook="A language model's output quality often changes dramatically based purely on how a question is phrased — prompt engineering is the practice of phrasing deliberately instead of accidentally.",
        explanation=(
            "Prompt engineering is the practice of crafting inputs to a language model to reliably get better, "
            "more useful, more accurate outputs. Because language models generate text by predicting what "
            "comes next based on patterns learned during training, the exact framing, examples, and structure "
            "of a prompt meaningfully shifts what kind of response the model produces — the same underlying "
            "question can produce a vague, generic answer or a precise, well-structured one depending purely "
            "on how it's asked.\n\n"
            "Zero-shot prompting asks the model to perform a task with no examples ('Summarize this article "
            "in three sentences'). Few-shot prompting includes a small number of example input-output pairs "
            "directly in the prompt before the actual request, which can substantially improve performance on "
            "tasks with a specific expected format or style the model wouldn't otherwise infer.\n\n"
            "Chain-of-thought prompting — explicitly asking the model to reason step by step before giving a "
            "final answer ('Think through this step by step, then give your answer') — often improves "
            "performance on problems requiring multi-step reasoning, like math word problems or logic puzzles, "
            "compared to asking for the answer directly.\n\n"
            "System prompts (a separate instruction channel, distinct from the user's message, supported by "
            "most modern chat-based models) set persistent context, tone, role, or constraints that apply "
            "across an entire conversation — 'You are a concise technical writer who never uses jargon "
            "without explaining it' shapes every subsequent response without needing to repeat that "
            "instruction in every message."
        ),
        deep_dive=(
            "Specificity generally beats vagueness: a prompt specifying the desired format ('respond as a "
            "bulleted list', 'limit to 100 words', 'respond only in valid JSON matching this schema') gives "
            "the model a much narrower, more predictable target than an open-ended request, and reduces the "
            "need for post-processing the output.\n\n"
            "Providing relevant context directly in the prompt (pasting in the actual document to summarize, "
            "the actual error message to debug, the actual data to analyze) generally outperforms assuming "
            "the model has current, specific knowledge about your exact situation — a model's training data "
            "has a cutoff and no visibility into your private files or the current moment unless you "
            "explicitly provide that information or the model has tool access to retrieve it.\n\n"
            "Iterative refinement — treating the first response as a draft, then asking for specific changes "
            "('make this more concise', 'add error handling to the code', 'explain the third point in more "
            "detail') — is often far more effective than trying to craft one perfect initial prompt, since "
            "it's easier to correct a specific, visible flaw than to anticipate every requirement upfront."
        ),
        code=dict(
            lang="text",
            label="Vague vs. specific prompting",
            src=(
                "VAGUE:\n"
                "  \"Write something about our new product\"\n\n"
                "SPECIFIC:\n"
                "  \"Write a 150-word product announcement for our new noise-cancelling\n"
                "   headphones, targeting remote workers. Emphasize the 30-hour battery\n"
                "   life and the fact that they fold flat. Tone: confident but not salesy.\n"
                "   End with a single call-to-action sentence.\""
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="Few-shot prompting to lock in a specific format",
            src=(
                "Classify the sentiment of each review as positive, negative, or mixed.\n\n"
                "Review: \"Fast shipping but the product broke after a week.\"\n"
                "Sentiment: mixed\n\n"
                "Review: \"Exceeded my expectations, will buy again.\"\n"
                "Sentiment: positive\n\n"
                "Review: \"Customer service never responded to my emails.\"\n"
                "Sentiment: negative\n\n"
                "Review: \"Decent product, arrived on time, does what it says.\"\n"
                "Sentiment:"
            ),
        ),
        example=(
            "A developer debugging an error gets a generic, unhelpful response from 'Why doesn't my code "
            "work?' but a precise, actionable answer from a prompt including the actual error message, the "
            "relevant code snippet, and what they already tried — the difference isn't the model's "
            "capability, it's the amount of concrete context it has to reason from."
        ),
        best_practices=[
            "Include the actual relevant content (document, code, error message) directly in the prompt rather than describing it abstractly.",
            "Specify the desired output format explicitly (length, structure, style) when it matters for how you'll use the response.",
            "Use few-shot examples when you need a specific, consistent output format or style the model wouldn't infer from a zero-shot request.",
            "Treat the first response as a draft and iterate with specific follow-up requests rather than trying to perfect the prompt in one attempt.",
        ],
        pitfalls=[
            "Assuming the model has specific, current knowledge about your private data, recent events, or exact situation without providing that context directly.",
            "Writing an overly vague prompt and being surprised by a generic, unfocused response.",
            "Stacking too many unrelated instructions into one prompt, making it hard for the model to prioritize which part matters most.",
        ],
        glossary=[
            dict(term="Zero-shot prompting", definition="Asking a model to perform a task with no examples provided, relying entirely on its training."),
            dict(term="Few-shot prompting", definition="Including a small number of example input-output pairs in the prompt to guide the model toward a specific format or style."),
            dict(term="Chain-of-thought prompting", definition="Explicitly asking a model to reason step by step before giving a final answer, often improving performance on multi-step problems."),
            dict(term="System prompt", definition="A separate instruction channel setting persistent context, role, or constraints for an entire conversation."),
        ],
        faq=[
            dict(q="Does prompt engineering actually matter, or is it overhyped?", a="It genuinely matters for output quality and consistency, especially for production use cases needing a specific format or reliability — but it's not magic; a model still can't reliably do things fundamentally outside its training or capabilities no matter how the prompt is worded."),
            dict(q="What's the single highest-leverage change I can make to a vague prompt?", a="Adding concrete specifics: the actual content to work from, the desired format, and any constraints that matter — vagueness is the most common root cause of unhelpful responses."),
            dict(q="Why did few-shot examples change the model's output format so much?", a="The examples demonstrate the exact pattern you want, which the model then continues — it's directly showing the model what 'correct' looks like rather than describing it abstractly and hoping for the right interpretation."),
        ],
        quiz=[
            dict(
                question="What does chain-of-thought prompting typically improve?",
                options=["Response speed", "Performance on multi-step reasoning problems", "The model's training data", "Output length only"],
                correct=1,
                explanation="Asking a model to reason step by step before answering tends to improve accuracy specifically on problems requiring multiple logical or arithmetic steps.",
            ),
        ],
        prompts=[
            "Help me rewrite this vague prompt to get a more specific, useful response.",
            "Show me a few-shot prompt example for classifying support tickets by urgency.",
            "When does chain-of-thought prompting actually help versus just adding length?",
            "What's the difference between a system prompt and a regular user message?",
        ],
    ),
    dict(
        id="generative-ai-and-llms",
        title="Generative AI & Large Language Models",
        hook="A large language model doesn't 'look up' answers — it predicts, one token at a time, the most statistically plausible continuation of the text so far, based on patterns learned from enormous amounts of training text.",
        explanation=(
            "Generative AI refers to models that produce new content — text, images, audio, code — rather "
            "than just classifying or predicting a number from existing data. Large Language Models (LLMs) "
            "are the text-generating branch of generative AI, built on the transformer architecture (covered "
            "in depth in the Deep Learning topic), trained on massive amounts of text to predict the next "
            "token (roughly, a word or word-piece) given everything before it.\n\n"
            "Pretraining is the initial, extremely expensive phase where a model learns general language "
            "patterns, facts, and reasoning ability from a huge, broad text corpus, purely by learning to "
            "predict next tokens. Fine-tuning takes a pretrained model and further trains it on a smaller, "
            "more specific dataset to specialize its behavior — for instance, training it to follow "
            "instructions and hold helpful conversations, rather than just completing arbitrary text.\n\n"
            "A model's context window is the maximum amount of text (measured in tokens) it can consider at "
            "once — both the conversation history and the response being generated count against this limit. "
            "Once a conversation exceeds the context window, earlier parts have to be dropped or summarized, "
            "which is why very long conversations can cause a model to 'forget' earlier details.\n\n"
            "A knowledge cutoff is the date after which a model's training data ends — it has no inherent "
            "knowledge of events, releases, or changes after that date unless that information is provided "
            "directly in the prompt or the model has access to tools like web search."
        ),
        deep_dive=(
            "'Hallucination' describes a model generating plausible-sounding but factually incorrect or "
            "entirely fabricated information, stated with the same confident tone as accurate information. "
            "This happens because the model is fundamentally predicting statistically likely text, not "
            "querying a verified database of facts — it has no built-in mechanism to distinguish 'I actually "
            "know this' from 'this sounds like the kind of thing that would be true here,' which is why "
            "verifying important factual claims (especially specific numbers, citations, or names) remains "
            "necessary rather than optional.\n\n"
            "RLHF (Reinforcement Learning from Human Feedback) is a common technique in the fine-tuning stage "
            "where human raters compare and rank different model outputs for the same prompt, and that "
            "feedback trains the model to produce outputs more aligned with human preferences for "
            "helpfulness, honesty, and safety — a significant part of why modern instruction-tuned models feel "
            "noticeably more helpful and appropriately cautious than raw pretrained models.\n\n"
            "Multimodal models extend beyond text to accept and/or generate images, audio, or video within the "
            "same underlying architecture, letting a single model describe an image, generate one from a text "
            "description, or reason jointly across text and visual input in one request."
        ),
        code=dict(
            lang="text",
            label="Next-token prediction, conceptually",
            src=(
                "Input so far: \"The capital of France is\"\n\n"
                "Model's probability distribution over next token:\n"
                "  \"Paris\"     -> 94%\n"
                "  \"a\"         -> 2%\n"
                "  \"located\"   -> 1%\n"
                "  ...\n\n"
                "-- The model repeats this process one token at a time,\n"
                "-- each new token becoming part of the input for predicting the next"
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="Pretraining vs. fine-tuning at a glance",
            src=(
                "PRETRAINING\n"
                "  Data:  Massive, broad, general text corpus\n"
                "  Goal:  Learn general language patterns, facts, reasoning by predicting next tokens\n"
                "  Cost:  Extremely high (often months, huge compute clusters)\n\n"
                "FINE-TUNING (e.g. instruction tuning, RLHF)\n"
                "  Data:  Smaller, curated, task/behavior-specific dataset\n"
                "  Goal:  Specialize behavior -- follow instructions, be helpful and safe\n"
                "  Cost:  Much lower than pretraining, built on top of the pretrained model"
            ),
        ),
        example=(
            "Asking a model for a specific legal citation it isn't confident about can produce a "
            "confident-sounding but entirely fabricated case name and number — the model generated text that "
            "'looks like' a real citation based on patterns in its training data, without any mechanism to "
            "verify the citation actually exists, which is exactly why fact-checking specific claims matters."
        ),
        best_practices=[
            "Verify specific factual claims (numbers, citations, names, dates) from an LLM independently, especially for anything consequential.",
            "Provide relevant, current information directly in the prompt for anything that might postdate the model's knowledge cutoff.",
            "Be aware of a conversation's approaching context window limit for very long sessions, and summarize or restart when needed.",
            "Understand that a model's confident tone is not a reliable signal of factual accuracy — confidence and correctness are not the same thing for these systems.",
        ],
        pitfalls=[
            "Trusting a specific, checkable factual claim from a language model without verification, especially citations, statistics, or names.",
            "Assuming a model knows about anything after its training cutoff without that information being provided in the prompt or via a tool.",
            "Expecting consistent recall of details from very early in an extremely long conversation that has exceeded the model's context window.",
        ],
        glossary=[
            dict(term="Large Language Model (LLM)", definition="A transformer-based model trained on massive text data to predict and generate text, one token at a time."),
            dict(term="Context window", definition="The maximum amount of text (in tokens) a model can consider at once, including conversation history and its own response."),
            dict(term="Hallucination", definition="A model generating plausible-sounding but factually incorrect or fabricated content, stated with unwarranted confidence."),
            dict(term="Knowledge cutoff", definition="The date after which a model's training data ends, beyond which it has no inherent knowledge unless provided in the prompt."),
            dict(term="RLHF", definition="Reinforcement Learning from Human Feedback — a fine-tuning technique using human preference rankings to align model outputs with what people find helpful and appropriate."),
        ],
        faq=[
            dict(q="Why do language models sometimes confidently state wrong information?", a="They generate text by predicting statistically plausible continuations based on training data patterns, not by querying a verified fact database. There's no built-in mechanism distinguishing 'verified fact' from 'plausible-sounding text', which is exactly what causes hallucination."),
            dict(q="Can a language model learn new things during a conversation?", a="Not in the sense of updating its underlying trained knowledge — but it can use information provided directly within the conversation's context window to inform its responses for the rest of that session, which is different from genuinely learning and retaining it long-term."),
            dict(q="What's the difference between pretraining and fine-tuning?", a="Pretraining is the expensive initial phase learning general language patterns from massive, broad data. Fine-tuning takes that pretrained model and further trains it on a smaller, specific dataset to specialize its behavior, like following instructions helpfully and safely."),
        ],
        quiz=[
            dict(
                question="What fundamentally causes an LLM to hallucinate incorrect information?",
                options=["A bug in the software", "It generates statistically plausible text without a built-in fact-verification mechanism", "It's deliberately programmed to lie sometimes", "It only happens with very old models"],
                correct=1,
                explanation="LLMs predict likely continuations of text based on training patterns; they have no inherent way to distinguish verified facts from plausible-sounding fabrications.",
            ),
        ],
        prompts=[
            "Explain next-token prediction with a simple example sentence.",
            "Why should I fact-check a specific citation an AI model gives me?",
            "What's the practical difference between pretraining and fine-tuning?",
            "How does a model's context window limit affect a long conversation?",
        ],
    ),
    dict(
        id="neural-networks-101",
        title="Neural Networks, Explained From Scratch",
        hook="Before backpropagation and transformers make sense, it helps to see the single simplest possible neural network — one neuron — and understand exactly what it's computing.",
        explanation=(
            "At its simplest, a neural network is built from neurons, each performing the same small "
            "computation: take several numeric inputs, multiply each by a learned weight, add them together "
            "along with a learned bias term, and pass the result through an activation function that "
            "introduces non-linearity. Stack many neurons into a layer, and stack many layers, and you have a "
            "'deep' neural network — the specific details of activation functions, layer types, and training "
            "are covered in depth in the Deep Learning topic; this lesson focuses purely on the conceptual "
            "shape of what's happening.\n\n"
            "The 'learning' in a neural network is entirely about adjusting those weights and biases so the "
            "network's output gets closer to the correct answer across many training examples. This happens "
            "through repeated small adjustments — the network makes a prediction, compares it to the known "
            "correct answer, measures how wrong it was, and nudges every weight slightly in the direction that "
            "would have reduced that error, then repeats this process across thousands or millions of "
            "examples.\n\n"
            "This is fundamentally a statistical curve-fitting process — the network is finding a mathematical "
            "function that maps inputs to outputs in a way that matches the training examples as closely as "
            "possible, then hoping (and, if trained well, reliably managing) that this same function "
            "generalizes to new, unseen inputs it wasn't explicitly trained on.\n\n"
            "Nothing about this process involves the network 'understanding' concepts the way a person does — "
            "it's adjusting numerical parameters to minimize a mathematical error measure, which is why "
            "neural networks can produce astonishingly capable results on tasks well-represented in training "
            "data while failing in surprising, sometimes nonsensical ways on inputs meaningfully different "
            "from anything they were trained on."
        ),
        deep_dive=(
            "The Universal Approximation Theorem is a mathematical result establishing that a neural network "
            "with even just one sufficiently wide hidden layer can, in principle, approximate any continuous "
            "function to arbitrary precision — this is a genuinely important theoretical result, but it says "
            "nothing about whether such a network is *practical* to train or how much data it would need; "
            "'can theoretically approximate' and 'is efficient and learnable in practice' are very different "
            "claims, which is part of why deep (many-layer) networks turned out to be far more practical than "
            "very wide but shallow ones for most real-world problems.\n\n"
            "The specific architecture of a network — how many layers, how they're connected, what kind of "
            "layer (convolutional for images, recurrent or transformer-based for sequences, fully connected "
            "for general tabular relationships) — reflects assumptions about the structure of the problem, "
            "baked in by the people designing the architecture, not something the network invents from "
            "scratch. This is why choosing an appropriate architecture for the data type (covered in the Deep "
            "Learning topic's CNN and RNN/transformer lessons) matters enormously for both performance and "
            "training efficiency.\n\n"
            "The number of learnable parameters (weights and biases) in a modern large network can reach into "
            "the billions, which is part of why training requires massive amounts of data and computation — "
            "each parameter needs to be nudged toward a value that works well across the entire training set, "
            "not memorized for just a few examples, or the network overfits and fails to generalize."
        ),
        code=dict(
            lang="text",
            label="One neuron's computation, spelled out",
            src=(
                "Inputs:   x1 = 2.0,  x2 = 5.0\n"
                "Weights:  w1 = 0.4,  w2 = -0.7   (learned during training)\n"
                "Bias:     b = 0.1                (also learned)\n\n"
                "Step 1 -- weighted sum:\n"
                "  z = (x1 * w1) + (x2 * w2) + b\n"
                "  z = (2.0 * 0.4) + (5.0 * -0.7) + 0.1\n"
                "  z = 0.8 - 3.5 + 0.1 = -2.6\n\n"
                "Step 2 -- activation function (e.g. ReLU):\n"
                "  output = max(0, z) = max(0, -2.6) = 0"
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="The training loop, at the conceptual level",
            src=(
                "REPEAT for many examples (and many passes over all examples):\n\n"
                "  1. Feed an input through the network -> get a prediction\n"
                "  2. Compare the prediction to the known correct answer\n"
                "     -> compute a single number: how wrong was this? (the \"loss\")\n"
                "  3. Figure out, for every weight, which direction to nudge it\n"
                "     to reduce that loss (this is backpropagation, see Deep Learning)\n"
                "  4. Nudge every weight slightly in that direction\n\n"
                "After enough repetitions, the network's weights settle into values\n"
                "that produce accurate predictions across the whole training set."
            ),
        ),
        example=(
            "A network trained exclusively on photos of cats and dogs taken in daylight can perform "
            "excellently on new daylight photos while failing badly on the exact same animals photographed at "
            "night — not because it 'doesn't know' what a cat looks like, but because its learned weights were "
            "fit specifically to the statistical patterns present in daylight images, and nighttime images "
            "don't share those same pixel-level patterns."
        ),
        best_practices=[
            "Think of a neural network's 'knowledge' as a mathematical function fit to training data, not as understanding in the human sense, when reasoning about its likely failure modes.",
            "Expect degraded performance on inputs meaningfully different from the training data's distribution, and test explicitly for that gap rather than assuming it away.",
            "Match network architecture to the structure of the problem (covered in the Deep Learning topic) rather than assuming a generic network will perform equally well regardless of data type.",
        ],
        pitfalls=[
            "Assuming a network trained on one kind of data will generalize well to meaningfully different data without any evidence that it does.",
            "Anthropomorphizing what a network is doing ('it understands cats') in a way that leads to overconfident assumptions about its robustness.",
            "Confusing the Universal Approximation Theorem's theoretical guarantee with a practical claim about how easy or data-efficient training actually is.",
        ],
        glossary=[
            dict(term="Weight", definition="A learned numeric parameter controlling how much influence one input has on a neuron's output."),
            dict(term="Bias", definition="A learned numeric parameter added to a neuron's weighted sum, shifting its output independent of the inputs."),
            dict(term="Loss", definition="A single number measuring how wrong a model's prediction was compared to the correct answer, which training tries to minimize."),
            dict(term="Generalization", definition="A model's ability to perform well on new, unseen data, not just the examples it was trained on."),
        ],
        faq=[
            dict(q="Does a neural network actually 'understand' what it's processing?", a="Not in the human sense — it's fitting a mathematical function that maps inputs to outputs based on statistical patterns in training data. It can produce results indistinguishable from understanding on familiar inputs while failing in ways that reveal there's no deeper conceptual grasp underneath."),
            dict(q="Why do neural networks need so many training examples?", a="Because they're adjusting potentially millions or billions of numeric parameters to fit patterns that generalize, rather than memorizing rules — too few examples leads to overfitting (memorizing specifics rather than learning generalizable patterns)."),
            dict(q="What does the Universal Approximation Theorem actually guarantee?", a="That a sufficiently wide single-hidden-layer network can theoretically approximate any continuous function — a mathematical existence proof, not a practical claim about how easy or data-efficient it is to actually train such a network to do so."),
        ],
        quiz=[
            dict(
                question="What is a neural network fundamentally doing when it 'learns'?",
                options=["Storing exact copies of training examples", "Adjusting weights and biases to minimize error across training examples", "Searching a database of pre-written answers", "Running a fixed, hand-coded algorithm"],
                correct=1,
                explanation="Training is the iterative process of nudging every weight and bias toward values that reduce the measured error (loss) across the training examples.",
            ),
        ],
        prompts=[
            "Walk through the math of a single neuron with real numbers.",
            "Why does a model trained on one kind of data fail on meaningfully different data?",
            "Explain what the Universal Approximation Theorem does and doesn't guarantee.",
            "What's the difference between a weight and a bias in a neural network?",
        ],
    ),
    dict(
        id="embeddings-and-vector-search",
        title="Embeddings & Vector Search",
        hook="An embedding turns a word, sentence, or image into a list of numbers positioned so that 'similar meaning' becomes 'nearby in space' — which is what lets a computer search by meaning instead of by exact keyword match.",
        explanation=(
            "An embedding is a numeric vector (typically hundreds or thousands of numbers) representing a "
            "piece of content — a word, sentence, document, or image — produced by a trained model so that "
            "semantically similar inputs end up close together in that vector space, and dissimilar inputs "
            "end up far apart. 'King' and 'queen' end up near each other; 'king' and 'bicycle' end up far "
            "apart — not because anyone hand-labeled these relationships, but because the embedding model "
            "learned them from patterns in how these words are actually used across huge amounts of text.\n\n"
            "Similarity between two embeddings is typically measured with cosine similarity (the angle "
            "between the two vectors, ignoring their length) or Euclidean distance (straight-line distance) "
            "— cosine similarity is more common for text embeddings since it focuses purely on direction "
            "(meaning) rather than magnitude.\n\n"
            "A vector database (or vector index within a general-purpose database) stores embeddings and "
            "supports fast nearest-neighbor search — given a query embedding, quickly find the stored "
            "embeddings closest to it, out of potentially millions or billions of candidates, without "
            "comparing against every single one individually (which would be too slow at scale). Approximate "
            "nearest neighbor algorithms trade a small amount of accuracy for dramatic speed improvements, "
            "which is the standard, practical approach for production vector search.\n\n"
            "This is the foundation of semantic search: instead of matching exact keywords, you embed both "
            "the search query and every document, then find documents whose embeddings are closest to the "
            "query's embedding — surfacing results that are conceptually relevant even if they don't share "
            "any of the same literal words as the query."
        ),
        deep_dive=(
            "Embedding models are themselves trained neural networks, commonly using a technique where the "
            "model is trained to predict whether two pieces of text are related (like a search query and a "
            "document that actually answers it) or unrelated, gradually learning to position related content "
            "closer together in the vector space as a byproduct of getting better at that prediction task.\n\n"
            "Embedding dimensionality (how many numbers make up each vector — commonly ranging from a few "
            "hundred to a few thousand) is a trade-off: higher-dimensional embeddings can capture more nuance "
            "but cost more to store and search; different embedding models make different choices here, and "
            "embeddings from different models generally aren't directly comparable to each other, since each "
            "model's vector space has its own learned geometry.\n\n"
            "Beyond text, the same fundamental idea applies to images (an image embedding model positions "
            "visually and semantically similar images near each other), audio, and even cross-modal "
            "embeddings, where text and images can be embedded into a *shared* vector space, letting you "
            "search for images using a text description, or vice versa, because both were trained to land "
            "near each other in the same space when they're semantically related."
        ),
        code=dict(
            lang="text",
            label="Semantic similarity via embeddings, conceptually",
            src=(
                "embed(\"How do I reset my password?\")   -> [0.12, -0.44, 0.81, ...]\n"
                "embed(\"password recovery steps\")        -> [0.15, -0.41, 0.79, ...]   <- very close\n"
                "embed(\"best pizza toppings\")             -> [-0.62, 0.33, -0.05, ...]  <- far away\n\n"
                "cosine_similarity(query_vector, doc_vector)\n"
                "  -> a number from -1 (opposite meaning) to 1 (identical meaning)\n"
                "  -> \"password recovery steps\" scores much higher than \"pizza toppings\"\n"
                "  -> even though NEITHER shares the exact words \"reset\" or \"password\" in one case"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="A minimal semantic search flow using an embedding API",
            src=(
                "import numpy as np\n\n"
                "def cosine_similarity(a, b):\n"
                "    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))\n\n"
                "documents = [\"How to reset your password\", \"Our return policy\", \"Shipping times explained\"]\n"
                "doc_embeddings = [embed(doc) for doc in documents]     # from an embedding model/API\n\n"
                "query = \"I forgot my login credentials\"\n"
                "query_embedding = embed(query)\n\n"
                "scores = [cosine_similarity(query_embedding, d) for d in doc_embeddings]\n"
                "best_match = documents[np.argmax(scores)]   # \"How to reset your password\""
            ),
        ),
        example=(
            "A customer support search box returns the 'How to reset your password' article for the query 'I "
            "forgot my login credentials' — a keyword search would find nothing, since no words overlap, but "
            "semantic embedding search recognizes the two are about the same underlying topic."
        ),
        best_practices=[
            "Use the same embedding model to embed both your query and your documents — embeddings from different models generally aren't comparable to each other.",
            "Reach for cosine similarity for text embeddings as the standard, well-supported similarity measure.",
            "Use an approximate nearest neighbor index (not brute-force comparison) once your document collection grows beyond a small scale, for acceptable search latency.",
            "Combine semantic (embedding) search with traditional keyword search (hybrid search) when exact term matching also matters, like for product SKUs or proper nouns.",
        ],
        pitfalls=[
            "Mixing embeddings from two different models in the same similarity comparison, producing meaningless results since each model's vector space has different geometry.",
            "Assuming semantic search alone always outperforms keyword search — for exact identifiers (SKUs, error codes), keyword matching often works better.",
            "Doing brute-force similarity comparison against every stored embedding at large scale, which becomes a genuine performance bottleneck without an approximate nearest neighbor index.",
        ],
        glossary=[
            dict(term="Embedding", definition="A numeric vector representing a piece of content, positioned so that semantically similar content ends up nearby in the vector space."),
            dict(term="Cosine similarity", definition="A similarity measure based on the angle between two vectors, commonly used to compare text embeddings."),
            dict(term="Vector database", definition="A database optimized for storing embeddings and performing fast nearest-neighbor similarity search over them."),
            dict(term="Semantic search", definition="Search based on meaning (via embeddings) rather than exact keyword matching."),
        ],
        faq=[
            dict(q="Can I compare embeddings from two different models?", a="Not meaningfully — each embedding model learns its own vector space geometry during training, so a vector from one model and a vector from a different model aren't positioned in any comparable coordinate system, even if they have the same number of dimensions."),
            dict(q="Is semantic search always better than keyword search?", a="No — semantic search excels at conceptual relevance despite different wording, but keyword/exact-match search is often better for precise identifiers like product codes, error messages, or proper nouns. Many production systems combine both (hybrid search)."),
            dict(q="Why do I need a vector database instead of just comparing embeddings manually?", a="Comparing a query against millions or billions of stored embeddings one at a time is too slow for real-time search. Vector databases use approximate nearest neighbor algorithms to find close matches dramatically faster, trading a small amount of precision for large speed gains."),
        ],
        quiz=[
            dict(
                question="Why can 'password reset' and 'I forgot my login' match well in semantic search despite sharing no words?",
                options=["The search engine cheats by checking a synonym dictionary", "Their embeddings land close together in vector space because they're semantically related", "It's a coincidence", "Semantic search only works with exact word overlap"],
                correct=1,
                explanation="Embedding models learn to position semantically similar content near each other in vector space based on patterns in training data, independent of exact word overlap.",
            ),
        ],
        prompts=[
            "Explain cosine similarity with a simple two-dimensional example.",
            "When should I use hybrid search instead of pure semantic search?",
            "Why can't I compare embeddings from two different embedding models?",
            "Show me how approximate nearest neighbor search trades accuracy for speed.",
        ],
    ),
    dict(
        id="retrieval-augmented-generation",
        title="RAG: Retrieval-Augmented Generation",
        hook="RAG solves a very specific, practical problem — a language model can't know about your private documents or anything after its training cutoff — by fetching relevant information first, then handing it to the model as context.",
        explanation=(
            "Retrieval-Augmented Generation combines a retrieval step (finding relevant documents or passages, "
            "typically via embedding-based semantic search) with a generation step (a language model producing "
            "a response, using the retrieved content as additional context in the prompt). Instead of relying "
            "purely on what the model memorized during training, RAG lets the model answer based on specific, "
            "current, or private information supplied at query time.\n\n"
            "The typical pipeline: a user asks a question, the system embeds that question and searches a "
            "vector database of pre-embedded document chunks for the most relevant matches, those matching "
            "chunks get inserted into the prompt alongside the original question, and the language model "
            "generates an answer grounded in that retrieved content rather than purely from its training "
            "data.\n\n"
            "This directly addresses two real limitations of language models used alone: knowledge cutoffs "
            "(RAG can retrieve genuinely current information) and lack of access to private or "
            "domain-specific data (RAG can retrieve from a company's internal documents, which were never "
            "part of any public training data). It also generally reduces hallucination on the specific "
            "questions it's used for, since the model has concrete source material to draw from instead of "
            "purely generating from memorized patterns.\n\n"
            "Chunking — splitting long documents into smaller, retrievable pieces before embedding them — is "
            "a genuinely important practical detail: chunks that are too large dilute relevance (a long "
            "document might only have one relevant paragraph, buried among irrelevant ones), while chunks "
            "that are too small lose surrounding context needed to make sense of the retrieved piece."
        ),
        deep_dive=(
            "RAG doesn't eliminate hallucination entirely — a model can still misinterpret or misstate "
            "information even when given accurate retrieved context, and if the retrieval step returns "
            "irrelevant or low-quality matches, the model may either produce a poor answer grounded in the "
            "wrong material, or fall back on its own (potentially inaccurate) training knowledge instead. "
            "Retrieval quality is often the actual bottleneck in a RAG system's overall accuracy, more so than "
            "the generation model itself.\n\n"
            "Re-ranking is a common refinement: retrieve a larger initial set of candidate chunks quickly with "
            "an efficient embedding search, then apply a more expensive, more accurate ranking model to just "
            "that smaller candidate set to select the best few before handing them to the language model — "
            "balancing retrieval speed against final relevance quality.\n\n"
            "Citing sources — having the system indicate which specific retrieved chunk supported which part "
            "of the generated answer — is an important practical feature for trust and verifiability in "
            "production RAG systems, letting a user check the underlying source rather than simply trusting "
            "the generated summary at face value."
        ),
        code=dict(
            lang="text",
            label="The RAG pipeline, end to end",
            src=(
                "1. INDEX TIME (done once, ahead of any user query):\n"
                "   - Split documents into chunks\n"
                "   - Embed each chunk, store in a vector database\n\n"
                "2. QUERY TIME (for each user question):\n"
                "   User question: \"What's our refund policy for damaged items?\"\n"
                "   -> Embed the question\n"
                "   -> Search vector DB for the most similar chunks\n"
                "   -> Retrieved: [chunk from \"returns-policy.pdf\", page 3]\n"
                "   -> Build a prompt: \"Using this context: {retrieved chunk}\n"
                "                        answer: {user question}\"\n"
                "   -> Language model generates an answer grounded in that chunk"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="A minimal RAG query flow",
            src=(
                "def answer_question(question, vector_db, llm_client, k=3):\n"
                "    query_embedding = embed(question)\n"
                "    top_chunks = vector_db.search(query_embedding, top_k=k)\n\n"
                "    context = \"\\n\\n\".join(chunk.text for chunk in top_chunks)\n"
                "    prompt = (\n"
                "        f\"Answer the question using ONLY the context below. \"\n"
                "        f\"If the answer isn't in the context, say so.\\n\\n\"\n"
                "        f\"Context:\\n{context}\\n\\nQuestion: {question}\"\n"
                "    )\n"
                "    return llm_client.generate(prompt)"
            ),
        ),
        example=(
            "A company's internal support bot answers 'What's the current PTO policy?' correctly and "
            "currently, even though the policy document was updated last week and the underlying language "
            "model's training data is over a year old — because RAG retrieves and grounds the answer in the "
            "actual current document rather than relying on the model's memorized (and now outdated) training "
            "knowledge."
        ),
        best_practices=[
            "Explicitly instruct the model to answer only from the retrieved context, and to say so if the answer isn't present, rather than falling back on unguided generation.",
            "Tune chunk size deliberately — large enough to preserve context, small enough to keep retrieved matches specifically relevant.",
            "Invest in retrieval quality (better embeddings, re-ranking, hybrid search) as the highest-leverage improvement for most underperforming RAG systems, before assuming the generation model itself needs to change.",
            "Surface which source chunk(s) informed a given answer, so users can verify important claims against the original document.",
        ],
        pitfalls=[
            "Assuming RAG eliminates hallucination entirely — a model can still misstate or misinterpret even accurate retrieved context.",
            "Using chunks that are too large (diluting relevance) or too small (losing necessary surrounding context) for the specific document types involved.",
            "Not instructing the model to stick to the retrieved context, letting it blend in ungrounded, potentially inaccurate information from its general training.",
        ],
        glossary=[
            dict(term="RAG (Retrieval-Augmented Generation)", definition="Combining a retrieval step (finding relevant content) with a generation step (an LLM producing an answer using that content as context)."),
            dict(term="Chunking", definition="Splitting long documents into smaller pieces before embedding and indexing them for retrieval."),
            dict(term="Re-ranking", definition="Applying a more accurate (but slower) ranking model to a smaller candidate set after an initial fast retrieval pass."),
            dict(term="Grounding", definition="Basing a generated response on specific retrieved source material, rather than purely on the model's memorized training knowledge."),
        ],
        faq=[
            dict(q="Does RAG completely solve the hallucination problem?", a="No — it significantly reduces hallucination on questions the retrieved content actually covers well, but the model can still misinterpret accurate context or fall back on ungrounded generation if retrieval quality is poor. It's a major improvement, not a complete guarantee."),
            dict(q="Why not just fine-tune the model on my documents instead of using RAG?", a="Fine-tuning is more expensive, harder to keep current as documents change, and doesn't let you easily cite specific sources. RAG lets you update the underlying document set at any time without retraining anything, and naturally supports source attribution."),
            dict(q="What's usually the actual bottleneck in a RAG system that isn't performing well?", a="Retrieval quality, more often than the language model itself — if the wrong chunks are retrieved, even the best generation model can only produce a poor or irrelevant answer from bad input."),
        ],
        quiz=[
            dict(
                question="What problem does RAG most directly address?",
                options=["Making models generate faster", "Giving a model access to current or private information beyond its training data", "Reducing the model's training cost", "Making the model's code run on a phone"],
                correct=1,
                explanation="RAG retrieves relevant, current, or private content at query time and provides it as context, letting the model answer based on information it was never trained on.",
            ),
        ],
        prompts=[
            "Design a RAG pipeline for answering questions from our internal company wiki.",
            "Why might my RAG system be giving wrong answers even though the right document exists?",
            "What's the difference between RAG and fine-tuning a model on my own data?",
            "How should I choose an appropriate chunk size for my documents?",
        ],
    ),
    dict(
        id="ai-agents-and-tool-use",
        title="AI Agents & Tool Use",
        hook="A plain language model only produces text — an agent is what you get when you give that model the ability to take actions in the world and decide for itself, step by step, what action to take next.",
        explanation=(
            "An AI agent, in the current common usage, is a system built around a language model that can "
            "decide to call external tools (search the web, run code, query a database, send an email) as "
            "part of accomplishing a task, rather than only generating a single, static text response. The "
            "model is given a list of available tools with descriptions, and it decides — based on the "
            "current task — whether to call a tool, which one, with what arguments, then incorporates the "
            "tool's result into its next step of reasoning.\n\n"
            "This 'reason, act, observe, repeat' loop is often called ReAct (reasoning + acting): the model "
            "reasons about what to do next, takes an action (a tool call), observes the result, and uses that "
            "observation to inform its next reasoning step — continuing until it decides the task is complete "
            "or it needs to ask the user for clarification.\n\n"
            "Function calling (or 'tool calling') is the underlying mechanism most modern LLM APIs expose for "
            "this: you describe available functions with a name, description, and parameter schema, and the "
            "model can respond by requesting a specific function call with specific arguments instead of (or "
            "alongside) plain text — your application code then actually executes that function and returns "
            "the result back to the model as part of the ongoing conversation.\n\n"
            "The Model Context Protocol (MCP, covered in its own topic) is a standardization of exactly this "
            "idea — a common protocol for exposing tools to any compatible AI agent, rather than every "
            "application needing a custom, bespoke integration for every tool it wants to offer a model."
        ),
        deep_dive=(
            "Giving a model the ability to take real actions (send an email, delete a file, make a purchase) "
            "meaningfully raises the stakes of any mistake compared to a model that only generates text a "
            "human reviews before acting on it — this is why many agent systems include human-in-the-loop "
            "checkpoints for consequential or irreversible actions, requiring explicit confirmation before "
            "the agent actually executes them, rather than letting the agent act fully autonomously on "
            "everything.\n\n"
            "Multi-step agent tasks can fail in ways a single text response can't: an agent might call the "
            "wrong tool, misinterpret a tool's result, get stuck in a loop repeating a failing action, or "
            "successfully complete individual steps that don't actually add up to the intended overall "
            "outcome — which is why evaluating agent systems generally requires testing the entire task "
            "end-to-end, not just each individual tool call in isolation.\n\n"
            "Agent memory and state management is a genuinely hard practical problem: a long-running agent "
            "task needs to track what's already been tried, what's been learned, and what still needs to "
            "happen, without simply relying on an ever-growing conversation history that will eventually "
            "exceed the model's context window — production agent systems often implement explicit "
            "summarization, structured task tracking, or external memory stores to manage this."
        ),
        code=dict(
            lang="text",
            label="The ReAct loop for a simple agent task",
            src=(
                "Task: \"What's the weather in the capital of France?\"\n\n"
                "Step 1 -- REASON: \"I need to know the capital of France first,\n"
                "                    then look up its weather.\"\n"
                "Step 2 -- ACT:     call search_tool(\"capital of France\")\n"
                "Step 3 -- OBSERVE: result = \"Paris\"\n"
                "Step 4 -- REASON:  \"Now I need the weather in Paris.\"\n"
                "Step 5 -- ACT:     call weather_tool(\"Paris\")\n"
                "Step 6 -- OBSERVE: result = \"18C, partly cloudy\"\n"
                "Step 7 -- REASON:  \"I have what I need.\"\n"
                "Step 8 -- RESPOND: \"It's 18C and partly cloudy in Paris.\""
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="A minimal tool-calling loop (conceptual, framework-agnostic)",
            src=(
                "tools = {\"search\": search_function, \"get_weather\": weather_function}\n\n"
                "conversation = [{\"role\": \"user\", \"content\": user_question}]\n\n"
                "while True:\n"
                "    response = llm.generate(conversation, available_tools=list(tools.keys()))\n\n"
                "    if response.tool_call:\n"
                "        result = tools[response.tool_call.name](**response.tool_call.arguments)\n"
                "        conversation.append({\"role\": \"tool\", \"content\": result})\n"
                "        continue     # loop again, model sees the tool result\n\n"
                "    break            # model responded with plain text -- task considered done\n\n"
                "print(response.text)"
            ),
        ),
        example=(
            "A coding agent tasked with 'fix the failing test' reads the test output (a tool call), inspects "
            "the relevant source file (another tool call), proposes and applies a code change (another tool "
            "call), re-runs the test to check if it passes (another tool call), and repeats this loop until "
            "the test passes or it determines it needs human input — an entire multi-step workflow driven by "
            "the model's own reasoning about what to do next at each stage."
        ),
        best_practices=[
            "Give each tool a clear, specific description and well-typed parameters — the model relies entirely on that description to decide when and how to call it.",
            "Add human-in-the-loop confirmation for any action that's consequential, costly, or hard to reverse.",
            "Test agent systems end-to-end on realistic multi-step tasks, not just individual tool calls in isolation.",
            "Design explicit ways for the agent to signal it's stuck or needs clarification, rather than looping indefinitely or guessing.",
        ],
        pitfalls=[
            "Giving an agent unrestricted access to consequential actions (financial transactions, deleting data) without any human checkpoint or safeguard.",
            "Writing vague or ambiguous tool descriptions, leading the model to call the wrong tool or pass incorrect arguments.",
            "Assuming a multi-step agent task will reliably self-correct from an early mistake, rather than testing failure recovery explicitly.",
        ],
        glossary=[
            dict(term="AI agent", definition="A system built around a language model that can decide to call external tools and take actions as part of accomplishing a task, not just generate text."),
            dict(term="Function calling / tool calling", definition="The mechanism by which a model requests a specific function be executed with specific arguments, as part of an API interaction."),
            dict(term="ReAct (Reason + Act)", definition="A loop pattern where a model reasons about the next step, takes an action, observes the result, and repeats until the task is complete."),
            dict(term="Human-in-the-loop", definition="A design pattern requiring explicit human confirmation before an agent executes a consequential or irreversible action."),
        ],
        faq=[
            dict(q="What's the actual difference between an AI agent and a regular chatbot?", a="A regular chatbot only generates text responses. An agent can decide to call external tools — searching, running code, querying data, taking real actions — and incorporate the results into its ongoing reasoning, potentially over many steps, before producing a final response."),
            dict(q="Why do agent systems need human-in-the-loop checkpoints?", a="Because giving a model the ability to take real, potentially irreversible actions raises the cost of any mistake significantly compared to generating text a human reviews first — checkpoints let a human confirm consequential actions before they actually happen."),
            dict(q="How is MCP related to agents and tool calling?", a="MCP standardizes how tools are exposed to any compatible agent, so a tool builder writes one MCP server instead of custom integration code for every different AI application that might want to use that tool."),
        ],
        quiz=[
            dict(
                question="What does the ReAct pattern describe?",
                options=["A JavaScript framework", "A loop of reasoning, acting via a tool, and observing the result, repeated until the task is done", "A type of neural network layer", "A method for training language models"],
                correct=1,
                explanation="ReAct describes an agent's iterative process: reason about what to do, take an action (often a tool call), observe the result, and use that to inform the next reasoning step.",
            ),
        ],
        prompts=[
            "Design a tool-calling agent that can answer questions using a search API and a calculator.",
            "Why should consequential agent actions require human confirmation?",
            "Explain the ReAct pattern with a concrete multi-step example.",
            "What's the relationship between MCP and agent tool calling?",
        ],
    ),
    dict(
        id="ai-ethics-and-bias",
        title="AI Ethics, Bias & Responsible Use",
        hook="An AI system trained on historical data doesn't just learn the patterns in that data — it learns the biases baked into it too, often invisibly, unless someone specifically looks for them.",
        explanation=(
            "Bias in AI systems typically originates from the training data reflecting historical or societal "
            "inequities, which the model then learns and reproduces (or even amplifies) in its outputs — a "
            "hiring model trained on a company's past hiring decisions can learn to replicate past "
            "discriminatory patterns, even without any single feature explicitly encoding a protected "
            "characteristic, since other features can act as unintended proxies for it.\n\n"
            "Fairness in ML is genuinely difficult partly because there are multiple, mathematically "
            "incompatible definitions of what 'fair' means (equal outcomes across groups, equal error rates "
            "across groups, individual fairness for similar cases) — a system can satisfy one definition of "
            "fairness while violating another, which is why fairness requires deliberate, context-specific "
            "decisions rather than a single universal fix.\n\n"
            "Explainability (or interpretability) concerns how well a person can understand *why* a model "
            "produced a specific output — simpler models like decision trees are inherently more interpretable "
            "than deep neural networks, which is a genuine trade-off to weigh against raw predictive "
            "performance, especially for high-stakes decisions (loan approvals, medical diagnoses, criminal "
            "justice) where an unexplainable 'the model said no' is a serious practical and ethical problem.\n\n"
            "Privacy concerns include both the data used to train a model (was it collected and used with "
            "appropriate consent) and the risk of a model inadvertently memorizing and later reproducing "
            "specific, sensitive pieces of its training data when prompted in particular ways."
        ),
        deep_dive=(
            "Proxy discrimination is a specific, subtle failure mode: even when a protected characteristic "
            "(like race or gender) is deliberately excluded from a model's input features, other features can "
            "correlate strongly enough with it (zip code correlating with race in a segregated housing "
            "market, for instance) that the model effectively discriminates on the excluded characteristic "
            "anyway, through these unintended proxies — simply removing the obvious feature doesn't guarantee "
            "fairness.\n\n"
            "Auditing a model for bias generally requires deliberately measuring its performance and outcomes "
            "*broken down by relevant demographic groups*, not just an aggregate accuracy number — a model "
            "with 95% overall accuracy might still perform substantially worse for a specific subgroup, which "
            "an aggregate metric alone would completely hide.\n\n"
            "Responsible AI deployment generally involves layers beyond just the model itself: clear "
            "disclosure that a user is interacting with an AI system, meaningful human review for high-stakes "
            "automated decisions, mechanisms for people to contest or appeal a decision the system made about "
            "them, and ongoing monitoring after deployment rather than treating a fairness evaluation as a "
            "one-time checkbox before launch."
        ),
        code=dict(
            lang="text",
            label="A simplified illustration of proxy discrimination",
            src=(
                "Model input features: [income, credit_score, zip_code, loan_amount]\n"
                "-- 'race' was deliberately excluded from the model's features --\n\n"
                "But: zip_code correlates strongly with race in this region\n"
                "  due to historical housing segregation patterns\n\n"
                "Result: the model can still produce racially disparate outcomes,\n"
                "        effectively discriminating THROUGH zip_code as a proxy,\n"
                "        despite race never being an explicit input"
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="Auditing for bias: aggregate vs. subgroup metrics",
            src=(
                "Overall accuracy: 95%   <- looks great in isolation\n\n"
                "Broken down by subgroup:\n"
                "  Group A: 97% accuracy\n"
                "  Group B: 78% accuracy   <- hidden by the aggregate number\n\n"
                "-- This gap would be invisible without deliberately\n"
                "-- measuring and reporting subgroup-level performance"
            ),
        ),
        example=(
            "A resume-screening model trained on a company's historical hiring data learned to downrank "
            "resumes mentioning a women's college or certain extracurriculars associated with women, despite "
            "gender never being an explicit input feature — the model had picked up the pattern from the "
            "company's own historically skewed hiring outcomes, and the company discontinued the tool once "
            "this was discovered during an internal audit."
        ),
        best_practices=[
            "Evaluate model performance broken down by relevant demographic subgroups, not just aggregate metrics, especially for high-stakes decisions.",
            "Treat feature exclusion (removing an explicit protected characteristic) as insufficient alone — actively check for correlated proxy features.",
            "Weigh interpretability seriously for high-stakes decisions, where an unexplainable model output is a genuine practical and ethical liability, not just an inconvenience.",
            "Build in human review, appeal mechanisms, and ongoing post-deployment monitoring for consequential automated decisions, rather than treating fairness as a one-time pre-launch check.",
        ],
        pitfalls=[
            "Assuming a model is unbiased simply because a protected characteristic was excluded from its input features, ignoring the risk of proxy discrimination through correlated features.",
            "Relying solely on an aggregate accuracy metric, which can hide substantially worse performance for a specific subgroup.",
            "Treating an AI system's output as an unquestionable, unexplainable final decision for high-stakes situations without a human review or appeal path.",
        ],
        glossary=[
            dict(term="Proxy discrimination", definition="A model effectively discriminating on an excluded protected characteristic through other features that correlate strongly with it."),
            dict(term="Fairness (in ML)", definition="A model's outcomes or errors being appropriately equitable across different groups — with several mathematically distinct, sometimes incompatible definitions of what 'appropriately equitable' means."),
            dict(term="Interpretability / explainability", definition="How well a person can understand why a model produced a specific output, generally in tension with raw predictive performance for complex models."),
            dict(term="Subgroup analysis", definition="Evaluating a model's performance separately for different demographic or category groups, rather than relying only on an aggregate metric."),
        ],
        faq=[
            dict(q="If I remove race/gender from my model's features, is it automatically fair?", a="No — this is one of the most common and dangerous misconceptions. Other features can act as proxies for the excluded characteristic (zip code for race, certain activities for gender), letting the model effectively discriminate anyway without ever seeing the protected feature directly."),
            dict(q="Why can't there just be one agreed definition of 'fair' for a model?", a="Different mathematical fairness definitions (equal outcomes across groups vs. equal error rates across groups, for example) can be mutually incompatible in practice — satisfying one can mean violating another, which is why fairness requires deliberate, context-specific trade-off decisions."),
            dict(q="Why does a 95% accurate model still need bias auditing?", a="An aggregate accuracy number can hide substantially worse performance for a specific subgroup — the only way to know is to deliberately measure performance broken down by relevant groups, not just look at the overall number."),
        ],
        quiz=[
            dict(
                question="What is proxy discrimination?",
                options=["A model refusing to make any prediction", "A model discriminating on an excluded characteristic through other, correlated features", "A type of data encryption", "An error that only happens in deep learning models"],
                correct=1,
                explanation="Even without a protected characteristic as an explicit input, other correlated features can let a model reproduce the same discriminatory pattern indirectly.",
            ),
        ],
        prompts=[
            "How would I check this hiring model for potential proxy discrimination?",
            "Explain why fairness has multiple, sometimes incompatible mathematical definitions.",
            "What's the trade-off between model interpretability and predictive performance?",
            "Design an approach to audit a model's performance across different demographic subgroups.",
        ],
    ),
]