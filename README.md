# ai-disclosure-checker

A free, open-source heuristic scanner that checks a website for common **EU AI Act transparency-disclosure gaps**: unidentified chatbots, privacy pages with no AI section, unlabeled AI-generated images, "powered by AI" claims with no disclosure link, and missing machine-readable disclosure.

## Why this exists

The EU AI Act's transparency duties are live: users must know when they're interacting with AI, and AI-generated content must be identifiable as such. Violations can draw fines of up to **€15M or 3% of global turnover**. Most small sites have no idea where their gaps are. This tool gives you a concrete checklist in 30 seconds.

**Brought to you by [Ingenious AI](https://disclosure-guard.onrender.com)** — makers of DisclosureGuard, the AI-disclosure compliance platform.

## Install

Python 3.8+, no dependencies (stdlib only):

```bash
git clone https://github.com/Iceman2050/ai-disclosure-checker.git
cd ai-disclosure-checker
python3 checker.py https://your-site.example
```

## Usage

```bash
# Scan a site (homepage + same-origin link crawl, max 25 pages)
python3 checker.py https://your-site.example

# Discover pages via sitemap.xml instead
python3 checker.py https://your-site.example --sitemap

# JSON output for CI pipelines
python3 checker.py https://your-site.example --json

# Limit pages / verbose crawl log
python3 checker.py https://your-site.example --max-pages 10 -v
```

Exit code: `0` = no gaps found, `1` = findings reported.

**Only scan websites you own or have explicit permission to test.** The crawler is polite by design: 1 request/second, `robots.txt` respected, 30s timeout, 2 MB body cap, max 25 pages.

## What it checks

| ID | Severity | Check |
|----|----------|-------|
| DC-001 | HIGH | Chatbot widget (Intercom, Drift, HubSpot, Crisp, Tawk.to, Tidio, Zendesk, LiveChat, Freshchat…) with no nearby AI-identification text |
| DC-002 | MEDIUM | Privacy/terms page exists but has no AI-disclosure section (or no policy page found at all) |
| DC-003 | MEDIUM | Image whose filename/alt suggests AI generation (midjourney, dall-e, stable diffusion…) without a caption disclosure |
| DC-004 | LOW | "Powered by AI" / "AI-driven" marketing claim with no link to a disclosure page |
| DC-005 | LOW | No machine-readable AI disclosure (`disclosure.json` or AI section in `llms.txt`) |

Every finding includes the page, an evidence snippet, and a concrete fix — and every finding is labeled **HEURISTIC**.

## **Honest limitations**

- **These are heuristics, not legal advice.** A clean scan does not prove EU AI Act compliance; a finding does not prove a violation. **For legal certainty, consult counsel.**
- Chatbot detection is marker-based: custom-built widgets it has never seen will be missed.
- "Nearby identification text" is a character-window heuristic, not semantic understanding.
- DC-005 (machine-readable disclosure) is an emerging best practice, not a settled legal requirement.
- The tool cannot assess your actual AI systems, training data, or risk classification — only your public web presence.

## CI example

```yaml
- name: AI disclosure check
  run: python3 ai-disclosure-checker/checker.py https://staging.example.com --json
```

## License

MIT — see [LICENSE](LICENSE). © 2026 Ingenious AI.

## Go deeper

For continuous monitoring, policy templates, and audit-ready evidence, see **[DisclosureGuard](https://disclosure-guard.onrender.com)**.
