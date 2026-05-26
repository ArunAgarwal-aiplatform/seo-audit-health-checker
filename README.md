# 🔍 SEO Audit Health Checker

> **Brutal honesty. Zero APIs. Pure Python.**
> A command-line SEO auditor that reads any content file — blog post, article,
> product page — runs 10 quality checks, and grades it A to F.
> Think of it as Grammarly for SEO, built from scratch using only the Python standard library.

---

## ✨ Features

- **Native file-picker dialog** — opens a real OS "Open File" window automatically
- **10 SEO checks** aligned with current best practices
- **Works on `.md`, `.txt` (Notepad), `.html`** — all three handled intelligently
- **Smart content-type detection** — Blog, Article, Product Page, Technical, Plain-text, Tags
- **Grade A–F** with a randomised satirical verdict per grade (3 variants each)
- **Top 4 actionable suggestions** ranked by your weakest checks
- **Visual score bars** with `█░` progress indicators per check 
- **Jupyter / IPython safe** — kernel JSON args are silently ignored
- **Zero dependencies** — pure Python 3 standard library only

---

## 📋 The 10 Checks

| # | Check | Target | What it catches |
|---|-------|--------|-----------------|
| 1 | **Keyword Density** | 1–3% | Under-use, stuffing, or complete absence |
| 2 | **Passive Voice Ratio** | < 20% | Weak, indirect writing |
| 3 | **Duplicate Sentences** | 0 | Copy-paste laziness, thin content |
| 4 | **Heading Structure** | H1 + H2s + H3s | Missing hierarchy, multiple H1s |
| 5 | **Title / H1 Quality** | < 60 chars, keyword front | Too long/short, missing keyword |
| 6 | **Meta Description** | 50–160 chars | Missing, truncated, no action verb |
| 7 | **Internal & External Links** | 2+ external, 1+ internal | No citations, no cross-links |
| 8 | **Image Alt Text** | All images described | Missing, empty, or generic alt |
| 9 | **Structured Data / Schema** | JSON-LD + OG tags | Missing schema, no social tags |
| 10 | **Content Depth** | Examples, data, steps | Shallow content, no proof of expertise |

---

## 🚀 Quick Start

### Requirements

- Python 3.7 or higher
- No external libraries required

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/seo-audit-checker.git
cd seo-audit-checker
```

No `pip install` needed — zero dependencies.

### Usage

**Just run it — a file picker window opens automatically:**
```bash
python seo_audit.py
```

**With command-line arguments (skips the prompts):**
```bash
# Markdown blog post
python seo_audit.py samples/inputs/sample_blog.md --keyword "content marketing"

# Plain text / Notepad file
python seo_audit.py samples/inputs/sample_tech_blog.txt --keyword "python automation"

# HTML web page
python seo_audit.py samples/inputs/sample_page.html -k "python tutorial"
```

---

## Important to Note 

This project includes visually generated chart elements created with AI-assisted design support.

Some code comments were drafted with AI assistance and later reviewed for clarity and accuracy.

---

## 🖥️ How the File Picker Works

When you run `python seo_audit.py` with no arguments, a **native OS dialog** opens automatically:

```
  STEP 1 of 2  -  YOUR CONTENT FILE

  Opening file picker dialog...
  (A window should appear — browse to your file and click Open.)
```

| Environment | What happens |
|---|---|
| **VS Code terminal** | Native OS file dialog pops up |
| **Windows terminal** | Native Windows Open File dialog |
| **macOS terminal** | Native macOS Finder dialog |
| **Jupyter / IPython** | Kernel args ignored; dialog or text prompt |
| **Headless / CI server** | Dialog unavailable → falls back to text input |

---

## 📊 Sample Audit Results

Test file: `sample_tech_blog.txt` — keyword: `python automation`

```
  [01] Keyword Density      10/10  ✅  2.11% — Goldilocks zone
  [02] Passive Voice        10/10  ✅  9.8% passive — Active & punchy
  [03] Duplicate Sentences  10/10  ✅  Zero duplicates
  [04] Heading Structure     9/10  ✅  3 ALL CAPS sections detected
  [05] Title Quality        10/10  ✅  55 chars, has number + power words
  [06] Meta Description      6/10  ⚠️  First paragraph too long (220 chars)
  [07] Links                 7/10  ⚠️  3 external, 0 internal
  [08] Image Alt Text        5/10  ⚠️  No images in .txt file
  [09] Schema                6/10  ⚠️  N/A baseline for .txt
  [10] Content Depth         8/10  ✅  Examples, data, code detected

  GRADE: B  —  81/100
```

---

## 📐 Grading Scale

| Grade | Score | Satirical Verdict |
|-------|-------|-------------------|
| **A** | 85–100% | Legendary. Frame this. |
| **B** | 72–84% | Solid. Almost legendary. |
| **C** | 58–71% | Aggressively average. |
| **D** | 42–57% | Distress signal detected. |
| **F** | 0–41% | Scorched earth SEO. |

---

---


---

## 🗂️ File Format Support

| Format | Headings detected | Meta tags | Schema | Notes |
|--------|------------------|-----------|--------|-------|
| `.html` | `<h1>`–`<h3>` | ✅ Full | ✅ Full | Best coverage |
| `.md` | `#` / `##` / `###` | Fallback to para | Partial | Great for blogs |
| `.txt` | ALL CAPS / underline `===` / numbered | Fallback | 6/10 baseline | Notepad friendly |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Notes

This tool is intended as a practical helper, not a replacement for human editing or full SEO review. The score should be used as a starting point for improving content quality, not as the only measure of performance.
---

*"Not all content deserves to rank. This tool tells you why yours doesn't — and exactly how to fix it."*
