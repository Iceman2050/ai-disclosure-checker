"""Tests for ai-disclosure-checker — fixture HTML only, zero live network."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import checker  # noqa: E402


def page(url, html):
    return {"url": url, "html": html}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

NONCOMPLIANT_HOME = """<html><head><title>Acme</title>
<script src="https://widget.intercom.io/widget/abc123"></script></head>
<body>
<h1>Acme — the platform that does everything</h1>
<p>Our software handles your workflow end to end.</p>
<img src="/img/hero-midjourney-v6.png" alt="futuristic office">
<a href="/about">About</a>
</body></html>"""

NONCOMPLIANT_CLAIM = """<html><head><title>Acme</title></head>
<body>
<h1>Acme — Powered by AI</h1>
<p>Our software handles your workflow end to end.</p>
<a href="/about">About</a>
</body></html>"""

NONCOMPLIANT_PRIVACY = """<html><body>
<h1>Privacy Policy</h1>
<p>We collect your email address to send newsletters. We use cookies.</p>
</body></html>"""

COMPLIANT_HOME = """<html><head><title>Acme</title>
<script src="https://widget.intercom.io/widget/abc123"></script></head>
<body>
<h1>Acme — Powered by AI</h1>
<p>You're chatting with our AI assistant below.</p>
<img src="/img/hero.png" alt="AI-generated illustration of a futuristic office">
<a href="/privacy">Privacy & AI disclosure</a>
</body></html>"""

COMPLIANT_PRIVACY = """<html><body>
<h1>Privacy Policy & AI Transparency</h1>
<p>Our chatbot is an AI assistant under the EU AI Act. AI-generated images on
this site are labeled. We do not use automated decision-making on your data.</p>
</body></html>"""


# ---------------------------------------------------------------------------
# DC-001 chatbot identification
# ---------------------------------------------------------------------------


def test_dc001_fires_on_unidentified_chatbot():
    fs = checker.check_chatbot([page("https://x.example/", NONCOMPLIANT_HOME)])
    ids = [f["id"] for f in fs]
    assert "DC-001" in ids
    assert fs[0]["severity"] == "HIGH"
    assert fs[0]["heuristic"] is True


def test_dc001_silent_when_identified():
    fs = checker.check_chatbot([page("https://x.example/", COMPLIANT_HOME)])
    assert [f["id"] for f in fs] == []


def test_dc001_silent_without_chatbot():
    fs = checker.check_chatbot(
        [page("https://x.example/", "<html><body><p>Hello</p></body></html>")]
    )
    assert fs == []


# ---------------------------------------------------------------------------
# DC-002 policy disclosure
# ---------------------------------------------------------------------------


def test_dc002_fires_on_privacy_without_ai_section():
    fs = checker.check_policy_disclosure(
        [
            page("https://x.example/", NONCOMPLIANT_HOME),
            page("https://x.example/privacy", NONCOMPLIANT_PRIVACY),
        ]
    )
    assert [f["id"] for f in fs] == ["DC-002"]


def test_dc002_silent_with_ai_section():
    fs = checker.check_policy_disclosure(
        [
            page("https://x.example/", COMPLIANT_HOME),
            page("https://x.example/privacy", COMPLIANT_PRIVACY),
        ]
    )
    assert fs == []


def test_dc002_fires_when_no_policy_page():
    fs = checker.check_policy_disclosure(
        [page("https://x.example/", NONCOMPLIANT_HOME)]
    )
    assert [f["id"] for f in fs] == ["DC-002"]


# ---------------------------------------------------------------------------
# DC-003 AI image disclosure
# ---------------------------------------------------------------------------


def test_dc003_fires_on_unlabeled_ai_image():
    fs = checker.check_ai_images([page("https://x.example/", NONCOMPLIANT_HOME)])
    ids = [f["id"] for f in fs]
    assert "DC-003" in ids
    assert "midjourney" in fs[0]["evidence"]


def test_dc003_silent_when_captioned():
    fs = checker.check_ai_images([page("https://x.example/", COMPLIANT_HOME)])
    assert fs == []


# ---------------------------------------------------------------------------
# DC-004 AI claims
# ---------------------------------------------------------------------------


def test_dc004_fires_on_claim_without_disclosure_link():
    fs = checker.check_ai_claims([page("https://x.example/", NONCOMPLIANT_CLAIM)])
    assert [f["id"] for f in fs] == ["DC-004"]


def test_dc004_silent_when_linked():
    fs = checker.check_ai_claims([page("https://x.example/", COMPLIANT_HOME)])
    assert fs == []


# ---------------------------------------------------------------------------
# DC-005 machine-readable disclosure
# ---------------------------------------------------------------------------


def _fake_fetch_factory(routes):
    def fake_fetch(url, timeout=30):
        for prefix, (body, status) in routes.items():
            if url.startswith(prefix):
                return url, body, status
        return url, None, 404

    return fake_fetch


def test_dc005_fires_when_nothing_found(monkeypatch):
    monkeypatch.setattr(
        checker, "fetch", _fake_fetch_factory({})
    )
    fs = checker.check_machine_readable("https://x.example/")
    assert [f["id"] for f in fs] == ["DC-005"]
    assert fs[0]["severity"] == "LOW"


def test_dc005_silent_with_disclosure_json(monkeypatch):
    monkeypatch.setattr(
        checker,
        "fetch",
        _fake_fetch_factory(
            {
                "https://x.example/disclosure.json": (
                    '{"ai": {"disclosure": "we use chatbots"}}',
                    200,
                )
            }
        ),
    )
    assert checker.check_machine_readable("https://x.example/") == []


def test_dc005_silent_with_llms_ai_section(monkeypatch):
    monkeypatch.setattr(
        checker,
        "fetch",
        _fake_fetch_factory(
            {
                "https://x.example/llms.txt": (
                    "# Site\n\n## AI disclosure\nWe use AI chatbots.",
                    200,
                )
            }
        ),
    )
    assert checker.check_machine_readable("https://x.example/") == []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def test_extract_links_same_origin_filtering():
    html = (
        '<a href="/about">a</a><a href="https://other.example/x">b</a>'
        '<a href="mailto:a@b.c">c</a>'
    )
    links = checker.extract_links(html, "https://x.example/")
    assert "https://x.example/about" in links
    assert "https://other.example/x" in links
    assert not any(l.startswith("mailto:") for l in links)


def test_extract_text_skips_scripts():
    html = "<script>var secret=1;</script><p>Hello world</p>"
    text = checker.extract_text(html)
    assert "secret" not in text
    assert "Hello world" in text


def test_evidence_window_truncates():
    text = "x" * 500
    snip = checker.evidence(text, 250, 260)
    assert len(snip) <= checker.EVIDENCE_LEN
    assert "x" in snip
