"""Deep Learning subtopics."""

SUBTOPICS = [
    dict(
        id="neurons-activation-functions",
        title="Neurons, Layers & Activation Functions",
        hook="A neural network is just a stack of weighted sums and simple non-linear functions — the 'deep' part is stacking enough of them to approximate very complex patterns.",
        explanation=(
            "A single artificial neuron computes a weighted sum of its inputs, adds a bias, and passes the "
            "result through an activation function. Without that activation function, stacking layers would be "
            "mathematically pointless — a chain of purely linear operations collapses into a single linear "
            "operation, no matter how many layers you add. The activation function is what lets a network learn "
            "non-linear, real-world patterns.\n\n"
            "ReLU (`max(0, x)`) is the default choice for hidden layers in most modern networks because it's "
            "cheap to compute and avoids some of the training problems older activations like sigmoid have. The "
            "output layer's activation depends on the task: sigmoid for binary classification (squashes to "
            "0-1), softmax for multi-class classification (outputs a probability distribution across classes), "
            "or no activation (linear) for regression."
        ),
        code=dict(
            lang="python",
            label="A single neuron's math, then a Keras layer",
            src=(
                "import numpy as np\n\n"
                "# One neuron by hand\n"
                "inputs = np.array([1.0, 2.0, 3.0])\n"
                "weights = np.array([0.2, -0.5, 0.1])\n"
                "bias = 0.4\n"
                "z = np.dot(inputs, weights) + bias\n"
                "activation = max(0, z)   # ReLU\n\n"
                "# The same idea, but 64 neurons, via Keras\n"
                "import tensorflow as tf\n"
                "layer = tf.keras.layers.Dense(64, activation=\"relu\")"
            ),
        ),
        example=(
            "Swapping a hidden layer's activation from sigmoid to ReLU on a deep image classifier often speeds "
            "up training noticeably, because sigmoid's gradient shrinks toward zero for large inputs (the "
            "vanishing gradient problem), while ReLU's gradient stays constant for any positive input."
        ),
        best_practices=[
            "Default to ReLU (or a variant like Leaky ReLU) for hidden layers unless you have a specific reason to use something else.",
            "Match the output layer's activation to the task: sigmoid for binary, softmax for multi-class, none for regression.",
            "Initialize weights with a scheme matched to your activation (like He initialization for ReLU) — poor initialization alone can prevent a network from training at all.",
        ],
        pitfalls=[
            "Using sigmoid or tanh throughout a deep network and running into vanishing gradients that stall training.",
            "Forgetting an activation function entirely on hidden layers, which collapses the network into an equivalent single linear layer.",
        ],
        prompts=[
            "Explain the vanishing gradient problem and why ReLU helps with it.",
            "When would I use tanh instead of ReLU?",
            "Walk through the math of a single neuron with actual numbers.",
        ],
    ),
    dict(
        id="backpropagation-training",
        title="Backpropagation & Gradient Descent",
        hook="Backpropagation isn't a separate algorithm from gradient descent — it's just an efficient way to compute the gradients that gradient descent needs.",
        explanation=(
            "Training a neural network means adjusting its weights to reduce a loss function that measures how "
            "wrong its predictions are. Gradient descent does this by nudging each weight in the direction that "
            "reduces the loss, scaled by a learning rate. The question is how to compute, for a network with "
            "millions of weights, exactly how much each one contributed to the error — that's what "
            "backpropagation solves, using the chain rule from calculus to propagate the error backward from the "
            "output layer to every earlier layer efficiently.\n\n"
            "In practice, nobody hand-codes the chain rule; frameworks like PyTorch and TensorFlow use automatic "
            "differentiation to compute gradients for you. The concept still matters because it explains real "
            "training symptoms: a learning rate that's too high overshoots and diverges, one that's too low "
            "trains painfully slowly, and certain architectures (very deep or with certain activations) can "
            "suffer vanishing or exploding gradients during this backward pass."
        ),
        code=dict(
            lang="python",
            label="One training step in PyTorch (autograd doing backprop for you)",
            src=(
                "import torch\n\n"
                "loss_fn = torch.nn.CrossEntropyLoss()\n"
                "optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)\n\n"
                "for inputs, labels in dataloader:\n"
                "    optimizer.zero_grad()\n"
                "    outputs = model(inputs)\n"
                "    loss = loss_fn(outputs, labels)\n"
                "    loss.backward()          # backpropagation: computes gradients\n"
                "    optimizer.step()          # gradient descent: updates weights"
            ),
        ),
        example=(
            "A training run where the loss suddenly explodes to `NaN` after a few epochs is a textbook symptom "
            "of an exploding gradient, usually fixed by gradient clipping or lowering the learning rate — a "
            "diagnosis that only makes sense once you understand what's flowing backward through the network."
        ),
        best_practices=[
            "Start with a well-tested optimizer like Adam and a conservative learning rate (e.g. 1e-3 or 1e-4) before trying to hand-tune from scratch.",
            "Watch the training loss curve, not just the final number — a loss that plateaus, oscillates, or diverges tells you exactly what's wrong.",
            "Use gradient clipping for recurrent architectures or very deep networks, which are especially prone to exploding gradients.",
        ],
        pitfalls=[
            "Setting a learning rate too high and watching loss oscillate or diverge instead of decrease.",
            "Assuming a bug is in the model architecture when it's actually a data problem (unnormalized inputs, wrong labels) manifesting as bad gradients.",
        ],
        prompts=[
            "Why did my training loss turn into NaN, and how do I fix it?",
            "Explain backpropagation using the chain rule with a two-layer example.",
            "What's the difference between SGD, Adam, and RMSprop as optimizers?",
        ],
    ),
    dict(
        id="cnns-computer-vision",
        title="CNNs & Computer Vision Basics",
        hook="A Dense layer looks at every pixel independently; a convolutional layer looks at small neighborhoods of pixels — that single shift is why CNNs are so good at images.",
        explanation=(
            "A Convolutional Neural Network applies small learnable filters (kernels) that slide across an "
            "image, each one detecting a local pattern — edges in early layers, textures and shapes in middle "
            "layers, whole objects in later layers. This exploits a property that's true of most images: nearby "
            "pixels are related, and the same edge-detecting filter that works in one corner of an image is "
            "useful everywhere else in it too, so the filter's weights are shared across the whole image instead "
            "of learning a separate weight per pixel.\n\n"
            "Pooling layers (typically max pooling) down-sample the feature maps between convolutions, reducing "
            "spatial size while keeping the strongest signals, which both reduces computation and adds a small "
            "amount of translation invariance. Before the final classification layer, the multi-dimensional "
            "feature maps need to be turned into a flat vector — via `Flatten()` or, more efficiently, "
            "`GlobalAveragePooling2D()`."
        ),
        code=dict(
            lang="python",
            label="A small image classifier with Keras",
            src=(
                "import tensorflow as tf\n\n"
                "model = tf.keras.Sequential([\n"
                "    tf.keras.layers.Conv2D(32, 3, activation=\"relu\", input_shape=(64, 64, 3)),\n"
                "    tf.keras.layers.MaxPooling2D(),\n"
                "    tf.keras.layers.Conv2D(64, 3, activation=\"relu\"),\n"
                "    tf.keras.layers.GlobalAveragePooling2D(),\n"
                "    tf.keras.layers.Dense(10, activation=\"softmax\"),\n"
                "])\n"
                "model.summary()"
            ),
        ),
        example=(
            "A quality-control camera on a manufacturing line uses a CNN trained on a few thousand labeled "
            "images of defective and non-defective parts — the early convolutional layers learn generic edge and "
            "texture detectors that transfer surprisingly well even across different product lines."
        ),
        best_practices=[
            "Start from a pretrained backbone (transfer learning) rather than training a CNN from scratch, unless you have a genuinely large, task-specific dataset.",
            "Always run `model.summary()` after changing the architecture — it's the fastest way to catch a shape mismatch before training even starts.",
            "Normalize pixel values (typically to 0-1 or using the pretrained model's expected preprocessing) before feeding images into the network.",
        ],
        pitfalls=[
            "Feeding raw 0-255 pixel values into a network expecting normalized inputs, which slows or destabilizes training.",
            "Forgetting a Flatten or GlobalAveragePooling step between the convolutional base and a Dense classification head, causing a shape error.",
        ],
        prompts=[
            "Explain how a convolutional filter detects an edge with a simple numeric example.",
            "When should I use transfer learning instead of training a CNN from scratch?",
            "What's the difference between MaxPooling and GlobalAveragePooling?",
        ],
    ),
    dict(
        id="rnns-sequences",
        title="RNNs, LSTMs & Sequential Data",
        hook="Some data has order baked into its meaning — a sentence, a stock price series, a sensor stream — and RNNs are the architecture built specifically to remember what came before.",
        explanation=(
            "A Recurrent Neural Network processes a sequence one element at a time, carrying a hidden state "
            "forward that acts as a summary of everything seen so far. This makes RNNs a natural fit for text, "
            "time series, and audio, where the order of inputs carries meaning that a plain feedforward network "
            "would throw away. Plain (vanilla) RNNs struggle with long sequences, though, because gradients "
            "flowing back through many time steps tend to vanish, effectively making the network 'forget' "
            "anything from too far in the past.\n\n"
            "LSTMs (Long Short-Term Memory) and the simpler GRU (Gated Recurrent Unit) solve this with gating "
            "mechanisms — learned gates that decide what to keep, forget, and output at each step — letting "
            "information flow across many more time steps without vanishing. In practice, LSTM/GRU layers were "
            "the standard for sequence tasks before transformer-based architectures became dominant for most NLP "
            "workloads, though RNNs remain relevant for many time series and streaming use cases."
        ),
        code=dict(
            lang="python",
            label="A simple LSTM for sequence classification",
            src=(
                "import tensorflow as tf\n\n"
                "model = tf.keras.Sequential([\n"
                "    tf.keras.layers.Embedding(input_dim=10000, output_dim=64),\n"
                "    tf.keras.layers.LSTM(64),\n"
                "    tf.keras.layers.Dense(1, activation=\"sigmoid\"),\n"
                "])\n"
                "model.compile(optimizer=\"adam\", loss=\"binary_crossentropy\", metrics=[\"accuracy\"])"
            ),
        ),
        example=(
            "A predictive maintenance system feeds a rolling window of sensor readings into an LSTM to forecast "
            "equipment failure — the model needs to weigh a gradual upward drift over the last few hours "
            "differently from a single momentary spike, which is exactly the kind of temporal pattern an LSTM's "
            "gating mechanism is designed to capture."
        ),
        best_practices=[
            "Normalize sequence inputs (especially for time series) — RNNs are sensitive to input scale just like other neural networks.",
            "Prefer LSTM or GRU over a vanilla RNN for anything beyond very short sequences; the extra complexity pays for itself almost immediately.",
            "Consider whether the problem actually needs sequence order at all before defaulting to an RNN — sometimes a simpler model with engineered lag features performs just as well and trains far faster.",
        ],
        pitfalls=[
            "Using a plain RNN on long sequences and being surprised when it fails to learn long-range dependencies.",
            "Feeding variable-length sequences into a model without proper padding and masking, corrupting the learned patterns.",
        ],
        prompts=[
            "Explain how LSTM gates decide what to remember and forget.",
            "When would a transformer be a better choice than an LSTM for my sequence problem?",
            "How do I handle variable-length sequences when batching for an RNN?",
        ],
    ),
    dict(
        id="transformers-basics",
        title="Transformers: The Architecture Behind Modern LLMs",
        hook="The single idea that made transformers dominant is attention — instead of processing a sequence step by step, the model looks at every position at once and learns which ones matter to each other.",
        explanation=(
            "Unlike RNNs, which process tokens sequentially, transformers process an entire sequence in "
            "parallel using self-attention: for every token, the model computes a weighted combination of all "
            "other tokens, where the weights reflect how relevant each one is to understanding this token in "
            "context. This lets a transformer directly relate the first and last word of a long paragraph in a "
            "single step, something an RNN could only do by carrying information through every step in between.\n\n"
            "Because self-attention has no inherent sense of order, positional encodings are added to give the "
            "model information about token position. Multi-head attention runs several attention computations in "
            "parallel, each potentially learning a different kind of relationship (grammatical structure, "
            "coreference, topical relevance), and their outputs are combined. This architecture, combined with "
            "massive scale, is the foundation of models like GPT, Claude, and BERT."
        ),
        code=dict(
            lang="python",
            label="Self-attention, conceptually simplified",
            src=(
                "import numpy as np\n\n"
                "# Simplified: attention score between two tokens\n"
                "# is roughly how aligned their query and key vectors are\n"
                "def attention_weights(query, keys):\n"
                "    scores = query @ keys.T / np.sqrt(keys.shape[-1])\n"
                "    exp_scores = np.exp(scores - scores.max())\n"
                "    return exp_scores / exp_scores.sum()   # softmax\n\n"
                "# In practice: use a pretrained transformer, not raw math\n"
                "from transformers import pipeline\n"
                "classifier = pipeline(\"sentiment-analysis\")\n"
                "classifier(\"This architecture changed everything.\")"
            ),
        ),
        example=(
            "When a transformer processes 'The trophy didn't fit in the suitcase because it was too big,' "
            "self-attention lets the model directly connect 'it' back to 'trophy' rather than 'suitcase' by "
            "weighing that relationship across the whole sentence at once, resolving an ambiguity that trips up "
            "simpler models."
        ),
        best_practices=[
            "Use the Hugging Face `transformers` library and pretrained checkpoints for real projects rather than implementing attention from scratch.",
            "Fine-tune a pretrained transformer on your specific task instead of training one from scratch — pretraining cost is enormous and rarely worth repeating.",
            "Pay attention to a model's context window (max token length) early in a project — it constrains what inputs are even possible to feed the model.",
        ],
        pitfalls=[
            "Assuming 'transformer' and 'chatbot' are the same thing — transformers power far more than conversational models, including vision and audio tasks.",
            "Ignoring token limits until a real input gets silently truncated in production.",
        ],
        prompts=[
            "Explain self-attention step by step with a short sentence as the example.",
            "What's the difference between an encoder-only, decoder-only, and encoder-decoder transformer?",
            "Why do transformers need positional encodings if RNNs didn't?",
        ],
    ),
]
