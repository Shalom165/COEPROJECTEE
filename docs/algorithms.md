# Mathematical Algorithms & Ranking Formulas

## 1. Okapi BM25 Lexical Score
The BM25 score for a document $D$ given query $Q = \{q_1, q_2, \dots, q_n\}$ is calculated as:

$$\text{BM25}(D, Q) = \sum_{i=1}^{n} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$

Where:
- $f(q_i, D)$ is term frequency in document $D$
- $|D|$ is document length in words, and $\text{avgdl}$ is average document length across corpus
- $k_1 = 1.5$ and $b = 0.75$

## 2. Dense Semantic Vector Cosine Similarity
Using `SentenceTransformer('all-MiniLM-L6-v2')`, dense embedding vectors $\mathbf{u}$ and $\mathbf{v}$ are compared using cosine similarity:

$$\text{CosineSimilarity}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$

## 3. Freshness Score Exponential Decay
Document freshness decays exponentially with document age in days:

$$\text{Freshness}(t) = \exp(-\lambda \cdot t)$$

Where:
- $t = \text{today\_date} - \text{updated\_date}$ (in days)
- $\lambda = 0.003$ (half-life $\approx 231$ days)

## 4. Multi-Dimensional Evidence Ranking Formula
The final evidence score $S(D, Q)$ for candidate document $D$ is an interpretable weighted sum normalized between $0.0$ and $1.0$:

$$S(D, Q) = w_r \cdot S_{\text{rel}} + w_a \cdot S_{\text{auth}} + w_f \cdot S_{\text{fresh}} + w_p \cdot S_{\text{app}} + w_c \cdot S_{\text{cit}} + w_v \cdot S_{\text{rev}} + w_k \cdot S_{\text{conf}}$$

Active Prototype Weights:
- $w_r = 0.35$ (Hybrid BM25 + Vector Relevance)
- $w_a = 0.20$ (Authority Hierarchy)
- $w_f = 0.15$ (Freshness Decay)
- $w_p = 0.20$ (Approval Status Score)
- $w_c = 0.04$ (Citation Centrality)
- $w_v = 0.03$ (Revision Currentness)
- $w_k = 0.03$ (Conflict Penalty)

$$\sum w_i = 1.00$$
