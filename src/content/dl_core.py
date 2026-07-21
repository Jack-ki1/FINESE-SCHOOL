"""Deep Learning subtopics — enriched schema."""

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
            "or no activation (linear) for regression.\n\n"
            "Variants of ReLU address a specific failure mode called 'dying ReLU', where a neuron gets stuck "
            "always outputting zero (and therefore never updates, since its gradient is also zero in that "
            "region) — Leaky ReLU allows a small non-zero slope for negative inputs specifically to keep "
            "gradients flowing even when a neuron's weighted sum goes negative."
        ),
        deep_dive=(
            "Sigmoid and tanh activations squash their output into a bounded range (0 to 1, or -1 to 1), which "
            "made them historically popular but causes a specific problem in deep networks: for very large or "
            "very small inputs, these functions' gradients approach zero, and during backpropagation "
            "(explained in its own lesson) that tiny gradient gets multiplied across every layer, shrinking "
            "toward zero exponentially fast in a deep network — the vanishing gradient problem, which "
            "effectively stops early layers of a deep network from learning anything meaningful.\n\n"
            "Softmax specifically converts a vector of raw scores (logits) into a valid probability "
            "distribution — every output is between 0 and 1, and all outputs sum to exactly 1 — by "
            "exponentiating each score and dividing by the sum of all exponentiated scores, which also has the "
            "effect of exaggerating differences between the largest score and the rest.\n\n"
            "Weight initialization strategy needs to match the chosen activation function for a network to "
            "train reliably from the start — He initialization (scaling initial random weights based on the "
            "number of inputs to a layer) is designed specifically to work well with ReLU-family activations, "
            "while Xavier/Glorot initialization was designed for sigmoid/tanh; using a mismatched "
            "initialization can make a network fail to train at all, or train much more slowly than it should."
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
        advanced_code=dict(
            lang="python",
            label="Softmax converting scores into a probability distribution",
            src=(
                "import numpy as np\n\n"
                "def softmax(scores):\n"
                "    exp_scores = np.exp(scores - np.max(scores))   # subtract max for stability\n"
                "    return exp_scores / np.sum(exp_scores)\n\n"
                "logits = np.array([2.0, 1.0, 0.1])\n"
                "probabilities = softmax(logits)\n"
                "print(probabilities)          # e.g. [0.659, 0.242, 0.099]\n"
                "print(probabilities.sum())     # 1.0 -- always sums to exactly 1"
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
            "Watch for signs of dying ReLU (neurons stuck outputting zero) and consider Leaky ReLU if this becomes a training problem.",
        ],
        pitfalls=[
            "Using sigmoid or tanh throughout a deep network and running into vanishing gradients that stall training.",
            "Forgetting an activation function entirely on hidden layers, which collapses the network into an equivalent single linear layer.",
            "Mismatching weight initialization strategy with the chosen activation function, causing slow or failed training.",
        ],
        glossary=[
            dict(term="Activation function", definition="A non-linear function applied to a neuron's weighted sum, essential for a network to learn non-linear patterns."),
            dict(term="Vanishing gradient", definition="A problem where gradients shrink toward zero across many layers during backpropagation, effectively stopping early layers from learning."),
            dict(term="Softmax", definition="An activation converting a vector of raw scores into a valid probability distribution summing to 1, used for multi-class classification output layers."),
            dict(term="Dying ReLU", definition="A failure mode where a ReLU neuron gets stuck always outputting zero and stops updating, since its gradient is also zero in that region."),
        ],
        faq=[
            dict(q="Explain the vanishing gradient problem and why ReLU helps with it.", a="Sigmoid/tanh activations have gradients that approach zero for large or small inputs; multiplied across many layers during backpropagation, this shrinks toward zero exponentially, stalling early-layer learning. ReLU's gradient is a constant 1 for any positive input, avoiding this shrinkage."),
            dict(q="When would I use tanh instead of ReLU?", a="Tanh is occasionally still used in specific architectures (like certain recurrent network gates) where a bounded, zero-centered output is specifically useful, but for general hidden layers in modern deep networks, ReLU and its variants are the more common default."),
            dict(q="Walk through the math of a single neuron with actual numbers.", a="Given inputs [1.0, 2.0, 3.0], weights [0.2, -0.5, 0.1], and bias 0.4: weighted sum = (1.0*0.2) + (2.0*-0.5) + (3.0*0.1) + 0.4 = 0.2 - 1.0 + 0.3 + 0.4 = -0.1. Applying ReLU: max(0, -0.1) = 0."),
        ],
        quiz=[
            dict(
                question="Why is an activation function necessary between neural network layers?",
                options=["It's purely for computational speed", "Without it, stacking layers collapses mathematically into a single linear operation", "It's only needed for the output layer", "It prevents overfitting"],
                correct=1,
                explanation="A chain of purely linear transformations is itself linear, no matter how many layers — the non-linear activation function is what allows a deep network to represent genuinely non-linear patterns.",
            ),
        ],
        prompts=[
            "Explain the vanishing gradient problem and why ReLU helps with it.",
            "When would I use tanh instead of ReLU?",
            "Walk through the math of a single neuron with actual numbers.",
            "What causes dying ReLU, and how does Leaky ReLU address it?",
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
            "suffer vanishing or exploding gradients during this backward pass.\n\n"
            "Batch size — how many training examples are processed before each weight update — trades off "
            "gradient estimate quality against speed and memory: a larger batch gives a more accurate estimate "
            "of the true gradient (less noisy updates) but requires more memory and compute per step, while a "
            "smaller batch is noisier but updates more frequently and can sometimes help the optimizer escape "
            "poor local regions of the loss landscape."
        ),
        deep_dive=(
            "Adam (Adaptive Moment Estimation) is the most widely used optimizer in modern deep learning "
            "because it adapts the effective learning rate per parameter automatically, based on estimates of "
            "both the gradient's recent average (momentum) and its recent variance — this generally makes "
            "training more robust to a less-than-perfectly-tuned learning rate compared to plain stochastic "
            "gradient descent (SGD), which is why it's the sensible default starting point for most new "
            "projects.\n\n"
            "Learning rate schedules (reducing the learning rate over the course of training, either on a "
            "fixed schedule or when validation performance plateaus) are a common refinement on top of a base "
            "optimizer — starting with a larger learning rate to make fast initial progress, then reducing it "
            "to allow finer, more precise convergence as training progresses.\n\n"
            "Gradient clipping (capping the magnitude of gradients before they're used to update weights) is a "
            "standard defense against exploding gradients, particularly common in recurrent architectures — "
            "rather than trying to prevent the underlying cause entirely, clipping directly limits how large "
            "an update any single step can cause, keeping training numerically stable even if a particular "
            "batch would otherwise produce an unusually large gradient."
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
        advanced_code=dict(
            lang="python",
            label="Gradient clipping and a learning rate scheduler",
            src=(
                "optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)\n"
                "scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3)\n\n"
                "for epoch in range(epochs):\n"
                "    for inputs, labels in dataloader:\n"
                "        optimizer.zero_grad()\n"
                "        loss = loss_fn(model(inputs), labels)\n"
                "        loss.backward()\n"
                "        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)\n"
                "        optimizer.step()\n\n"
                "    val_loss = evaluate(model, val_loader)\n"
                "    scheduler.step(val_loss)   # reduce LR if val_loss plateaus"
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
            "Add a learning rate scheduler that reduces the rate when validation performance plateaus, rather than using one fixed rate for the entire training run.",
        ],
        pitfalls=[
            "Setting a learning rate too high and watching loss oscillate or diverge instead of decrease.",
            "Assuming a bug is in the model architecture when it's actually a data problem (unnormalized inputs, wrong labels) manifesting as bad gradients.",
            "Choosing an excessively large batch size that exceeds available memory, or one so small that training becomes needlessly noisy and slow to converge.",
        ],
        glossary=[
            dict(term="Backpropagation", definition="An efficient algorithm using the chain rule to compute how much each weight in a network contributed to the overall error."),
            dict(term="Learning rate", definition="A scaling factor controlling how large a step gradient descent takes when updating weights based on computed gradients."),
            dict(term="Adam optimizer", definition="A widely used optimizer that adapts the effective learning rate per parameter based on recent gradient statistics, generally more robust than plain SGD."),
            dict(term="Gradient clipping", definition="Capping the magnitude of gradients before applying a weight update, a standard defense against exploding gradients."),
        ],
        faq=[
            dict(q="Why did my training loss turn into NaN, and how do I fix it?", a="This is the classic symptom of exploding gradients — weight updates become so large that numbers overflow. Try gradient clipping, lowering the learning rate, checking for unnormalized input data, or verifying there isn't a division by zero or log of zero somewhere in a custom loss function."),
            dict(q="Explain backpropagation using the chain rule with a two-layer example.", a="For a two-layer network, the loss depends on the output layer's weights directly, and on the hidden layer's weights indirectly (through the output layer). The chain rule lets you compute the hidden layer's gradient by multiplying the output layer's gradient by how much the hidden layer's output affects the output layer's input — propagating the error backward one layer at a time."),
            dict(q="What's the difference between SGD, Adam, and RMSprop as optimizers?", a="Plain SGD updates weights using a fixed learning rate scaled by the raw gradient. RMSprop adapts the learning rate per parameter based on a running average of recent squared gradients. Adam combines RMSprop's adaptive learning rate idea with momentum (a running average of the gradient direction itself), generally making it the most robust default choice."),
        ],
        quiz=[
            dict(
                question="What is backpropagation primarily used to compute?",
                options=["The final model accuracy", "How much each weight contributed to the total error, via the chain rule", "The number of layers a network needs", "The learning rate to use"],
                correct=1,
                explanation="Backpropagation efficiently computes the gradient of the loss with respect to every weight in the network, which gradient descent then uses to update those weights.",
            ),
        ],
        prompts=[
            "Why did my training loss turn into NaN, and how do I fix it?",
            "Explain backpropagation using the chain rule with a two-layer example.",
            "What's the difference between SGD, Adam, and RMSprop as optimizers?",
            "How does gradient clipping prevent exploding gradients?",
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
            "`GlobalAveragePooling2D()`.\n\n"
            "Transfer learning — starting from a large network already pretrained on a huge, general image "
            "dataset (like ImageNet) and fine-tuning it on your specific, often much smaller dataset — is the "
            "standard practical approach for most real-world computer vision problems, since the early "
            "layers' learned edge/texture detectors transfer well across very different tasks and domains, "
            "saving enormous amounts of training time and data compared to training from scratch."
        ),
        deep_dive=(
            "The receptive field of a neuron (how much of the original input image influences its value) "
            "grows with network depth — a neuron in an early layer only 'sees' a small patch of the input "
            "image, while a neuron several layers deep effectively 'sees' a much larger region, because it's "
            "built from earlier neurons that each already saw a smaller patch. This growing receptive field is "
            "part of why deeper CNNs can recognize larger-scale patterns and whole objects, not just local "
            "textures.\n\n"
            "Data augmentation (randomly flipping, rotating, cropping, or color-shifting training images "
            "before each epoch) artificially expands the effective size and diversity of a training set "
            "without collecting new data, and is one of the most cost-effective ways to reduce overfitting for "
            "vision models, since it teaches the network that the same object is still the same object under "
            "minor real-world variations in presentation.\n\n"
            "Fine-tuning a pretrained model typically involves freezing the early layers (keeping their "
            "learned general features fixed) and only training the later layers (and a new final "
            "classification head) on your specific dataset — this is both faster and requires far less data "
            "than training an entire network from scratch, since the early general-purpose feature detectors "
            "don't need to be relearned for a new but related task."
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
        advanced_code=dict(
            lang="python",
            label="Transfer learning: freezing a pretrained base, training a new head",
            src=(
                "base_model = tf.keras.applications.MobileNetV2(\n"
                "    input_shape=(224, 224, 3), include_top=False, weights=\"imagenet\"\n"
                ")\n"
                "base_model.trainable = False   # freeze the pretrained feature detectors\n\n"
                "model = tf.keras.Sequential([\n"
                "    base_model,\n"
                "    tf.keras.layers.GlobalAveragePooling2D(),\n"
                "    tf.keras.layers.Dense(5, activation=\"softmax\"),   # new head, 5 custom classes\n"
                "])\n"
                "model.compile(optimizer=\"adam\", loss=\"categorical_crossentropy\")\n"
                "model.fit(train_data, epochs=10)   # trains only the new head initially"
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
            "Use data augmentation (flips, rotations, crops) to reduce overfitting, especially with a limited training set.",
        ],
        pitfalls=[
            "Feeding raw 0-255 pixel values into a network expecting normalized inputs, which slows or destabilizes training.",
            "Forgetting a Flatten or GlobalAveragePooling step between the convolutional base and a Dense classification head, causing a shape error.",
            "Training an entire pretrained backbone from the very first epoch instead of first training just the new head, risking destroying the useful pretrained features.",
        ],
        glossary=[
            dict(term="Convolutional layer", definition="A layer applying small, shared-weight filters across an image to detect local patterns like edges and textures."),
            dict(term="Pooling", definition="Down-sampling feature maps (commonly via max pooling) to reduce spatial size and add translation invariance."),
            dict(term="Receptive field", definition="The region of the original input that influences a given neuron's value, growing larger with network depth."),
            dict(term="Transfer learning", definition="Starting from a network pretrained on a large general dataset and fine-tuning it on a smaller, specific dataset."),
        ],
        faq=[
            dict(q="Explain how a convolutional filter detects an edge with a simple numeric example.", a="A simple edge-detecting filter might have positive weights on one side and negative on the other (like [-1, 0, 1]); sliding it across the image, it produces a large output wherever pixel intensity changes sharply (an edge) and near zero where pixels are uniform — the network learns filter weights like this automatically during training."),
            dict(q="When should I use transfer learning instead of training a CNN from scratch?", a="Almost always, unless you have a very large, task-specific labeled dataset and specific reasons your task differs fundamentally from natural images. Transfer learning saves enormous training time and data by reusing already-learned general-purpose feature detectors."),
            dict(q="What's the difference between MaxPooling and GlobalAveragePooling?", a="MaxPooling reduces spatial dimensions by a fixed factor (e.g., 2x2 pooling halves width and height), keeping the strongest activation in each region. GlobalAveragePooling collapses each entire feature map down to a single average value, producing a fixed-size vector regardless of the input image's spatial dimensions, commonly used right before a final classification layer."),
        ],
        quiz=[
            dict(
                question="Why do CNN filters share weights across the entire image instead of learning separate weights per pixel?",
                options=["To make the model use less memory only", "Because a useful pattern detector (like an edge detector) is equally useful anywhere in the image", "Shared weights are required by Keras", "It has no real benefit, just convention"],
                correct=1,
                explanation="Weight sharing exploits the fact that a feature like an edge or texture pattern is meaningful regardless of where it appears in the image, dramatically reducing the number of parameters compared to a fully-connected approach.",
            ),
        ],
        prompts=[
            "Explain how a convolutional filter detects an edge with a simple numeric example.",
            "When should I use transfer learning instead of training a CNN from scratch?",
            "What's the difference between MaxPooling and GlobalAveragePooling?",
            "How does data augmentation help reduce overfitting for image models?",
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
            "workloads, though RNNs remain relevant for many time series and streaming use cases.\n\n"
            "Bidirectional RNNs process a sequence in both directions (forward and backward) and combine both "
            "results, useful whenever the full sequence is available upfront (like a complete sentence for "
            "translation) and understanding a given position benefits from context on both sides — this "
            "doesn't apply to genuinely real-time, streaming scenarios where future values aren't available "
            "yet at prediction time."
        ),
        deep_dive=(
            "An LSTM cell maintains two separate pieces of state: the hidden state (similar to a plain RNN's "
            "output at each step) and a separate cell state, which acts as a more protected 'long-term memory' "
            "conveyor belt that gates can selectively write to, read from, and clear, without necessarily "
            "passing through a squashing activation function at every single step — this architectural detail "
            "is specifically what allows information to persist across many more time steps than a vanilla "
            "RNN can manage.\n\n"
            "GRUs simplify the LSTM's three-gate design (input, forget, output gates) down to two gates "
            "(reset and update), reducing the number of parameters and often training faster with comparable "
            "performance on many tasks — the choice between LSTM and GRU is frequently more about empirical "
            "testing on your specific data than a clear theoretical winner in every case.\n\n"
            "Teacher forcing is a training technique for sequence-generation tasks (like translation) where, "
            "during training, the model is fed the actual correct previous output as input for predicting the "
            "next step, rather than its own (possibly wrong) prediction — this speeds up and stabilizes "
            "training, but creates a train/inference mismatch (at actual inference time, the model must feed "
            "its own predictions back in) that techniques like scheduled sampling are designed to mitigate."
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
        advanced_code=dict(
            lang="python",
            label="A bidirectional LSTM for a task where the full sequence is available upfront",
            src=(
                "model = tf.keras.Sequential([\n"
                "    tf.keras.layers.Embedding(input_dim=10000, output_dim=64),\n"
                "    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),\n"
                "    tf.keras.layers.Dense(1, activation=\"sigmoid\"),\n"
                "])\n"
                "# Processes the sequence forward AND backward, concatenating both results --\n"
                "# only valid when the whole sequence is available at once (not real-time streaming)"
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
            "Use a bidirectional architecture only when the full sequence is genuinely available upfront, not for real-time streaming predictions.",
            "Consider whether the problem actually needs sequence order at all before defaulting to an RNN — sometimes a simpler model with engineered lag features performs just as well and trains far faster.",
        ],
        pitfalls=[
            "Using a plain RNN on long sequences and being surprised when it fails to learn long-range dependencies.",
            "Feeding variable-length sequences into a model without proper padding and masking, corrupting the learned patterns.",
            "Using a bidirectional layer for a genuinely real-time streaming task, where future values simply aren't available at prediction time.",
        ],
        glossary=[
            dict(term="Hidden state", definition="A vector an RNN carries forward through a sequence, summarizing information seen so far."),
            dict(term="LSTM (Long Short-Term Memory)", definition="An RNN variant using gating mechanisms and a separate cell state to preserve information across many more time steps than a vanilla RNN."),
            dict(term="GRU (Gated Recurrent Unit)", definition="A simplified alternative to LSTM using two gates instead of three, often training faster with comparable performance."),
            dict(term="Teacher forcing", definition="A training technique feeding the true previous output (rather than the model's own prediction) as input during sequence generation training."),
        ],
        faq=[
            dict(q="Explain how LSTM gates decide what to remember and forget.", a="An LSTM has a forget gate (deciding what to discard from the cell state), an input gate (deciding what new information to add), and an output gate (deciding what to output based on the current cell state) — each is a small learned neural network layer producing values between 0 and 1 that scale how much information passes through at each step."),
            dict(q="When would a transformer be a better choice than an LSTM for my sequence problem?", a="Transformers generally outperform LSTMs on tasks with long sequences and available parallel compute, since self-attention processes the whole sequence at once rather than step-by-step, and can directly relate distant positions without the sequential bottleneck an RNN has. LSTMs can still be a reasonable, simpler choice for smaller-scale or genuinely streaming, real-time sequential tasks."),
            dict(q="How do I handle variable-length sequences when batching for an RNN?", a="Pad shorter sequences with a designated padding value up to the longest sequence in the batch, and use a masking layer (or masking parameter) so the network ignores the padded positions during both the forward pass and loss computation."),
        ],
        quiz=[
            dict(
                question="What core problem do LSTM and GRU architectures solve compared to a vanilla RNN?",
                options=["They train faster on any hardware", "They mitigate vanishing gradients, allowing information to persist across many more time steps", "They eliminate the need for an activation function", "They only work with image data"],
                correct=1,
                explanation="Gating mechanisms in LSTMs and GRUs let information flow across long sequences without vanishing, addressing vanilla RNNs' core limitation with long-range dependencies.",
            ),
        ],
        prompts=[
            "Explain how LSTM gates decide what to remember and forget.",
            "When would a transformer be a better choice than an LSTM for my sequence problem?",
            "How do I handle variable-length sequences when batching for an RNN?",
            "What's the practical difference between choosing an LSTM versus a GRU?",
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
            "massive scale, is the foundation of models like GPT, Claude, and BERT.\n\n"
            "Encoder-only architectures (like BERT) are optimized for understanding tasks — producing rich "
            "representations of input text for classification or extraction. Decoder-only architectures (like "
            "GPT-family models) are optimized for generation — predicting the next token repeatedly to produce "
            "new text. Encoder-decoder architectures (like the original Transformer, and T5) combine both, "
            "commonly used for tasks like translation where you need to fully understand an input before "
            "generating a related but different output sequence."
        ),
        deep_dive=(
            "Self-attention computes, for each token, a Query vector, a Key vector, and a Value vector "
            "(learned linear projections of that token's representation). The attention weight between two "
            "tokens is computed from how well one token's Query aligns with another's Key (typically a scaled "
            "dot product), and the final output for a token is a weighted sum of every token's Value vector, "
            "weighted by those alignment scores — this Query/Key/Value framing is the mathematical core "
            "underlying every transformer variant.\n\n"
            "Multi-head attention runs this entire Query/Key/Value process several times in parallel with "
            "different learned projections, letting different 'heads' specialize in different kinds of "
            "relationships — one head might learn to track subject-verb agreement, another might track "
            "long-range topical relevance — and their outputs are concatenated and combined, giving the model "
            "a richer overall representation than a single attention computation could provide.\n\n"
            "Computational cost is a genuine practical constraint: standard self-attention's cost grows "
            "quadratically with sequence length (doubling the input length roughly quadruples the "
            "computation), which is why context window size is a meaningful engineering and cost trade-off, "
            "and why substantial research effort has gone into more efficient attention variants that scale "
            "more gently for very long sequences."
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
        advanced_code=dict(
            lang="text",
            label="Encoder-only vs. decoder-only vs. encoder-decoder",
            src=(
                "Encoder-only (e.g. BERT):\n"
                "  Good at: understanding, classification, extracting information\n"
                "  Sees the WHOLE input at once, in both directions\n\n"
                "Decoder-only (e.g. GPT-family, Claude):\n"
                "  Good at: generating text, one token at a time\n"
                "  Only sees PRIOR tokens when predicting the next one\n\n"
                "Encoder-decoder (e.g. original Transformer, T5):\n"
                "  Good at: transforming one sequence into a different one\n"
                "  (translation, summarization) -- encoder understands input,\n"
                "  decoder generates output referencing the encoded input"
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
            "Choose an architecture family (encoder-only, decoder-only, encoder-decoder) matched to whether your task is understanding, generation, or transformation.",
        ],
        pitfalls=[
            "Assuming 'transformer' and 'chatbot' are the same thing — transformers power far more than conversational models, including vision and audio tasks.",
            "Ignoring token limits until a real input gets silently truncated in production.",
            "Underestimating the quadratic cost growth of self-attention with sequence length when planning for very long input documents.",
        ],
        glossary=[
            dict(term="Self-attention", definition="A mechanism where every token in a sequence computes a weighted relationship to every other token, capturing context regardless of distance."),
            dict(term="Positional encoding", definition="Information added to token representations so a transformer, which has no inherent sense of order, knows each token's position in the sequence."),
            dict(term="Query/Key/Value", definition="Three learned vector projections of each token used to compute attention weights and combine information across a sequence."),
            dict(term="Multi-head attention", definition="Running several self-attention computations in parallel with different learned projections, letting the model capture different kinds of relationships simultaneously."),
        ],
        faq=[
            dict(q="Explain self-attention step by step with a short sentence as the example.", a="For the sentence 'The cat sat', each word computes a Query, and compares it against every word's Key to get attention scores (how relevant each word is to it). Those scores, turned into weights via softmax, determine how much of each word's Value vector contributes to the final representation — 'sat' might attend strongly to 'cat' since it's the subject performing the action."),
            dict(q="What's the difference between an encoder-only, decoder-only, and encoder-decoder transformer?", a="Encoder-only models see the whole input bidirectionally and excel at understanding/classification tasks. Decoder-only models generate text token by token, only attending to prior tokens. Encoder-decoder models combine both, first encoding a full input, then generating a related output sequence referencing that encoding — common for translation and summarization."),
            dict(q="Why do transformers need positional encodings if RNNs didn't?", a="RNNs process tokens sequentially, so order is implicitly built into how information flows through the network. Transformers process all tokens in parallel with no inherent sequential structure, so positional information has to be explicitly added to each token's representation for the model to know their relative order."),
        ],
        quiz=[
            dict(
                question="What is the key advantage of self-attention over an RNN's sequential processing?",
                options=["It uses less memory in every case", "It can directly relate any two positions in a sequence in one step, regardless of distance", "It doesn't require any training", "It only works on short sequences"],
                correct=1,
                explanation="Self-attention computes relationships between every pair of tokens directly and in parallel, letting a transformer connect distant tokens in one step, unlike an RNN which must carry information sequentially through every intermediate step.",
            ),
        ],
        prompts=[
            "Explain self-attention step by step with a short sentence as the example.",
            "What's the difference between an encoder-only, decoder-only, and encoder-decoder transformer?",
            "Why do transformers need positional encodings if RNNs didn't?",
            "Why does self-attention's computational cost grow quadratically with sequence length?",
        ],
    ),
]