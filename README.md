# Kindred — Dating Recommendation Demo

A portfolio project combining an interactive dating discovery interface with an explainable recommendation engine and reproducible data science evaluation. **All 360 adult profiles are fictional.** No real user data is collected.

## Features
- Select a fictional member and explore personalized recommendations.
- Enforce the same city and reciprocal age preferences before ranking.
- Rank binary interest vectors with cosine similarity.
- Explain each recommendation through shared interests.
- Evaluate against a seeded random ranking baseline.
- Responsive HTML interface and a Python JSON API, using only the standard library.

## Run
Requires Python 3.10 or newer. No third-party packages, secrets or external services required.

```sh
python prepare.py
python -m unittest -v
python app.py --port 8000
```

Open the local server in your own browser. GitHub displays the source and documentation; it does not run the Python app. In cloud onboarding, use local HTTP requests to validate the service.

## Evaluation
A deterministic generator (seed 42) creates 360 fictional profiles in three Swedish cities. For each query, one interest is hidden; candidate relevance is the number of interests shared with the full original query profile. The engine sees only the remaining query interests. We compare NDCG@6 with a seeded random baseline over the same eligible pool.

| Ranking | Mean NDCG@6 |
| --- | ---: |
| Interest similarity | 0.815 |
| Random baseline | 0.323 |

All 360 queries were evaluated. Full machine-readable results: [metrics](outputs/metrics.json).

**Interpretation:** This is a constructed synthetic interest-recovery benchmark. The labels and ranking share an interest-based design, so the result is not evidence of attraction, real-world matching accuracy, fairness or dating success. No model is trained and no genuine behavioral test set is available. No sensitive personal attributes are inferred.

## Architecture
`prepare.py` → `data/profiles.json` + `outputs/metrics.json`

`index.html` → `app.py` JSON endpoints → `matching.py`

API endpoints: `GET /api/profiles`, `GET /api/matches?user=1`, `GET /api/metrics`. Invalid profile IDs return 400. The development server binds to loopback only.

## Scope
This completed portfolio demo supports discovery and ranking. It has no authentication, real users, messaging or production deployment. A production dating service would need consent, data retention controls, blocking/reporting, moderation, abuse prevention and real-world evaluation.

## CV description
**Kindred — Dating Recommendation System | Python, JavaScript, HTML/CSS**  
Built an explainable recommendation prototype with reciprocal preference filtering, cosine similarity ranking, an interactive interface and reproducible evaluation against a random baseline using synthetic data.
