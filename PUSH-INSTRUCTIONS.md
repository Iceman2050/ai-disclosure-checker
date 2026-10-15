# Push instructions (your one tap)

The repo is fully built and tested locally. Creating the GitHub repo is an
account action — run ONE of these:

## Option A — GitHub CLI (fastest)

```bash
cd ~/workspace/oss/ai-disclosure-checker
gh repo create ai-disclosure-checker --public --source=. --push \
  --description "Free heuristic scanner for EU AI Act transparency-disclosure gaps: unidentified chatbots, missing AI sections in privacy pages, unlabeled AI imagery."
```

## Option B — web UI

1. Go to https://github.com/new → name: `ai-disclosure-checker` → Public → Create.
2. Then:
```bash
cd ~/workspace/oss/ai-disclosure-checker
git init -b main
git add .
git commit -m "ai-disclosure-checker v1.0.0 — EU AI Act transparency-gap scanner"
git remote add origin https://github.com/YOUR-USERNAME/ai-disclosure-checker.git
git push -u origin main
```

## After pushing

1. In `README.md`, replace `YOUR-USERNAME` with your GitHub username (2 spots).
2. Add repo topics: `eu-ai-act` `ai-transparency` `compliance` `security` `chatbot` `open-source` `python`.
3. Traffic taps, in order:
   - **Show HN**: "Show HN: Free scanner for EU AI Act disclosure gaps" (packet has the pre-flight).
   - **r/SaaS or r/Entrepreneur**: compliance-fear angle for founders.
   - **TLDR / newsletter re-pitch**: second tool in the portfolio strengthens the story.
   - **awesome lists**: PR to compliance/security awesome-lists once the repo has a week of history.
4. Every README links https://disclosure-guard.onrender.com — the repo is the top of the funnel.
