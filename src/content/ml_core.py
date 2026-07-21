"""Machine Learning subtopics — enriched schema."""

SUBTOPICS = [
    dict(
        id="supervised-vs-unsupervised",
        title="Supervised vs. Unsupervised Learning",
        hook="The first question to ask about any ML problem isn't 'which algorithm' — it's 'do I have labeled examples of the right answer?'",
        explanation=(
            "Supervised learning trains a model on examples that already have the correct answer attached — "
            "photos labeled 'cat' or 'dog', houses with known sale prices. The model learns a mapping from input "
            "features to output labels, then applies that mapping to new, unlabeled inputs. It splits further "
            "into classification (predicting a category) and regression (predicting a continuous number).\n\n"
            "Unsupervised learning works with data that has no labels at all — the goal is to find structure "
            "the data itself suggests: groups of similar customers (clustering), the underlying dimensions "
            "driving variation in the data (dimensionality reduction), or unusual points that don't fit any "
            "pattern (anomaly detection). There's no 'correct answer' to check against, which also makes "
            "unsupervised results harder to evaluate objectively.\n\n"
            "Semi-supervised learning sits between the two — using a small amount of labeled data alongside a "
            "much larger amount of unlabeled data, common in situations where labeling is expensive (requiring "
            "expert human review) but raw unlabeled data is abundant. Self-supervised learning, a related but "
            "distinct idea underlying much of modern deep learning, generates its own labels automatically "
            "from the structure of the data itself (like predicting a masked word in a sentence), sidestepping "
            "the need for human-provided labels almost entirely during pretraining."
        ),
        deep_dive=(
            "The practical litmus test for 'is this problem supervised' is: could you, in principle, go back "
            "in time and collect the correct answer for every historical example in your dataset? Predicting "
            "next month's churn is supervised because you eventually observe whether a customer actually "
            "churned. Segmenting customers into behavioral groups is unsupervised because there's no "
            "objective 'correct' grouping to have collected in the first place — different reasonable people "
            "could produce different valid groupings.\n\n"
            "Reinforcement learning is a third major paradigm, distinct from both supervised and unsupervised "
            "learning — an agent learns by taking actions in an environment and receiving rewards or "
            "penalties, gradually learning a policy (a strategy for choosing actions) that maximizes "
            "cumulative reward over time, rather than learning from a fixed dataset of labeled examples at "
            "all. This is the paradigm behind game-playing AI and much of robotics control.\n\n"
            "Evaluating unsupervised results generally requires either a downstream task to validate against "
            "(do the discovered clusters actually predict something useful, like purchasing behavior), "
            "internal validity metrics (like silhouette score, measuring how well-separated clusters are from "
            "each other), or ultimately, domain expert judgment about whether the discovered structure makes "
            "business or scientific sense."
        ),
        code=dict(
            lang="python",
            label="Supervised (classification) vs. unsupervised (clustering)",
            src=(
                "from sklearn.linear_model import LogisticRegression\n"
                "from sklearn.cluster import KMeans\n\n"
                "# Supervised: we HAVE labels (y)\n"
                "clf = LogisticRegression().fit(X_train, y_train)\n"
                "predictions = clf.predict(X_test)\n\n"
                "# Unsupervised: no labels, just find structure\n"
                "kmeans = KMeans(n_clusters=4, n_init=10).fit(X)\n"
                "cluster_ids = kmeans.labels_    # discovered groups, not 'correct answers'"
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="The four major ML paradigms, side by side",
            src=(
                "Supervised:      Have labels     -> learn input -> label mapping\n"
                "Unsupervised:    No labels        -> find structure/patterns\n"
                "Semi-supervised: Few labels + lots of unlabeled data -> combine both\n"
                "Reinforcement:   No fixed dataset -> learn from reward/penalty via actions\n\n"
                "Litmus test for supervised vs unsupervised:\n"
                "  Could I have collected a 'correct answer' for every past example?\n"
                "  YES -> supervised.  NO (or no single correct answer exists) -> unsupervised."
            ),
        ),
        example=(
            "A churn model predicting 'will this customer cancel next month' is supervised — historical customers "
            "already have a known outcome. A customer segmentation project grouping users into behavioral tiers "
            "with no predefined categories is unsupervised — there's no ground truth for what the 'right' groups are."
        ),
        best_practices=[
            "Check whether reliable labels actually exist and are trustworthy before assuming a problem is supervised — mislabeled data quietly caps your model's ceiling.",
            "For unsupervised results, validate clusters against business intuition or a downstream metric, since there's no accuracy score to lean on.",
            "Consider semi-supervised or self-supervised approaches when you have a little labeled data and a lot of unlabeled data.",
            "Use the 'could I have collected a correct answer historically' test to quickly classify a new problem as supervised or unsupervised.",
        ],
        pitfalls=[
            "Treating a clustering result as if it were ground truth just because the algorithm assigned confident-looking group numbers.",
            "Forcing a supervised approach onto a problem where reliable labels don't actually exist yet.",
            "Confusing reinforcement learning with supervised learning simply because both involve 'training' a model on data.",
        ],
        glossary=[
            dict(term="Label", definition="The known correct answer attached to a training example in supervised learning."),
            dict(term="Semi-supervised learning", definition="Training using a small amount of labeled data alongside a much larger pool of unlabeled data."),
            dict(term="Reinforcement learning", definition="A paradigm where an agent learns a policy by taking actions and receiving rewards or penalties, rather than learning from a fixed labeled dataset."),
            dict(term="Silhouette score", definition="An internal metric for evaluating clustering quality by measuring how well-separated clusters are from each other."),
        ],
        faq=[
            dict(q="Is customer lifetime value prediction supervised or unsupervised, and why?", a="Supervised — for historical customers, you can compute their actual realized lifetime value after the fact, giving you a genuine label to train against for predicting it for newer, still-active customers."),
            dict(q="How do I evaluate a clustering result when there's no ground truth?", a="Use internal validity metrics (like silhouette score) to check cluster separation quality, and more importantly, validate against a downstream business question — do the discovered groups actually differ meaningfully in behavior, spend, or another metric that matters?"),
            dict(q="What's the difference between classification and regression with real examples of each?", a="Classification predicts a category (spam vs. not spam, which of 5 product categories). Regression predicts a continuous number (predicted house price, predicted temperature tomorrow) — the type of output, category vs. number, is the defining difference."),
        ],
        quiz=[
            dict(
                question="Which of these problems is unsupervised?",
                options=["Predicting whether an email is spam", "Grouping customers into behavioral segments with no predefined categories", "Predicting a house's sale price", "Predicting next month's revenue"],
                correct=1,
                explanation="Customer segmentation with no predefined categories has no objective 'correct' grouping to train against, making it an unsupervised clustering problem rather than supervised.",
            ),
        ],
        prompts=[
            "Is customer lifetime value prediction supervised or unsupervised, and why?",
            "How do I evaluate a clustering result when there's no ground truth?",
            "What's the difference between classification and regression with real examples of each?",
            "How is reinforcement learning fundamentally different from supervised learning?",
        ],
    ),
    dict(
        id="train-test-split-cv",
        title="Train/Test Split & Cross-Validation",
        hook="A model's accuracy on the data it was trained on tells you almost nothing about how it'll perform on data it hasn't seen — which is the entire reason evaluation splits exist.",
        explanation=(
            "Splitting data into a training set and a held-out test set simulates 'future, unseen data' so you "
            "can estimate real-world performance honestly. The test set must never influence training in any "
            "way — no fitting a scaler on it, no using it to pick hyperparameters — or the estimate becomes "
            "optimistically biased, a problem known as data leakage.\n\n"
            "A single train/test split can be noisy, especially on small datasets, since performance depends "
            "partly on which rows happened to land in which split. K-fold cross-validation addresses this by "
            "splitting the training data into K folds, training K times (each time holding out a different fold "
            "as validation), and averaging the results — giving a more stable, reliable estimate of performance.\n\n"
            "A three-way split (train / validation / test) is standard practice for any workflow involving "
            "hyperparameter tuning or model selection: the training set fits the model, the validation set "
            "(or cross-validation over the training set) guides which hyperparameters or model to choose, and "
            "the test set is reserved purely for one final, honest performance estimate at the very end, "
            "touched exactly once."
        ),
        deep_dive=(
            "Nested cross-validation addresses a subtle leakage risk in ordinary cross-validation used for "
            "hyperparameter tuning: if you cross-validate purely to pick the best hyperparameters and then "
            "report that same cross-validation score as your final performance estimate, you're optimistically "
            "biased, because you specifically chose the hyperparameters that performed best on that data. "
            "Nested CV uses an outer loop for the final honest estimate and an inner loop purely for "
            "hyperparameter selection, keeping the two concerns properly separated.\n\n"
            "Group-based splitting matters whenever your data has natural groupings that shouldn't be split "
            "across train and test — if you have multiple rows per patient and want to predict something "
            "about new, unseen patients, randomly splitting individual rows can leak information (the model "
            "essentially 'sees' a version of a specific patient during training and gets an easier version of "
            "the same patient at test time), and `GroupKFold` or similar group-aware splitting strategies are "
            "necessary to properly simulate performance on genuinely new, unseen patients.\n\n"
            "Bootstrap resampling is an alternative evaluation approach to k-fold cross-validation, repeatedly "
            "drawing random samples with replacement from the training data to build many slightly different "
            "training sets, useful specifically for estimating the variability (confidence interval) of a "
            "performance metric, not just its average value."
        ),
        code=dict(
            lang="python",
            label="Cross-validation with scikit-learn",
            src=(
                "from sklearn.model_selection import train_test_split, cross_val_score\n"
                "from sklearn.ensemble import RandomForestClassifier\n\n"
                "X_train, X_test, y_train, y_test = train_test_split(\n"
                "    X, y, test_size=0.2, stratify=y, random_state=42\n"
                ")\n\n"
                "model = RandomForestClassifier(random_state=42)\n"
                "scores = cross_val_score(model, X_train, y_train, cv=5, scoring=\"f1\")\n"
                "print(f\"F1: {scores.mean():.3f} +/- {scores.std():.3f}\")\n\n"
                "model.fit(X_train, y_train)   # final fit before touching X_test"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Group-aware splitting to prevent leakage across related rows",
            src=(
                "from sklearn.model_selection import GroupKFold\n\n"
                "# Multiple rows per patient_id -- must not split the SAME patient\n"
                "# across both train and validation\n"
                "group_kfold = GroupKFold(n_splits=5)\n\n"
                "for train_idx, val_idx in group_kfold.split(X, y, groups=patient_ids):\n"
                "    X_train, X_val = X[train_idx], X[val_idx]\n"
                "    y_train, y_val = y[train_idx], y[val_idx]\n"
                "    # train and evaluate -- no patient appears in both sets"
            ),
        ),
        example=(
            "A model that scores 98% accuracy on training data but 61% on the test set isn't a great model — "
            "it's an overfit one that memorized the training rows rather than learning a generalizable pattern, "
            "and only the held-out test set exposed that gap."
        ),
        best_practices=[
            "Use `stratify=y` for classification splits with imbalanced classes so both splits keep the same class proportions.",
            "Reserve the test set for one final evaluation — use cross-validation on the training set for all model selection and tuning decisions.",
            "For time series data, split chronologically (train on the past, test on the future) instead of randomly, or you'll leak future information into training.",
            "Use group-aware splitting (GroupKFold) whenever multiple rows belong to the same real-world entity that shouldn't be split across sets.",
        ],
        pitfalls=[
            "Looking at test set performance repeatedly while tuning the model, which turns the test set into a de facto validation set and inflates the final estimate.",
            "Using a random split on time-ordered data, letting the model 'see the future' during training.",
            "Randomly splitting rows that belong to the same real-world group (like the same patient or customer) across train and test, leaking information between them.",
        ],
        glossary=[
            dict(term="Cross-validation", definition="Repeatedly splitting training data into folds, training and validating on different combinations, to get a more stable performance estimate than one single split."),
            dict(term="Nested cross-validation", definition="Using separate inner and outer cross-validation loops to properly separate hyperparameter tuning from the final honest performance estimate."),
            dict(term="GroupKFold", definition="A cross-validation strategy ensuring rows belonging to the same specified group never appear in both train and validation simultaneously."),
        ],
        faq=[
            dict(q="Why is repeatedly checking test set performance during tuning a form of leakage?", a="Every time you check the test score and adjust something in response, you're implicitly using that test data to guide decisions — even without directly training on it. Over many iterations, you end up selecting whatever configuration happens to perform best on that specific test set, inflating your final estimate."),
            dict(q="How should I split time series data differently from tabular data?", a="Split chronologically — train on earlier time periods, test on later ones — rather than randomly. A random split would let the model train on future data and be tested on the past, which doesn't reflect how the model will actually be used in production (predicting the future from the past)."),
            dict(q="Explain the difference between k-fold and stratified k-fold cross-validation.", a="Plain k-fold splits data into folds without regard to class balance, which can produce folds with very different class proportions on imbalanced data. Stratified k-fold specifically preserves the overall class proportions in every fold, giving more reliable, comparable results across folds for classification problems."),
        ],
        quiz=[
            dict(
                question="Why should time series data be split chronologically rather than randomly?",
                options=["It's faster to compute", "A random split could let the model train on future data and be tested on the past, unlike real-world use", "Chronological splitting is required by scikit-learn", "There's no real difference"],
                correct=1,
                explanation="In real deployment, a time series model predicts the future from the past — a random split breaks that structure, letting the model 'see' future information during training that wouldn't actually be available at prediction time.",
            ),
        ],
        prompts=[
            "Why is repeatedly checking test set performance during tuning a form of leakage?",
            "How should I split time series data differently from tabular data?",
            "Explain the difference between k-fold and stratified k-fold cross-validation.",
            "When do I need GroupKFold instead of regular cross-validation?",
        ],
    ),
    dict(
        id="data-leakage-pipelines",
        title="Data Leakage & Pipelines",
        hook="Leakage is the single most common reason a model looks great in testing and then falls apart in production — and a scikit-learn Pipeline is the cleanest defense against it.",
        explanation=(
            "Data leakage happens when information from outside the training data — often, indirectly, from the "
            "test set — influences model training, making performance look better than it will be in reality. "
            "The classic case: fitting a `StandardScaler` on the full dataset before splitting means the scaler's "
            "mean and standard deviation were computed partly from test rows, quietly leaking test information "
            "into every training example.\n\n"
            "A `Pipeline` bundles preprocessing steps and the model into a single object, and when used with "
            "`cross_val_score` or `GridSearchCV`, scikit-learn refits every step — including the scaler — inside "
            "each cross-validation fold using only that fold's training data. This makes leakage structurally "
            "hard to introduce by accident, rather than something you have to remember to avoid manually.\n\n"
            "Target leakage — a distinct and often more damaging form of leakage — happens when a feature is, "
            "directly or indirectly, a proxy for or derived from the target you're trying to predict, in a way "
            "that wouldn't actually be available at genuine prediction time. This is more insidious than "
            "train/test contamination because the model can look highly accurate throughout development and "
            "only fail once deployed against real, live data where that feature genuinely isn't available yet."
        ),
        deep_dive=(
            "A practical test for target leakage: for every feature, ask 'would I actually have this "
            "information at the exact moment I need to make this prediction in production?' A feature like "
            "'total refunds issued' when predicting whether an order will be fraudulent is a leak if refunds "
            "are typically only issued after the fraud has already been investigated and confirmed — the "
            "feature is only available *after* the answer is already known.\n\n"
            "`ColumnTransformer` extends the Pipeline concept to apply different preprocessing to different "
            "column types within a single fold-safe pipeline — numeric columns get scaled, categorical columns "
            "get one-hot encoded, all wired together and refit correctly per fold without manual bookkeeping.\n\n"
            "Feature importance or correlation analysis is a useful practical leakage detector: a feature with "
            "suspiciously overwhelming importance, or near-perfect correlation with the target, deserves "
            "scrutiny — it's not always leakage (sometimes a feature genuinely is that predictive), but it's a "
            "strong enough signal to warrant specifically checking whether that feature would actually be "
            "available at real prediction time."
        ),
        code=dict(
            lang="python",
            label="Pipeline prevents leakage automatically",
            src=(
                "from sklearn.pipeline import Pipeline\n"
                "from sklearn.preprocessing import StandardScaler\n"
                "from sklearn.impute import SimpleImputer\n"
                "from sklearn.linear_model import LogisticRegression\n"
                "from sklearn.model_selection import cross_val_score\n\n"
                "pipe = Pipeline([\n"
                "    (\"impute\", SimpleImputer(strategy=\"median\")),\n"
                "    (\"scale\", StandardScaler()),\n"
                "    (\"clf\", LogisticRegression()),\n"
                "])\n\n"
                "# Each fold refits impute + scale + clf using ONLY that fold's training rows\n"
                "scores = cross_val_score(pipe, X, y, cv=5)"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="ColumnTransformer for mixed numeric/categorical preprocessing",
            src=(
                "from sklearn.compose import ColumnTransformer\n"
                "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n\n"
                "preprocessor = ColumnTransformer([\n"
                "    (\"num\", StandardScaler(), [\"income\", \"age\"]),\n"
                "    (\"cat\", OneHotEncoder(handle_unknown=\"ignore\"), [\"region\", \"segment\"]),\n"
                "])\n\n"
                "full_pipeline = Pipeline([\n"
                "    (\"preprocess\", preprocessor),\n"
                "    (\"clf\", LogisticRegression()),\n"
                "])\n"
                "# Fold-safe: every fold refits BOTH the scaler and the one-hot encoder correctly"
            ),
        ),
        example=(
            "A fraud model that used the transaction's final 'confirmed fraud' database flag — set after human "
            "review, which happens after the transaction is already processed — as a feature scored 99% in "
            "testing and was useless in production, because that flag simply wouldn't exist yet at prediction time."
        ),
        best_practices=[
            "Ask of every feature: 'would this value actually be available at the moment I need to make the prediction?' — not just 'is it available in my historical dataset?'",
            "Wrap every fit-able preprocessing step (scalers, imputers, encoders) inside a Pipeline rather than applying them manually before the split.",
            "Be especially suspicious of features that are suspiciously predictive — extremely high performance is a common symptom of leakage, not just a good model.",
            "Use ColumnTransformer to keep mixed numeric/categorical preprocessing fold-safe within a single Pipeline object.",
        ],
        pitfalls=[
            "Target leakage: including a feature that's a proxy for, or downstream of, the outcome you're trying to predict.",
            "Fitting any transformer (scaler, encoder, imputer) on the full dataset once, before doing the train/test split.",
            "Dismissing suspiciously high accuracy as simply 'a good model' without specifically checking for leakage first.",
        ],
        glossary=[
            dict(term="Data leakage", definition="Information from outside the legitimate training data influencing model training, inflating apparent performance beyond what's achievable in real deployment."),
            dict(term="Target leakage", definition="A feature that's a proxy for, or only available after, the outcome being predicted — often more damaging than train/test contamination."),
            dict(term="ColumnTransformer", definition="A scikit-learn tool applying different preprocessing to different column subsets within a single fold-safe Pipeline."),
        ],
        faq=[
            dict(q="Is this feature likely to cause leakage: 'account_closed_date' when predicting churn?", a="Very likely yes — a customer's account_closed_date is essentially a direct encoding of whether (and often exactly when) they churned, making it a near-perfect proxy for the target rather than a genuine predictive feature available before the outcome is known."),
            dict(q="Rewrite this preprocessing code to use a Pipeline and prevent leakage.", a="Move every fit-able step (scaler, imputer, encoder) into a Pipeline (or ColumnTransformer feeding into a Pipeline) alongside the model, then pass that whole pipeline object into cross_val_score or GridSearchCV rather than fitting preprocessing separately beforehand."),
            dict(q="What's the difference between target leakage and train-test contamination?", a="Train-test contamination is fitting a preprocessing step on data that includes test rows, subtly biasing the evaluation. Target leakage is a specific feature being a proxy for, or derived from, the target itself — a more fundamental problem that can make a model appear excellent yet be useless in production, regardless of how carefully the train/test split was handled."),
        ],
        quiz=[
            dict(
                question="What's the most reliable way to prevent preprocessing steps from leaking test information into training?",
                options=["Manually remembering to fit only on training data every time", "Wrapping preprocessing and the model together in a scikit-learn Pipeline", "Using a larger test set", "Skipping preprocessing entirely"],
                correct=1,
                explanation="A Pipeline, combined with cross_val_score or GridSearchCV, automatically refits every preprocessing step within each fold using only that fold's training data, making leakage structurally difficult to introduce by accident.",
            ),
        ],
        prompts=[
            "Is this feature likely to cause leakage: 'account_closed_date' when predicting churn?",
            "Rewrite this preprocessing code to use a Pipeline and prevent leakage.",
            "What's the difference between target leakage and train-test contamination?",
            "How do I use ColumnTransformer for a dataset with both numeric and categorical columns?",
        ],
    ),
    dict(
        id="feature-engineering",
        title="Feature Engineering",
        hook="A simple model with well-crafted features regularly beats a complex model fed raw, unprocessed data — features are usually where the real modeling work happens.",
        explanation=(
            "Feature engineering is the process of transforming raw data into inputs that better expose the "
            "patterns a model needs to learn. This includes encoding categorical variables (one-hot or target "
            "encoding), scaling numeric ranges, extracting components from dates (day of week, is-holiday), "
            "combining columns into ratios or interaction terms, and handling missing values thoughtfully rather "
            "than dropping them by default.\n\n"
            "Different model families need different treatment: tree-based models (Random Forest, XGBoost) are "
            "largely indifferent to feature scale and can handle raw categorical codes reasonably well, while "
            "linear models and neural networks are sensitive to scale and need properly encoded categories to "
            "perform well at all.\n\n"
            "Interaction features — combining two existing features into a new one (like `price_per_sqft = "
            "price / square_feet`) — can expose a relationship a model wouldn't otherwise easily discover on "
            "its own, especially for simpler model types that can't automatically learn arbitrary non-linear "
            "combinations of raw inputs the way a deep enough tree ensemble or neural network sometimes can."
        ),
        deep_dive=(
            "Target encoding (replacing a categorical value with the mean of the target variable for that "
            "category) can be a powerful feature for high-cardinality categorical columns where one-hot "
            "encoding would create too many columns, but it carries a genuine leakage risk if not done "
            "carefully — computing the target mean using the same rows you're encoding leaks target "
            "information directly into the feature, which is why proper target encoding implementations use "
            "cross-validation internally (encoding each fold using target means computed only from the other "
            "folds).\n\n"
            "Binning (converting a continuous variable into discrete buckets, like turning exact age into age "
            "ranges) can help simpler models capture non-linear relationships and can also help with outlier "
            "robustness, at the cost of losing some information compared to keeping the original continuous "
            "value — a genuine trade-off to consider deliberately rather than applying reflexively.\n\n"
            "Domain knowledge consistently outperforms generic, automated feature engineering for most "
            "real-world business problems — an engineered feature like 'days since last purchase' or 'ratio "
            "of this month's spend to the customer's 3-month average' encodes understanding of what actually "
            "drives the business outcome, something a purely automated feature generation process has no way "
            "to know without that context."
        ),
        code=dict(
            lang="python",
            label="Encoding categories and engineering a date feature",
            src=(
                "import pandas as pd\n"
                "from sklearn.preprocessing import OneHotEncoder\n\n"
                "df[\"day_of_week\"] = df[\"order_date\"].dt.dayofweek\n"
                "df[\"is_weekend\"] = df[\"day_of_week\"].isin([5, 6]).astype(int)\n"
                "df[\"price_per_unit\"] = df[\"total_price\"] / df[\"quantity\"]\n\n"
                "encoder = OneHotEncoder(handle_unknown=\"ignore\", sparse_output=False)\n"
                "category_encoded = encoder.fit_transform(df[[\"category\"]])"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Leakage-safe target encoding within cross-validation",
            src=(
                "from category_encoders import TargetEncoder\n"
                "from sklearn.pipeline import Pipeline\n"
                "from sklearn.model_selection import cross_val_score\n\n"
                "# TargetEncoder, wrapped in a Pipeline, is refit correctly PER FOLD --\n"
                "# each fold's encoding uses only that fold's training target values\n"
                "pipe = Pipeline([\n"
                "    (\"encode\", TargetEncoder(cols=[\"zip_code\"])),   # high-cardinality column\n"
                "    (\"clf\", RandomForestClassifier()),\n"
                "])\n"
                "scores = cross_val_score(pipe, X, y, cv=5)"
            ),
        ),
        example=(
            "A demand-forecasting model improved noticeably not from switching algorithms but from adding a "
            "single engineered feature — 'days until next public holiday' — because that single number captured "
            "a strong, otherwise-invisible driver of purchasing spikes that raw calendar dates couldn't express directly."
        ),
        best_practices=[
            "Engineer features guided by domain knowledge first, then let feature-importance analysis confirm or challenge your assumptions.",
            "Use `handle_unknown='ignore'` on one-hot encoders so categories unseen during training don't crash predictions in production.",
            "Fit any encoder or scaler only on the training fold (inside a Pipeline) to avoid leaking category or scale information from test data.",
            "Use target encoding, when needed for high-cardinality categoricals, only through an implementation that's properly leakage-safe within cross-validation.",
        ],
        pitfalls=[
            "One-hot encoding a high-cardinality column (like zip code) without limits, exploding the feature space and hurting model performance.",
            "Engineering a feature that's only computable after the outcome is known, accidentally reintroducing target leakage.",
            "Computing target encoding naively on the full dataset before splitting, leaking target information directly into the encoded feature.",
        ],
        glossary=[
            dict(term="One-hot encoding", definition="Representing a categorical variable as multiple binary columns, one per category, indicating presence/absence."),
            dict(term="Target encoding", definition="Replacing a categorical value with a statistic (typically the mean) of the target variable for that category, useful for high-cardinality columns but leakage-prone if done naively."),
            dict(term="Interaction feature", definition="A new feature created by combining two or more existing features, exposing a relationship the model might not otherwise easily learn."),
            dict(term="Binning", definition="Converting a continuous variable into discrete buckets/ranges, trading some information for potential robustness or interpretability."),
        ],
        faq=[
            dict(q="How should I encode a categorical column with 500 unique values?", a="One-hot encoding would create 500 new columns, which is often impractical. Target encoding (done in a leakage-safe way) or embedding-based approaches (for deep learning models) are common alternatives for high-cardinality categorical columns."),
            dict(q="Suggest engineered features for predicting flight delays.", a="Time-based features (day of week, hour of day, holiday proximity), weather at departure/arrival airports, historical average delay for that specific route and airline, aircraft turnaround time from its previous flight, and airport congestion metrics are all strong candidates worth engineering."),
            dict(q="What's the difference between one-hot encoding and target encoding, and when is each appropriate?", a="One-hot encoding creates a binary column per category, working well for low-to-moderate cardinality with no risk of leakage. Target encoding compresses a category into a single number based on target statistics, better for high-cardinality columns, but requires careful, leakage-safe implementation to avoid biasing the model."),
        ],
        quiz=[
            dict(
                question="What's the main risk of naive target encoding?",
                options=["It only works with numeric targets", "Computing the encoding using the same rows being encoded leaks target information into the feature", "It always performs worse than one-hot encoding", "It can't be used with tree-based models"],
                correct=1,
                explanation="If you compute a category's target mean using the very rows you're then encoding, you're leaking direct target information into that feature — proper implementations use cross-validation internally to avoid this.",
            ),
        ],
        prompts=[
            "How should I encode a categorical column with 500 unique values?",
            "Suggest engineered features for predicting flight delays.",
            "What's the difference between one-hot encoding and target encoding, and when is each appropriate?",
            "Why is naive target encoding a leakage risk, and how do I do it safely?",
        ],
    ),
    dict(
        id="model-evaluation-metrics",
        title="Model Evaluation: Choosing the Right Metric",
        hook="Accuracy is the most commonly misused metric in machine learning — on imbalanced data it can look great while the model is nearly useless.",
        explanation=(
            "For classification, accuracy (percent correct) is misleading whenever classes are imbalanced: a "
            "model that always predicts 'not fraud' on a dataset that's 99% not-fraud scores 99% accuracy while "
            "catching zero actual fraud. Precision (of what I flagged as positive, how much was right) and "
            "recall (of all actual positives, how much did I catch) capture the trade-off that matters in these "
            "cases, and F1 balances the two into a single number.\n\n"
            "For regression, MAE (mean absolute error) is easy to interpret in the original units, while RMSE "
            "(root mean squared error) penalizes large errors more heavily — useful when big misses are "
            "disproportionately costly. The right metric always follows from the actual cost of different kinds "
            "of mistakes in the specific business context, not from convention.\n\n"
            "ROC AUC (area under the receiver operating characteristic curve) summarizes a classifier's ability "
            "to rank positive examples above negative ones across all possible decision thresholds, which makes "
            "it threshold-independent — useful for comparing models generally, but it can look deceptively good "
            "on heavily imbalanced data compared to precision-recall AUC, which focuses specifically on "
            "performance on the minority (often more important) class."
        ),
        deep_dive=(
            "The precision-recall trade-off is adjustable via the classification decision threshold — most "
            "classifiers output a probability, and the default 0.5 cutoff for 'positive' isn't necessarily "
            "optimal for a given business context. Lowering the threshold catches more true positives "
            "(higher recall) at the cost of more false positives (lower precision); raising it does the "
            "reverse — plotting the full precision-recall curve and choosing a threshold deliberately based "
            "on the actual costs of each error type is generally better than accepting the default.\n\n"
            "A confusion matrix (a table of true positives, false positives, true negatives, false negatives) "
            "underlies every one of these summary metrics and is worth inspecting directly, not just relying "
            "on a single derived number — it shows exactly which kind of mistake a model is making, "
            "information a single summary metric necessarily compresses away.\n\n"
            "For multi-class classification, precision, recall, and F1 need to be aggregated across classes "
            "somehow — macro-averaging (unweighted average across classes, treating every class equally "
            "regardless of size) and weighted-averaging (weighted by each class's frequency) can tell quite "
            "different stories on imbalanced multi-class problems, and choosing the wrong aggregation can hide "
            "poor performance on a minority class."
        ),
        code=dict(
            lang="python",
            label="Choosing metrics beyond accuracy",
            src=(
                "from sklearn.metrics import (\n"
                "    precision_score, recall_score, f1_score,\n"
                "    confusion_matrix, mean_absolute_error, mean_squared_error\n"
                ")\n\n"
                "print(\"Precision:\", precision_score(y_test, y_pred))\n"
                "print(\"Recall:\", recall_score(y_test, y_pred))\n"
                "print(\"F1:\", f1_score(y_test, y_pred))\n"
                "print(confusion_matrix(y_test, y_pred))\n\n"
                "# Regression\n"
                "mae = mean_absolute_error(y_test, y_pred_reg)\n"
                "rmse = mean_squared_error(y_test, y_pred_reg, squared=False)"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Choosing a decision threshold from the precision-recall curve",
            src=(
                "from sklearn.metrics import precision_recall_curve\n\n"
                "probabilities = model.predict_proba(X_test)[:, 1]\n"
                "precisions, recalls, thresholds = precision_recall_curve(y_test, probabilities)\n\n"
                "# Find the threshold achieving at least 90% recall\n"
                "import numpy as np\n"
                "idx = np.argmax(recalls >= 0.90)\n"
                "chosen_threshold = thresholds[idx]\n"
                "print(f\"Threshold for 90% recall: {chosen_threshold:.3f}, precision: {precisions[idx]:.3f}\")"
            ),
        ),
        example=(
            "A medical screening model is tuned to maximize recall even at the cost of precision, because "
            "missing an actual case (a false negative) is far more costly than a false alarm that gets ruled out "
            "by a follow-up test — the metric choice directly encodes that real-world asymmetry."
        ),
        best_practices=[
            "Choose the metric based on the real cost of false positives versus false negatives for the specific problem, before looking at any results.",
            "Always look at the confusion matrix alongside a single summary metric — one number can hide exactly which kind of mistake the model is making.",
            "For imbalanced classification, check precision-recall curves in addition to (or instead of) ROC curves, which can look misleadingly good on skewed data.",
            "Tune the classification decision threshold deliberately based on the precision-recall trade-off, rather than accepting the default 0.5 cutoff automatically.",
        ],
        pitfalls=[
            "Reporting accuracy as the headline metric on a dataset with significant class imbalance.",
            "Optimizing for a metric that doesn't reflect the actual business cost of different error types.",
            "Using macro-averaged metrics on an imbalanced multi-class problem without realizing they can mask poor performance on a small but important class.",
        ],
        glossary=[
            dict(term="Precision", definition="Of everything the model flagged as positive, what fraction was actually positive."),
            dict(term="Recall", definition="Of everything that was actually positive, what fraction did the model correctly identify."),
            dict(term="ROC AUC", definition="A threshold-independent measure of a classifier's ability to rank positives above negatives; can look deceptively good on imbalanced data."),
            dict(term="Confusion matrix", definition="A table breaking down predictions into true positives, false positives, true negatives, and false negatives."),
        ],
        faq=[
            dict(q="Which metric should I optimize for a loan default model, and why?", a="Depends on the specific business cost structure, but often recall-leaning if missing a genuine defaulter (false negative) costs more than incorrectly flagging a safe borrower (false positive) — though the exact balance should be set deliberately based on actual financial costs, not assumed."),
            dict(q="Explain precision and recall using a spam filter as the example.", a="Precision: of the emails flagged as spam, what fraction were actually spam (low precision means legitimate emails get wrongly blocked). Recall: of all the actual spam emails, what fraction did the filter catch (low recall means spam gets through to the inbox)."),
            dict(q="Why can ROC AUC look good even when a model performs poorly on the minority class?", a="ROC AUC's false positive rate is calculated relative to the (often huge) number of true negatives in an imbalanced dataset, which can stay low and make the curve look good even when the model catches very few of the (rare) true positives — precision-recall AUC is generally more informative in this specific situation."),
        ],
        quiz=[
            dict(
                question="Why is accuracy a poor primary metric for a highly imbalanced classification problem?",
                options=["Accuracy can't be computed for imbalanced data", "A model that always predicts the majority class can score high accuracy while catching none of the minority class", "Accuracy only works for regression", "It's actually the best metric in every case"],
                correct=1,
                explanation="On a dataset where 99% of examples are one class, always predicting that class yields 99% accuracy while providing zero value for detecting the minority class, which is usually the actual point of the model.",
            ),
        ],
        prompts=[
            "Which metric should I optimize for a loan default model, and why?",
            "Explain precision and recall using a spam filter as the example.",
            "Why can ROC AUC look good even when a model performs poorly on the minority class?",
            "How do I choose the right classification threshold for my specific business costs?",
        ],
    ),
]