"""Machine Learning subtopics."""

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
            "unsupervised results harder to evaluate objectively."
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
        example=(
            "A churn model predicting 'will this customer cancel next month' is supervised — historical customers "
            "already have a known outcome. A customer segmentation project grouping users into behavioral tiers "
            "with no predefined categories is unsupervised — there's no ground truth for what the 'right' groups are."
        ),
        best_practices=[
            "Check whether reliable labels actually exist and are trustworthy before assuming a problem is supervised — mislabeled data quietly caps your model's ceiling.",
            "For unsupervised results, validate clusters against business intuition or a downstream metric, since there's no accuracy score to lean on.",
            "Consider semi-supervised or self-supervised approaches when you have a little labeled data and a lot of unlabeled data.",
        ],
        pitfalls=[
            "Treating a clustering result as if it were ground truth just because the algorithm assigned confident-looking group numbers.",
            "Forcing a supervised approach onto a problem where reliable labels don't actually exist yet.",
        ],
        prompts=[
            "Is customer lifetime value prediction supervised or unsupervised, and why?",
            "How do I evaluate a clustering result when there's no ground truth?",
            "What's the difference between classification and regression with real examples of each?",
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
            "as validation), and averaging the results — giving a more stable, reliable estimate of performance."
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
        example=(
            "A model that scores 98% accuracy on training data but 61% on the test set isn't a great model — "
            "it's an overfit one that memorized the training rows rather than learning a generalizable pattern, "
            "and only the held-out test set exposed that gap."
        ),
        best_practices=[
            "Use `stratify=y` for classification splits with imbalanced classes so both splits keep the same class proportions.",
            "Reserve the test set for one final evaluation — use cross-validation on the training set for all model selection and tuning decisions.",
            "For time series data, split chronologically (train on the past, test on the future) instead of randomly, or you'll leak future information into training.",
        ],
        pitfalls=[
            "Looking at test set performance repeatedly while tuning the model, which turns the test set into a de facto validation set and inflates the final estimate.",
            "Using a random split on time-ordered data, letting the model 'see the future' during training.",
        ],
        prompts=[
            "Why is repeatedly checking test set performance during tuning a form of leakage?",
            "How should I split time series data differently from tabular data?",
            "Explain the difference between k-fold and stratified k-fold cross-validation.",
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
            "hard to introduce by accident, rather than something you have to remember to avoid manually."
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
        example=(
            "A fraud model that used the transaction's final 'confirmed fraud' database flag — set after human "
            "review, which happens after the transaction is already processed — as a feature scored 99% in "
            "testing and was useless in production, because that flag simply wouldn't exist yet at prediction time."
        ),
        best_practices=[
            "Ask of every feature: 'would this value actually be available at the moment I need to make the prediction?' — not just 'is it available in my historical dataset?'",
            "Wrap every fit-able preprocessing step (scalers, imputers, encoders) inside a Pipeline rather than applying them manually before the split.",
            "Be especially suspicious of features that are suspiciously predictive — extremely high performance is a common symptom of leakage, not just a good model.",
        ],
        pitfalls=[
            "Target leakage: including a feature that's a proxy for, or downstream of, the outcome you're trying to predict.",
            "Fitting any transformer (scaler, encoder, imputer) on the full dataset once, before doing the train/test split.",
        ],
        prompts=[
            "Is this feature likely to cause leakage: 'account_closed_date' when predicting churn?",
            "Rewrite this preprocessing code to use a Pipeline and prevent leakage.",
            "What's the difference between target leakage and train-test contamination?",
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
            "perform well at all."
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
        example=(
            "A demand-forecasting model improved noticeably not from switching algorithms but from adding a "
            "single engineered feature — 'days until next public holiday' — because that single number captured "
            "a strong, otherwise-invisible driver of purchasing spikes that raw calendar dates couldn't express directly."
        ),
        best_practices=[
            "Engineer features guided by domain knowledge first, then let feature-importance analysis confirm or challenge your assumptions.",
            "Use `handle_unknown='ignore'` on one-hot encoders so categories unseen during training don't crash predictions in production.",
            "Fit any encoder or scaler only on the training fold (inside a Pipeline) to avoid leaking category or scale information from test data.",
        ],
        pitfalls=[
            "One-hot encoding a high-cardinality column (like zip code) without limits, exploding the feature space and hurting model performance.",
            "Engineering a feature that's only computable after the outcome is known, accidentally reintroducing target leakage.",
        ],
        prompts=[
            "How should I encode a categorical column with 500 unique values?",
            "Suggest engineered features for predicting flight delays.",
            "What's the difference between one-hot encoding and target encoding, and when is each appropriate?",
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
            "of mistakes in the specific business context, not from convention."
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
        example=(
            "A medical screening model is tuned to maximize recall even at the cost of precision, because "
            "missing an actual case (a false negative) is far more costly than a false alarm that gets ruled out "
            "by a follow-up test — the metric choice directly encodes that real-world asymmetry."
        ),
        best_practices=[
            "Choose the metric based on the real cost of false positives versus false negatives for the specific problem, before looking at any results.",
            "Always look at the confusion matrix alongside a single summary metric — one number can hide exactly which kind of mistake the model is making.",
            "For imbalanced classification, check precision-recall curves in addition to (or instead of) ROC curves, which can look misleadingly good on skewed data.",
        ],
        pitfalls=[
            "Reporting accuracy as the headline metric on a dataset with significant class imbalance.",
            "Optimizing for a metric that doesn't reflect the actual business cost of different error types.",
        ],
        prompts=[
            "Which metric should I optimize for a loan default model, and why?",
            "Explain precision and recall using a spam filter as the example.",
            "Why can ROC AUC look good even when a model performs poorly on the minority class?",
        ],
    ),
]
