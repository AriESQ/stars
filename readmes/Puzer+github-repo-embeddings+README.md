# Training GitHub Repository Embeddings using Stars


<p align="center">
    <a href="https://puzer.github.io/github_recommender/">
        <img src="https://img.shields.io/badge/GitHub_Pages-Live_Demo-2ea44f?logo=github" alt="Live Demo" height="20">
    </a>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="https://huggingface.co/datasets/Puzer/github-stars"><img src="https://huggingface.co/datasets/huggingface/badges/resolve/main/dataset-on-hf-sm.svg" alt="Hugging Face Dataset" height="20"></a>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="https://colab.research.google.com/github/Puzer/github-repo-embeddings/blob/main/notebooks/inference.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" height="20"></a>
    <br>
    <br>
    <img src="./images/img_2.png" width="500" alt="screenshot">
    <br>
    <em>Semantic comparison of developer profiles from Demo</em>
</p>

# TL;DR
- **The Idea:** People use GitHub Stars as bookmarks. This is an excellent signal for understanding which repositories are semantically similar.
- **The Data:** Processed ~1TB of raw data from GitHub Archive (BigQuery) to build an interest matrix of 4 million developers.
- **The ML:** Trained embeddings for 300k+ repositories using Metric Learning (EmbeddingBag + MultiSimilarityLoss).
- **The Frontend:** Built a client-only demo that runs vector search (KNN) directly in the browser via WASM, with no backend involved.
- **The Result:** The system finds non-obvious library alternatives and allows for semantic comparison of developer profiles.

---

# Personal Motivation
Finishing ideas is usually harder than it looks. It's easy to build a prototype, but the real struggle begins afterwards: polishing the rough edges, writing the text, and setting up the demo. This project is my attempt to go the full distance and tie up one of these "loose ends."

I also started thinking about the nature of our GitHub Stars. We are used to treating them simply as bookmarks "for later." But in reality, they are a valuable digital asset. They are a snapshot of our professional interests and skills. I wondered: can we put this passive asset to work? Can we use the accumulated knowledge of millions of developers to build a repository recommendation system and allow people to compare their technical interests?

And let's be honest: social validation is nice. If you enjoy this post or the demo, please Star the repo and/or [Follow](https://github.com/Puzer) me on GitHub. It’s the best signal that I should keep writing texts like this.

*My next post will be about [RL in LLMs (TRL + FunctionGemma + GRPO)](https://github.com/Puzer/Finetuning-LLM-agent-using-RL).*

---

# The Concept
## Cluster Hypothesis
The people reading this article are much more similar to you in interests than a randomly selected person from the street. In our universe, similar things often appear in similar contexts.

We intuitively sense these "hidden" preferences. If you see a new colleague typing in Vim and successfully exiting it without help, you've probably already built a mental vector of their interests: you can likely discuss patching KDE2 under FreeBSD with them, but asking for advice on an RGB gaming mouse might be a miss.

## Repo Representation
Let's apply this to repositories. We want to obtain a space where semantically similar repos are located close to each other.

To simplify, imagine a 2D space where the position depends on two main characteristics:
- **Axis X:** Data (Preparation & Analysis) vs Models (Training & Inference).
- **Axis Y:** Local / Single-node vs Big Data / Cluster.

<p align="center">
  <img src="./images/img_1.jpg" width="600" alt="semantic quadrants">
</p>

In reality, the neural network learns these axes (features) itself. They aren't always interpretable by humans, but the mathematical essence remains: similar repos are pulled together into clusters based on some learned features.

With these vectors, we can:
*   Search for similar repositories using **Cosine Similarity** (measuring the angle between vectors).
*   Obtain a user interest vector by simply averaging the vectors of their **starred** repositories.
*   Compare user profiles with each other.
---

# Signal Source
To get quality vectors, I used a hybrid approach.

### 1. Text (README.md) - For Initialization
Many repositories have a README. This is a great source for a "cold start". I used the [**Qwen3-Embedding-0.6B**](https://github.com/QwenLM/Qwen3-Embedding/blob/44548aa5f0a0aed1c76d64e19afe47727a325b8f/examples/qwen3_embedding_transformers.py#L54) model, which supports **MRL (Matryoshka Representation Learning)**, keeping only the first **128D** (the most important components). I used these vectors as the *initial weight initialization* for the trainable model.  
*Note:* This step adds about 10% to the final quality. To avoid overcomplicating the code with extra dependencies, I skipped this step in the public repo—the model learns perfectly fine from scratch (random init), just a bit slower.

### 2. Stars Matrix - For Main Training
Text is good, but it doesn't show how tools are used *together*. This is where collaborative filtering comes into play.

> | User | Starred repositories |
> | --- | --- |
> | A | Pandas, Dask, SK-Learn, Numpy |
> | B | Vue, React, TypeScript, Vite |

There are many approaches to training on such data: graph algorithms (LightGCN) or matrix factorization. I chose **Metric Learning** because it requires fewer GPU resources (1xGPU with ~8GB) and offers flexibility in managing the vector space.

---

# Data Preparation
Data was sourced from the public [GitHub Archive](https://www.gharchive.org/#bigquery) dataset in BigQuery.
I needed two queries:
1.  **Stars (WatchEvent):** Collect users with 10 to 800 stars (filtering out bots and inactive users). Preserving the order of stars.
2.  **Meta (PushEvent):** Collect repository names, commit dates, and descriptions.

In total, the queries processed about 1 TB of data and almost fit within the BigQuery Free Tier. The output was a Parquet file with ~4 million users and ~2.5 million unique repositories.

---

# Training Vectors
## Model Choice
I wanted to make the solution as lightweight as possible for the browser, so I immediately ruled out Transformers.
My model is a classic `torch.nn.EmbeddingBag`. Essentially, it's just a large lookup table `repo_id -> vector[128]` that can efficiently aggregate (average) vectors.

## Sampling and Loss Function
How do we explain to the neural network that Pandas and Numpy are "close"?

I split each user's list of stars into two random, non-overlapping "buckets" and used `EmbeddingBag` to calculate aggregated embedding of each bucket.

| User | Bucket | Repos in bucket | Mean(Embeddings in Bucket)
| --- | --- | --- | --- |
| A | A1 |  Numpy, Dask, SciPy| [0.2, -1.1, 0.9, ...]
| A | A2 | Pandas, SK-Learn| [0.1, -1.3, 0.6, ...]
| B | B1 | Vue, Vite| [-0.4, 0.6, 0.2, ...]
| B | B2 | React, TypeScript| [-0.3, 0.7, 0.1, ...]

We train embeddings so that two conditions are met *simultaneously*:
1.  Buckets from the same user are as close as possible (A1 <-pull-> A2).
2.  Buckets from different users are as far apart as possible (B1 <-push-> A2).

Obviously, the model cannot perfectly satisfy both conditions simultaneously for all users. However, by balancing these two forces, gradient descent attempts to adjust the repository vectors to minimize the overall error.

For the loss function, [**MultiSimilarityLoss**](https://kevinmusgrave.github.io/pytorch-metric-learning/losses/#multisimilarityloss) from the `pytorch-metric-learning` library performed the best.

> Note: Here, we should pay tribute to [StarSpace](https://github.com/facebookresearch/StarSpace), which pioneered this concept 8 years ago.

## Advanced Methods vs. Simplicity
It was logical to assume that the *sequence* of stars (the order in which you star repos) holds a strong signal, so I tried approaches à la Word2Vec (sliding window).

Surprisingly, **the simplest random split worked best**. Perhaps the timing data is too noisy, or I simply failed to extract value from it.

I also tried Hard Negative Miners, some other losses e.g. NTXentLoss (uses 4x more memory than MS, CrossBatchMemory didn't help) - but nothing managed to beat the original baseline.

Sometimes in ML, Occam's razor wins. And sometimes you realize that either the razor is dull, or you are.

---

# Quality Evaluation
We have vectors, but are they any good?  
One could use synthetic data from an LLM, but I found a more elegant Ground Truth—**Awesome Lists**. There are thousands of repositories on GitHub like "Awesome Python" or "Awesome React." These are human-curated clusters of similar libraries.
I downloaded the READMEs of these lists, found collocations (which repos appear together), applied heuristic weighting, and used the NDCG metric to evaluate ranking. This allowed me to fairly compare different loss functions, hyperparameters, and sampling methods.

---

# Frontend: Showcase & AI-Assisted Dev
Despite my 10 years of experience in Data Science, I am not an expert in frontend development. So the challenge was: build complex client-side logic without a backend, while not being a JS developer.

The entire frontend and "glue" code was written with the help of an **AI Coding Agent**.

## Architecture
1.  **Data:** The client downloads compressed embeddings (FP16, ~80 MB) and metadata, caching them in IndexedDB.
2.  **Search (WASM):** Uses the core of the [USearch](https://github.com/unum-cloud/USearch) library, compiled to WebAssembly.

## Low-level Magic
Initially, I wanted to use a pre-calculated HNSW index, but it consumed more memory than raw embeddings.
So I asked the agent to try implementing Exact Search (still using WASM).
The agent found the low-level `_usearch_exact_search` methods and generated a worker (`coreWorker.js`) that manually manages memory, allocates buffers via `_malloc`, and juggles pointers.
Browsers still don't handle native FP16 well, so the agent also had to write an on-the-fly FP16 -> FP32 converter for reading vectors. To me, this looks like magic, but it works fast even on 300k vectors, without HNSW indexes.

## User Profile & Skill Radar
Any demo becomes more engaging if it reveals something personal about the user. That’s why I added profile analytics.

### User Embedding
The math here is simple but effective:
1.  The client queries the GitHub API to fetch your starred repositories.
2.  We take the embeddings of these repositories and average them.
3.  The resulting **mean vector** is a digital fingerprint of your interests. Since it resides in the same metric space as the repositories, we can search for libraries that are "nearest" to you.

### Skill Radar (Interpreting the Vector)
Staring at 128 raw numbers is boring. I wanted to visualize skills RPG-style.
To create the radar axes (e.g., "GenAI", "Web3", "System Programming"), I used an LLM trick:
1.  I asked an LLM to generate lists of 20 "reference" repositories for 10 different categories.
2.  I trained simple **Logistic Regressions (Linear Probes)** to distinguish the vectors of these categories.
3.  Now, the browser simply passes the user vector through these models to generate probability scores for the chart.
4. It works since repos and user embeddings lives in the same space.

### Serverless Sharing
To add a social element, I pre-calculated vectors for famous developers.
The comparison uses Cosine Similarity, but with a twist. People struggle with abstract metrics (what does "0.6 similarity" actually mean?).
So, I applied a **Quantile Transformation**: instead of raw cosine scores, we display percentiles. A "95% Match" means you are more similar to this person than 95% of random pairs.

To let you compare yourself with other people, I implemented **Serverless Sharing**: the user vector is compressed, Base64-encoded, and embedded directly into the URL fragment identifier (hash). No database, no backend—just pure client-side math.

---

# Results: Expectations vs. Reality
Besides metrics, I verified the model with the "eyeball test."

**What didn't work:**
I hoped for beautiful vector arithmetic, like in NLP (`King - Man + Woman = Queen`).
Hypothesis: `Pandas - Python + TypeScript = Danfo.js`.
Reality: This didn't work. The repository vector space turned out to be more complex, and simple linear operations don't yield such interpretable results.
Also, I hoped for a distinct cluster structure of embeddings, but unfortunately, it doesn't look very pronounced visually.

**What worked:**
The main goal was achieved—the search finds alternatives I didn't know about, but which are semantically relevant.
Unlike LLMs, which often have a bias towards the most popular solutions, this approach, based on the *behavior* of IT professionals, digs up:
1.  **Niche Tools:** Libraries used by pros but rarely written about in blogs.
2.  **Fresh Solutions:** Repositories that gained popularity recently and share a similar "starring pattern."
3.  **Local-first:** Everything runs locally on client devices.

# Future Vision
The current demo is showing what is possible without a backend. But you can think about other use-cases:

1.  **Semantic Text Search:**
    Theoretically, one could take a text encoder and train a projection layer into the repository embedding space. This would allow searching for tools or people by abstract description.

2.  **GitHub Tinder (Networking):**
    With user vectors, we can match people.
    - Looking for a mentor or co-founder? The algorithm finds a person with a complementary stack.
    - Looking for a contributor? You can find developers who actively "star" similar projects but haven't seen yours yet.
    - HR Tech use-cases for position/candidate matching

3.  **Trend Analytics:**
    By adding a time dimension, we can visualize the evolution of technology. We could spot the birth of a new trend before it hits Hacker News. Though, this might be a chicken and egg problem :)

# Final Words
After 3+ years of working with LLMs, I wanted to take a step back, "shake off the rust" and revisit classical approaches. I also wanted to show that "good old" embeddings can still be useful in a world that seems to revolve entirely around GenAI.

> If you have questions, liked the article/demo, or want to leave a comment, please join the [GitHub Discussions](https://github.com/Puzer/github-repo-embeddings/discussions/1)!
