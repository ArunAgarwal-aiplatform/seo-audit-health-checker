#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║            SEO AUDIT HEALTH CHECKER  v2.0                    ║
║      "Brutal honesty. Zero APIs. Pure Python."               ║
╚══════════════════════════════════════════════════════════════╝

Works on:  .txt (Notepad)  |  .md (Markdown)  |  .html / .htm

Usage:
    python seo_audit.py                              # interactive
    python seo_audit.py myfile.md                    # prompts keyword
    python seo_audit.py article.txt --keyword "seo"
    python seo_audit.py page.html -k "best laptops"
"""

import sys
import os
import re
import string
import random


# ─────────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────────

SEP = "─" * 64
SEP2 = "═" * 64

GRADE_ART = {
    "A": "     ██╗  \n    ████╗  \n   █╔╗██║  \n   ███████║  \n   ╚══╝██║  \n      ╚═╝  ",
    "B": "   ██████╗  \n   ██╔══██╗  \n   ██████╔╝  \n   ██╔══██╗  \n   ██████╔╝  \n   ╚═════╝  ",
    "C": "   ██████╗  \n   ██╔════╝  \n   ██║       \n   ██║       \n   ╚██████╗  \n    ╚═════╝  ",
    "D": "   ██████╗  \n   ██╔══██╗  \n   ██║  ██║  \n   ██║  ██║  \n   ██████╔╝  \n   ╚═════╝  ",
    "F": "   ███████╗  \n   ██╔════╝  \n   █████╗    \n   ██╔══╝    \n   ██║       \n   ╚═╝       ",
}

GRADE_COMMENTS = {
    "A": [
        "🏆  A  —  LEGENDARY TIER.\n"
        "    This content is so well-optimised Google might give it a corner office\n"
        "    and a standing ovation. The SEO gods are weeping actual tears of joy.\n"
        "    You didn't just pass the exam — you rewrote the entire syllabus.\n"
        "    Frame this. Tattoo it. Send it to your mum.\n"
        "    She will finally understand what you do for a living.",

        "🦅  A  —  THE GOLDEN CHILD.\n"
        "    Crawlers are fighting each other over who gets to index this first.\n"
        "    Your keyword density is so perfect it belongs in a glass museum case.\n"
        "    Your heading structure has the hierarchy that therapists would envy.\n"
        "    Honestly, this content makes other content feel bad about itself.\n"
        "    Well done. Genuinely. We are not even being sarcastic this time.",

        "🎖️   A  —  YOU ABSOLUTE OVERACHIEVER.\n"
        "    Other blog posts read this file and quietly delete themselves.\n"
        "    Google's algorithm read it and whispered: 'Finally. Someone gets it.'\n"
        "    You have the passive voice of a poet and the schema of a scholar.\n"
        "    Whatever you are doing — don't stop. Don't change.\n"
        "    The internet needs more of this. Carry on.",
    ],
    "B": [
        "🎯  B  —  SOLID. BUT NOT LEGENDARY. YET.\n"
        "    Google likes you. It doesn't love you. Not quite yet.\n"
        "    Think of this as the SEO version of 'you're a great person but\n"
        "    let's just be friends.' Knock out those last few checks\n"
        "    and you'll go from Google's acquaintance to its absolute best mate.\n"
        "    You're so close. The A is right there. Don't stop now.",

        "😎  B  —  THE PROMISING STUDENT.\n"
        "    You clearly read the SEO handbook. Maybe skipped chapter 7.\n"
        "    Your content performs like a mid-table football team:\n"
        "    never relegated, never wins the league. Always 'almost there'.\n"
        "    Respectable. Functional. Slightly forgettable at parties.\n"
        "    Add depth signals and a couple more links. Go on. You've got this.",

        "📐  B  —  ALMOST THERE, CHAMP.\n"
        "    This is the SEO equivalent of arriving 3 minutes late to a party —\n"
        "    everything was perfectly set up, but you missed the door prize.\n"
        "    Structure is good. Writing is largely active. Schema is present.\n"
        "    Something small is still keeping that A just out of arm's reach.\n"
        "    Check the suggestions below. Your ranking is watching. Waiting.",
    ],
    "C": [
        "😐  C  —  AGGRESSIVELY AVERAGE.\n"
        "    Your content is the plain white rice of the internet.\n"
        "    Technically edible. Nutritionally present. Utterly forgettable.\n"
        "    Google has seen it, nodded politely, and moved on to better things.\n"
        "    Google is now dating someone else's blog. It has better alt text.\n"
        "    You can fix this. You just have to want it badly enough.",

        "🤷  C  —  THE 'FINE' GRADE.\n"
        "    When someone asks how the content is and the answer is just 'fine'.\n"
        "    Not bad. Not good. Just existing. Quietly occupying server space.\n"
        "    Google crawled it, shrugged like a bored French waiter, and left.\n"
        "    Your headings are there. Your keyword is somewhere. Probably.\n"
        "    Metaphorically speaking, this content is wearing a beige turtleneck.",

        "🎠  C  —  STUCK IN THE MIDDLE WITH NOBODY.\n"
        "    Like a roundabout with no exits — looks busy, goes in circles,\n"
        "    never quite arrives anywhere particularly useful.\n"
        "    Your passive voice is doing several jobs it was never hired for.\n"
        "    Your content depth is doing approximately none.\n"
        "    Together they cancel each other into mediocrity. Break the cycle.",
    ],
    "D": [
        "😬  D  —  DISTRESS SIGNAL DETECTED.\n"
        "    This content tried. You can feel it in every passive sentence,\n"
        "    every missing heading, every link that was meant to be added 'later'.\n"
        "    Google found it, filed a quiet frown, and kept on scrolling.\n"
        "    This is the '2am the night before it's due' of blog posts.\n"
        "    Not dead. But critically, urgently, needing immediate first aid.",

        "🚑  D  —  CALLING DR. SEO.\n"
        "    Your content is on life support and the keyword is flatlining.\n"
        "    Passive voice: everywhere. Heading hierarchy: collapsed in on itself.\n"
        "    Content depth: paddling pool. Schema: sent your apologies, couldn't come.\n"
        "    Google's crawler visited once, filed a health and safety report, and left.\n"
        "    The suggestions below are a defibrillator. Charge to 360. Use them all.",

        "📉  D  —  THE UNDERPERFORMER.\n"
        "    Remember when you wrote this? You probably thought: good enough.\n"
        "    Reader — it was not good enough. It was barely enough at all.\n"
        "    Google has you on page 4, next to a forum thread nobody asked for\n"
        "    and a website whose SSL certificate expired during the last World Cup.\n"
        "    Your content deserves better. Pick the lowest score. Start there. Now.",
    ],
    "F": [
        "💀  F  —  FAREWELL, SWEET CONTENT.\n"
        "    This is not a blog post. This is a digital ghost story.\n"
        "    It haunts a server somewhere, indexed by nobody,\n"
        "    read by no one, ranking for absolutely nothing whatsoever.\n"
        "    Google's bots visited once, left a one-star review in their logs,\n"
        "    and quietly removed it from the crawl queue. Deepest condolences.",

        "🗑️   F  —  THE CAUTIONARY TALE.\n"
        "    SEO consultants print this score and frame it with the caption:\n"
        "    'Never. Again. Show this to your clients. To your enemies. To strangers.'\n"
        "    Keyword density: zero or a misdemeanour, unclear which is worse.\n"
        "    Structure: the architectural integrity of a collapsed soufflé.\n"
        "    Passive voice has taken over entirely. There is no active voice left.",

        "🔥  F  —  SCORCHED EARTH SEO.\n"
        "    Somewhere out there, a search engine is quietly weeping.\n"
        "    Not dramatically — just a small, tired, not-again kind of cry.\n"
        "    No useful headings. No real links. No meaningful keyword presence.\n"
        "    Just unbroken wall-of-text energy and the ghost of a meta description.\n"
        "    Close this file. Read the suggestions below. Begin entirely anew.",
    ],
}

# True passive: "to be" verb form directly preceding a past participle
PASSIVE_BE = re.compile(
    r'\b(am|is|are|was|were|be|been|being|'
    r'has been|have been|had been|'
    r'will be|would be|could be|should be|might be|may be)\b',
    re.IGNORECASE,
)

# Common words ending in -ed/-en that are NOT passive participles
PASSIVE_FALSE_POS = {
    "need", "indeed", "speed", "seed", "feed", "freed", "agreed",
    "exceed", "proceed", "succeed", "hundred", "open", "even",
    "often", "happen", "broken", "spoken", "token", "golden",
    "frozen", "chosen", "woven", "proven", "reserved", "detailed",
}

DEPTH_SIGNALS = {
    "examples": [
        "for example", "for instance", "such as", "e.g.",
        "example:", "consider this", "let's say", "imagine",
        "scenario", "case study", "to illustrate",
    ],
    "data": [
        "%", "percent", "million", "billion", "according to",
        "research shows", "study found", "survey", "statistics",
        "data shows", "reported that", "analysis", "found that",
        "survey shows", "report says", "studies show",
    ],
    "steps": [
        "step 1", "step 2", "step 3",
        "first,", "second,", "third,", "finally,",
        "to begin", "start by", "next,", "then,", "lastly,",
    ],
    "lists": [
        "here are", "the following", "these include",
    ],
    "code": [
        "```", "<code>", "def ", "function(",
        "import ", "class ", "print(", "console.log",
    ],
}

SCHEMA_PATTERNS = [
    r'application/ld\+json',
    r'"@context"\s*:',
    r'"@type"\s*:',
    r'itemscope',
    r'itemtype\s*=',
    r'og:title',
    r'og:description',
    r'twitter:card',
    r'twitter:title',
]

SUGGESTION_BANK = {
    "Keyword Density": (
        "🔍  LSI Strategy: instead of repeating your exact keyword phrase,\n"
        "     weave in semantically related terms — synonyms, subtopics, and\n"
        "     related concepts. Google understands context and co-occurrence.\n"
        "     A page about 'teacher growth' is stronger with 'professional\n"
        "     development', 'educator well-being', and 'teacher retention' in it."
    ),
    "Passive Voice Ratio": (
        "✍️   'Who does what?' test: read every sentence aloud. If you can't\n"
        "     name the actor instantly, rewrite it. Active voice also shortens\n"
        "     sentences — and short, direct sentences rank better as snippets."
    ),
    "Duplicate Sentences": (
        "♻️   Self-plagiarism check: paste your older posts into a diff tool.\n"
        "     Google Panda penalises internal duplication across your whole site,\n"
        "     not just content copied from others. Audit the entire domain."
    ),
    "Heading Structure": (
        "🗂️   Skeleton-first writing: draft ALL your section headings before\n"
        "     writing a single body paragraph. Frame at least 2 headings as\n"
        "     questions — question-format headings are 3x more likely to appear\n"
        "     in Google's featured snippet / People Also Ask boxes."
    ),
    "Title / H1 Quality": (
        "🏹  Magazine-cover test: would this headline appear on a magazine?\n"
        "     Add a number, a power word, and a specific outcome.\n"
        "     'SEO Tips' → '11 Proven SEO Tips That Doubled Traffic in 90 Days'"
    ),
    "Meta Description / Preview": (
        "🎭  Write TWO meta descriptions and pick the stronger one. One focuses\n"
        "     on the problem solved; one teases a surprising stat. The one that\n"
        "     sparks curiosity wins — curiosity gap drives click-through rate."
    ),
    "Internal & External Links": (
        "🕸️   Pillar + cluster: pick your 3 strongest pages and link every new\n"
        "     post back to at least one of them. This funnels authority into your\n"
        "     key URLs — the highest-ROI internal linking move you can make."
    ),
    "Image Alt Text": (
        "🖼️   Describe as if on a phone call: 'Analytics dashboard showing a\n"
        "     47% drop in bounce rate after the redesign' beats 'screenshot'.\n"
        "     Also rename image files before uploading — crawlers read filenames."
    ),
    "Structured Data / Schema": (
        "📋  FAQ schema hack: add 4–6 real questions (from Google's PAA box)\n"
        "     with 40–60 word answers. FAQ schema can double your SERP real estate\n"
        "     with zero extra ranking effort — highest leverage schema type."
    ),
    "Content Depth & Expertise": (
        "📈  Original data hook: even a small internal analytics snippet\n"
        "     ('our data shows…') makes content uniquely citable — the holy\n"
        "     grail for earning backlinks without an outreach campaign."
    ),
}

UNIVERSAL_TIP = (
    "📅  Content Refresh: revisit this piece in 3 months. Update one stat,\n"
    "     add one new example, bump the 'Last modified' date. Google rewards\n"
    "     freshness — updated posts often jump 2–5 positions overnight."
)


# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────

def strip_html(text):
    """Remove HTML tags and decode basic entities."""
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', text,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', text,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    for ent, repl in [('&nbsp;', ' '), ('&amp;', '&'), ('&lt;', '<'),
                      ('&gt;', '>'), ('&quot;', '"'), ('&#39;', "'")]:
        text = text.replace(ent, repl)
    return text


def clean_text(text):
    """Strip all markup and normalise whitespace for linguistic analysis."""
    txt = strip_html(text)
    txt = re.sub(r'#+\s*', '', txt)
    txt = re.sub(r'\*\*|__|\*|_|~~|`{1,3}', '', txt)
    txt = re.sub(r'!\[.*?\]\(.*?\)', '', txt)
    txt = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt.strip()


def get_sentences(text):
    """Split cleaned text into non-trivial sentences (>=5 words)."""
    cleaned = clean_text(text)
    raw = re.split(r'(?<=[.!?])\s+', cleaned)
    return [s.strip() for s in raw if len(s.strip().split()) >= 5]


def score_bar(score, max_score, width=20):
    filled = round((score / max_score) * width) if max_score else 0
    pct = int((score / max_score) * 100) if max_score else 0
    return f"[{'█' * filled}{'░' * (width - filled)}] {pct:3d}%"


def make_result(label, score, max_score, detail, raw=None):
    return {"label": label, "score": score, "max": max_score,
            "detail": detail, "raw": raw}


# ─────────────────────────────────────────────────────────────
#  CONTENT-TYPE DETECTION
# ─────────────────────────────────────────────────────────────

def detect_type(text, filename=""):
    """
    Returns (display_label, type_key, is_plain_text).
    is_plain_text = True for .txt / Notepad files with no markup.
    """
    fname = filename.lower()
    lower = text.lower()
    lines = text.split("\n")

    # ── extension shortcuts ──
    if fname.endswith((".py", ".js", ".ts", ".java", ".cpp", ".cs")):
        return "Source Code File", "code", False
    if fname.endswith((".html", ".htm")):
        return "HTML / Web Page", "html", False

    is_plain = fname.endswith(".txt") or (
        "##" not in text
        and "<h" not in lower
        and "```" not in text
        and not any(re.match(r'^#\s+\S', ln.strip()) for ln in lines)
    )

    wc = len(clean_text(text).split())

    blog_sigs = [
        "blog", "posted by", "author:", "published on", "tags:",
        "categories:", "comments", "share this", "subscribe",
        "related posts", "read more", "written by",
    ]
    product_sigs = [
        "add to cart", "buy now", "price:", "shipping",
        "in stock", "sku", "warranty", "dimensions",
        "product description", "free shipping",
    ]
    # Academic requires very specific signals — NOT just "introduction"
    academic_sigs = [
        "abstract", "bibliography", "doi:", "methodology",
        "literature review", "hypothesis", "peer-reviewed",
        "journal of", "vol.", "pp.",
    ]

    blog_sc = sum(1 for s in blog_sigs if s in lower)
    product_sc = sum(1 for s in product_sigs if s in lower)
    academic_sc = sum(1 for s in academic_sigs if s in lower)

    has_md_h1 = any(re.match(r'^#\s+\S', ln.strip()) for ln in lines)
    has_md_h2 = any(re.match(r'^##\s+\S', ln.strip()) for ln in lines)
    has_code = "```" in text or "<code>" in lower

    if product_sc >= 2:
        return "Product Description / E-commerce", "product", is_plain
    if academic_sc >= 3:
        return "Academic / Research Article", "article", is_plain
    if blog_sc >= 1 or (has_md_h1 and has_md_h2):
        return "Blog Post", "blog", is_plain
    if has_code:
        return "Technical / Developer Content", "technical", is_plain
    if wc < 150:
        return "Short-form Content / Snippet", "short", is_plain
    if is_plain:
        return "Plain-text Article (Notepad / .txt)", "general", True
    return "General Web Content / Article", "general", False


# ─────────────────────────────────────────────────────────────
#  HEADING DETECTION — Markdown + HTML + plain-text
# ─────────────────────────────────────────────────────────────

def find_headings(text, is_plain):
    """
    Returns dict: {h1: [...], h2: [...], h3: [...]}.
    Handles Markdown (# / ## / ###), HTML (<h1>–<h3>),
    and plain-text conventions (ALL CAPS lines, underlined lines,
    numbered section headers like '1. Introduction').
    """
    lines = text.split("\n")
    h1, h2, h3 = [], [], []

    # ── Markdown ──
    for ln in lines:
        s = ln.strip()
        if re.match(r'^###\s+\S', s):
            h3.append(re.sub(r'^#+\s*', '', s))
        elif re.match(r'^##\s+\S', s):
            h2.append(re.sub(r'^##\s*', '', s))
        elif re.match(r'^#\s+\S', s):
            h1.append(re.sub(r'^#\s*', '', s))

    # ── HTML ──
    for tag, bucket in (('h1', h1), ('h2', h2), ('h3', h3)):
        for m in re.finditer(
                rf'<{tag}[^>]*>(.*?)</{tag}>', text,
                re.IGNORECASE | re.DOTALL):
            bucket.append(strip_html(m.group(1)).strip())

    # ── Plain-text (only when no Markdown/HTML headings found) ──
    if is_plain and not h1 and not h2:
        for idx, ln in enumerate(lines):
            s = ln.strip()
            if not s:
                continue

            # Underline style: Title\n======  or  Title\n------
            nxt = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
            if re.match(r'^={3,}$', nxt) and 3 <= len(s) <= 80:
                h1.append(s)
                continue
            if re.match(r'^-{3,}$', nxt) and 3 <= len(s) <= 80:
                h2.append(s)
                continue

            # ALL CAPS single line (4–60 chars, no sentence punctuation)
            if (s == s.upper()
                    and re.search(r'[A-Z]', s)
                    and 4 <= len(s) <= 60
                    and not re.search(r'[.!?,;]', s)):
                h2.append(s)
                continue

            # Numbered section:  "1. Introduction" / "2.1 Background"
            if re.match(r'^\d+(\.\d+)?\s+[A-Z][a-zA-Z\s]{3,50}$', s):
                h2.append(s)

    return {"h1": h1, "h2": h2, "h3": h3}


# ─────────────────────────────────────────────────────────────
#  CHECK 1 — KEYWORD DENSITY
# ─────────────────────────────────────────────────────────────

def check_keyword_density(text, keyword):
    if not keyword:
        return make_result(
            "Keyword Density", 5, 10,
            "⚠️  [SKIPPED] No keyword provided — use --keyword flag.\n"
            "     Assuming 5/10 as neutral baseline.",
        )

    cleaned = clean_text(text).lower()
    words = cleaned.split()
    total = len(words)
    kw = keyword.lower().strip()

    if total == 0:
        return make_result("Keyword Density", 0, 10,
                           "❌ [ERROR] File appears to be empty.")

    # ── CORRECT formula: phrase count / total words × 100 ──
    # (NOT multiplied by keyword word-count — that was the v1 bug)
    count = cleaned.count(kw)
    density = round((count / total) * 100, 2)

    if 1.0 <= density <= 3.0:
        sc, st = 10, "✅ PERFECT"
        note = (f"'{kw}' appears {count}× in {total:,} words "
                f"({density}%). Goldilocks zone!")
    elif 0.5 <= density < 1.0:
        sc, st = 6, "⚠️  LOW"
        note = (f"'{kw}' appears {count}× ({density}%). "
                "Mention it more naturally throughout.")
    elif 3.0 < density <= 5.0:
        sc, st = 5, "⚠️  HIGH"
        note = (f"'{kw}' appears {count}× ({density}%). "
                "Getting stuffed — ease off a little.")
    elif density > 5.0:
        sc, st = 1, "❌ KEYWORD STUFFING"
        note = (f"'{kw}' appears {count}× ({density}%). "
                "Google's spam detector is already annoyed.")
    else:
        sc, st = 3, "❌ TOO RARE"
        note = (f"'{kw}' found {count}× ({density}%). "
                "Almost invisible — mention it more.")

    return make_result("Keyword Density", sc, 10,
                       f"[{st}] {note}", raw=density)


# ─────────────────────────────────────────────────────────────
#  CHECK 2 — PASSIVE VOICE
# ─────────────────────────────────────────────────────────────

def is_passive(sentence):
    """
    True only when a 'to be' verb is followed within 3 tokens by a
    past participle (-ed / -en / -n suffix) not in the false-positive list.
    This avoids flagging 'is happy', 'are ready', 'was there', etc.
    """
    words = sentence.lower().split()
    for i, raw_w in enumerate(words):
        w = raw_w.strip(string.punctuation)
        if not PASSIVE_BE.fullmatch(w):
            continue
        # Look ahead up to 3 positions
        for j in range(i + 1, min(i + 4, len(words))):
            cand = words[j].strip(string.punctuation)
            if cand in PASSIVE_FALSE_POS:
                continue
            if len(cand) > 4 and (
                cand.endswith("ed")
                or cand.endswith("en")
                or (cand.endswith("n") and len(cand) > 5)
            ):
                return True
    return False


def check_passive_voice(text):
    sentences = get_sentences(text)
    total = len(sentences)

    if total < 3:
        return make_result("Passive Voice Ratio", 7, 10,
                           "⚠️  [LIMITED] Too few sentences for reliable analysis.")

    passive_sents = [s for s in sentences if is_passive(s)]
    count = len(passive_sents)
    ratio = round((count / total) * 100, 1)

    if ratio < 10:
        sc, st = 10, "✅ EXCELLENT"
        note = f"{count}/{total} passive ({ratio}%). Active & punchy!"
    elif ratio < 20:
        sc, st = 8, "✅ GOOD"
        note = f"{count}/{total} passive ({ratio}%). Within the target range."
    elif ratio < 35:
        sc, st = 5, "⚠️  HIGH"
        note = f"{count}/{total} passive ({ratio}%). Rewrite some sentences actively."
    else:
        sc, st = 2, "❌ HEAVY PASSIVE"
        note = f"{count}/{total} passive ({ratio}%). Writing feels sluggish."

    detail = f"[{st}] {note}"
    if passive_sents:
        sample = passive_sents[0][:90]
        detail += f'\n     Example: "{sample}…"'

    return make_result("Passive Voice Ratio", sc, 10, detail, raw=ratio)


# ─────────────────────────────────────────────────────────────
#  CHECK 3 — DUPLICATE SENTENCES
# ─────────────────────────────────────────────────────────────

def check_duplicates(text):
    sentences = get_sentences(text)
    seen, dupes = {}, {}

    for sent in sentences:
        norm = " ".join(sent.lower().split())
        seen[norm] = seen.get(norm, 0) + 1
        if seen[norm] == 2:
            dupes[norm[:72]] = seen[norm]

    count = len(dupes)

    if count == 0:
        sc, st = 10, "✅ CLEAN"
        note = "Zero duplicate sentences. Original content confirmed."
    elif count <= 2:
        sc, st = 6, "⚠️  MINOR"
        note = f"{count} repeated sentence(s) — light copy-paste detected."
    elif count <= 5:
        sc, st = 3, "❌ NOTICEABLE"
        note = f"{count} duplicates — were you copy-pasting yourself?"
    else:
        sc, st = 0, "❌ SEVERE"
        note = f"{count} duplicates — Google will flag this as thin content."

    detail = f"[{st}] {note}"
    if dupes:
        ex = list(dupes.keys())[0]
        detail += f'\n     E.g.: "{ex}…"'

    return make_result("Duplicate Sentences", sc, 10, detail, raw=count)


# ─────────────────────────────────────────────────────────────
#  CHECK 4 — HEADING STRUCTURE
# ─────────────────────────────────────────────────────────────

def check_headings(text, is_plain):
    h = find_headings(text, is_plain)
    h1s = h["h1"]
    h2s = h["h2"]
    h3s = h["h3"]
    sc = 10
    issues = []

    if not h2s and not h1s:
        sc -= 5
        if is_plain:
            issues.append(
                "No headings found — in .txt files use ALL CAPS section "
                "titles or underline them with === / ---"
            )
        else:
            issues.append("No H1/H2 headings — add structure with # / ##")
    elif not h2s:
        sc -= 4
        issues.append("H1 found but no H2 sections — break into titled sections")
    elif len(h2s) < 2:
        sc -= 2
        issues.append("Only 1 H2 — add more sections for scannability")

    if not h3s:
        sc -= 1
        issues.append("No H3 sub-headings (optional, but helps long pieces)")

    if len(h1s) > 1:
        sc -= 2
        issues.append(f"{len(h1s)} H1s found — each page should have exactly one")

    sc = max(0, sc)

    if sc >= 9:
        st = "✅ GREAT"
    elif sc >= 7:
        st = "✅ GOOD"
    elif sc >= 4:
        st = "⚠️  WEAK"
    else:
        st = "❌ POOR"

    note = f"H1: {len(h1s)}  |  H2: {len(h2s)}  |  H3: {len(h3s)}"
    if h2s:
        sample = [re.sub(r'^#+\s*', '', x)[:38] for x in h2s[:3]]
        note += "\n     Sections: " + " | ".join(sample)
    if issues:
        note += "\n     Issues: " + "; ".join(issues)

    return make_result("Heading Structure", sc, 10, f"[{st}] {note}",
                       raw={"h1": len(h1s), "h2": len(h2s), "h3": len(h3s)})


# ─────────────────────────────────────────────────────────────
#  CHECK 5 — TITLE / H1 QUALITY
# ─────────────────────────────────────────────────────────────

def check_title(text, keyword, is_plain):
    lines = text.strip().split("\n")
    title = None

    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        # Markdown H1
        if re.match(r'^#\s+\S', s):
            title = re.sub(r'^#+\s*', '', s).strip()
            break
        # HTML h1
        m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.IGNORECASE)
        if m:
            title = strip_html(m.group(1)).strip()
            break

    # Plain-text fallback: first line that looks like a headline (not a sentence)
    if not title and is_plain:
        for ln in lines:
            s = ln.strip()
            if not s:
                continue
            wc = len(s.split())
            if (2 <= wc <= 14
                    and not s.endswith(".")
                    and not s.startswith("http")):
                title = s
                break

    if not title:
        return make_result(
            "Title / H1 Quality", 0, 10,
            "❌ [MISSING] No title found.\n"
            "     .md files  → start with  '# Your Title'\n"
            "     .txt files → put your title on the very first non-blank line",
        )

    sc = 10
    issues = []
    tlen = len(title)

    if tlen > 70:
        sc -= 4
        issues.append(f"Too long ({tlen} chars) — Google truncates at ~60")
    elif tlen > 60:
        sc -= 2
        issues.append(f"Slightly long ({tlen} chars) — try to stay under 60")
    elif tlen < 15:
        sc -= 3
        issues.append(f"Too short ({tlen} chars) — add more descriptive context")

    if keyword:
        pos = title.lower().find(keyword.lower())
        if pos == -1:
            sc -= 3
            issues.append(f"Keyword '{keyword}' not in title — front-load it")
        elif pos > 30:
            sc -= 1
            issues.append(f"Keyword at pos {pos} — move it closer to the start")

    power_words = [
        "how", "why", "what", "best", "top", "guide", "tips", "ways",
        "mistakes", "secrets", "ultimate", "complete", "easy", "proven",
        "free", "new", "step", "learn", "master",
    ]
    has_num = bool(re.search(r'\b\d+\b', title))
    has_power = any(w in title.lower() for w in power_words)
    if has_num or has_power:
        sc = min(10, sc + 1)

    sc = max(0, sc)

    if sc >= 8:
        st = "✅ GREAT"
    elif sc >= 6:
        st = "✅ GOOD"
    elif sc >= 4:
        st = "⚠️  WEAK"
    else:
        st = "❌ POOR"

    preview = f'"{title[:65]}{"…" if tlen > 65 else ""}" ({tlen} chars)'
    note = preview
    if issues:
        note += "\n     Issues: " + "; ".join(issues)
    extras = []
    if has_num:
        extras.append("✓ Has a number (CTR boost)")
    if has_power:
        extras.append("✓ Has power words")
    if extras:
        note += "\n     " + " | ".join(extras)

    return make_result("Title / H1 Quality", sc, 10, f"[{st}] {note}", raw=tlen)


# ─────────────────────────────────────────────────────────────
#  CHECK 6 — META DESCRIPTION / INTRO PARAGRAPH
# ─────────────────────────────────────────────────────────────

def check_meta_desc(text, is_plain):
    desc = None
    source = None

    # ── HTML meta tag ──
    m = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        text, re.IGNORECASE,
    )
    if m:
        desc, source = m.group(1).strip(), "HTML <meta> tag"

    if not desc:
        m = re.search(
            r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']',
            text, re.IGNORECASE,
        )
        if m:
            desc, source = m.group(1).strip(), "Open Graph description"

    # ── Fallback: first substantial paragraph ──
    if not desc:
        paras = re.split(r'\n{2,}', text)
        for para in paras:
            c = clean_text(para).strip()
            if (len(c.split()) >= 12
                    and not c.startswith("#")
                    and not c.startswith("```")
                    and re.search(r'[a-zA-Z]', c)):
                desc = c[:220]
                source = "First paragraph (add a <meta> tag for HTML pages)"
                break

    if not desc:
        return make_result(
            "Meta Description / Preview", 2, 10,
            "❌ [MISSING] No meta tag and no usable intro paragraph.\n"
            "     Write a strong opening sentence to act as your SERP preview.",
        )

    clen = len(desc)
    sc = 10
    issues = []

    if clen < 50:
        sc -= 5
        issues.append(f"Too short ({clen} chars) — SERP snippet will look thin")
    elif clen < 120:
        sc -= 1
        issues.append(f"Could be fuller ({clen} chars) — aim for 120–160")
    elif clen > 160:
        sc -= 3
        issues.append(f"Too long ({clen} chars) — Google cuts off after ~160")

    cta_words = [
        "learn", "discover", "find", "get", "download", "explore",
        "read", "see how", "start", "boost", "improve", "understand",
        "master", "try",
    ]
    if not any(w in desc.lower() for w in cta_words):
        sc -= 1
        issues.append("No action verb — add 'Learn', 'Discover', 'Find out' etc.")

    sc = max(0, sc)

    if sc >= 8:
        st = "✅ GREAT"
    elif sc >= 6:
        st = "✅ GOOD"
    elif sc >= 4:
        st = "⚠️  WEAK"
    else:
        st = "❌ POOR"

    preview = desc[:110] + ("…" if clen > 110 else "")
    note = f'Source: {source} ({clen} chars)\n     Preview: "{preview}"'
    if issues:
        note += "\n     Issues: " + "; ".join(issues)

    return make_result("Meta Description / Preview", sc, 10,
                       f"[{st}] {note}", raw=clen)


# ─────────────────────────────────────────────────────────────
#  CHECK 7 — LINKS
# ─────────────────────────────────────────────────────────────

def check_links(text):
    md_ext = re.findall(r'\[.+?\]\((https?://[^\s)]+)\)', text)
    html_ext = re.findall(r'href=["\'](https?://[^"\']+)["\']',
                          text, re.IGNORECASE)
    raw_ext = re.findall(r'(?<![(\'"=])(https?://[^\s\)\]"\'<>,]+)', text)
    external = list(set(md_ext + html_ext + raw_ext))

    md_int = re.findall(r'\[.+?\]\((/[^\s)]+)\)', text)
    html_int = re.findall(r'href=["\'](/[^"\']+)["\']', text, re.IGNORECASE)
    internal = list(set(md_int + html_int))

    ext_c = len(external)
    int_c = len(internal)
    total = ext_c + int_c

    sc = 10
    issues = []

    if total == 0:
        sc = 1
        issues.append(
            "No links at all — add external citations and internal cross-links"
        )
    else:
        if ext_c == 0:
            sc -= 4
            issues.append(
                "No external links — cite authoritative sources (studies, gov, edu)"
            )
        elif ext_c == 1:
            sc -= 2
            issues.append("Only 1 external link — add 2–3 credible references")
        elif ext_c > 20:
            sc -= 1
            issues.append("Many external links — too many dilutes page authority")

        if int_c == 0:
            sc -= 3
            issues.append(
                "No internal links — link to related pages on your own site"
            )

    sc = max(0, sc)

    if sc >= 8:
        st = "✅ GREAT"
    elif sc >= 5:
        st = "⚠️  WEAK"
    else:
        st = "❌ POOR"

    note = f"External: {ext_c}  |  Internal: {int_c}"
    if external:
        short = [u[:55] + ("…" if len(u) > 55 else "") for u in external[:3]]
        note += "\n     Refs: " + " | ".join(short)
    if issues:
        note += "\n     Issues: " + "; ".join(issues)

    return make_result("Internal & External Links", sc, 10,
                       f"[{st}] {note}", raw=total)


# ─────────────────────────────────────────────────────────────
#  CHECK 8 — IMAGE ALT TEXT
# ─────────────────────────────────────────────────────────────

def check_images(text):
    md_images = re.findall(r'!\[([^\]]*)\]\([^\)]+\)', text)
    html_img_all = re.findall(r'<img\b[^>]*/?>', text, re.IGNORECASE)
    html_img_alt = re.findall(r'<img\b[^>]*\balt\s*=', text, re.IGNORECASE)

    total = len(md_images) + len(html_img_all)
    no_alt = len(html_img_all) - len(html_img_alt)

    lazy_words = {
        "image", "img", "photo", "picture", "screenshot",
        "icon", "logo", "banner", "figure", "pic",
    }

    # Extract alt values from HTML img tags
    html_alts = []
    for tag in html_img_all:
        m = re.search(r'alt=["\']([^"\']*)["\']', tag, re.IGNORECASE)
        if m:
            html_alts.append(m.group(1))

    all_alts = md_images + html_alts
    empty_alts = [a for a in all_alts if not a.strip()]
    lazy_alts = [a for a in all_alts
                 if a.strip() and a.strip().lower() in lazy_words]
    good_alts = [a for a in all_alts
                 if a.strip() and a.strip().lower() not in lazy_words]

    sc = 10
    issues = []

    if total == 0:
        return make_result(
            "Image Alt Text", 5, 10,
            "⚠️  [NO IMAGES] No images detected.\n"
            "     Visuals improve engagement and dwell time — consider adding some.",
        )

    if no_alt > 0:
        sc -= min(5, no_alt * 2)
        issues.append(f"{no_alt} image(s) missing alt attribute entirely")
    if empty_alts:
        sc -= min(3, len(empty_alts))
        issues.append(f"{len(empty_alts)} image(s) with empty alt text")
    if lazy_alts:
        sc -= min(2, len(lazy_alts))
        issues.append(f"{len(lazy_alts)} generic alt text (e.g. 'photo', 'image')")

    sc = max(0, sc)

    if sc >= 8:
        st = "✅ GREAT"
    elif sc >= 5:
        st = "⚠️  WEAK"
    else:
        st = "❌ POOR"

    probs = len(empty_alts) + len(lazy_alts) + no_alt
    note = (f"Total: {total}  |  Good alts: {len(good_alts)}"
            f"  |  Problems: {probs}")
    if good_alts:
        note += f'\n     Good example: "{good_alts[0][:60]}"'
    if issues:
        note += "\n     Issues: " + "; ".join(issues)

    return make_result("Image Alt Text", sc, 10, f"[{st}] {note}", raw=total)


# ─────────────────────────────────────────────────────────────
#  CHECK 9 — STRUCTURED DATA / SCHEMA
#  .txt files can never have JSON-LD, so they get a fair baseline.
# ─────────────────────────────────────────────────────────────

def check_schema(text, filename, content_type):
    fname = filename.lower()
    is_html = fname.endswith((".html", ".htm")) or content_type == "html"
    is_txt = fname.endswith(".txt") or (
        not fname.endswith(".md") and not is_html and content_type != "html"
    )

    if is_txt:
        return make_result(
            "Structured Data / Schema", 6, 10,
            "⚠️  [N/A — .txt file] Plain text cannot carry JSON-LD or meta tags.\n"
            "     When this content is published online, add Article schema +\n"
            "     Open Graph tags to the page template. Score: 6/10 baseline.",
        )

    has_jsonld = bool(re.search(r'application/ld\+json', text, re.IGNORECASE))
    has_microdata = bool(re.search(r'itemscope', text, re.IGNORECASE))
    has_og = bool(re.search(r'og:title|og:description', text, re.IGNORECASE))
    has_twitter = bool(re.search(r'twitter:card|twitter:title', text, re.IGNORECASE))

    sc = 0
    notes = []

    if has_jsonld:
        sc += 7
        notes.append("✓ JSON-LD structured data (best method)")
    if has_microdata:
        sc += 5
        notes.append("✓ Microdata attributes")
    if has_og:
        sc += 2
        notes.append("✓ Open Graph tags")
    if has_twitter:
        sc += 1
        notes.append("✓ Twitter Card tags")

    sc = min(10, sc)

    missing = []
    if not has_jsonld and not has_microdata:
        missing.append("Add JSON-LD Article/BlogPosting schema")
    if not has_og:
        missing.append("Add Open Graph tags for social sharing previews")

    if sc >= 7:
        st = "✅ GREAT"
    elif sc >= 4:
        st = "⚠️  PARTIAL"
    elif sc >= 1:
        st = "⚠️  MINIMAL"
    else:
        st = "❌ NONE"

    note = " | ".join(notes) if notes else "No schema markup found"
    if missing:
        note += "\n     Missing: " + "; ".join(missing)

    return make_result("Structured Data / Schema", sc, 10,
                       f"[{st}] {note}", raw=sc)


# ─────────────────────────────────────────────────────────────
#  CHECK 10 — CONTENT DEPTH
# ─────────────────────────────────────────────────────────────

def check_depth(text, content_type):
    # Use clean_text so CSS/JS noise is stripped before signal scanning
    cleaned_lower = clean_text(text).lower()
    wc = len(cleaned_lower.split())
    found = {}

    for cat, signals in DEPTH_SIGNALS.items():
        hits = [s for s in signals if s in cleaned_lower]
        if hits:
            found[cat] = hits[:2]

    # Regex-based data detection — catches "44%", "82 %", "3x more", commas in numbers
    if "data" not in found:
        data_pats = [
            (r"\b\d+\s*%", "percentage stat"),
            (r"\b\d+x\s+more", "multiplier stat"),
            (r"\b\d{1,3},\d{3}\b", "large number"),
            (r"\baccording to\b", "attribution"),
            (r"\bresearch\b", "research reference"),
            (r"\bsurvey\b", "survey reference"),
        ]
        for pat, label in data_pats:
            if re.search(pat, cleaned_lower):
                found["data"] = [label]
                break

    # HTML list items (<li>) count as list/steps depth
    if "lists" not in found and "steps" not in found:
        li_count = len(re.findall(r"<li\b", text, re.IGNORECASE))
        if li_count >= 3:
            found["lists"] = [f"{li_count} list items"]

    sc = 0
    if "examples" in found:
        sc += 2
    if "data" in found:
        sc += 3
    if "steps" in found:
        sc += 2
    if "lists" in found:
        sc += 1
    if "code" in found:
        sc += 2

    # Word-count adjustment
    if content_type in ("blog", "article", "general", "technical"):
        if wc >= 1500:
            sc += 1
        elif wc < 300:
            sc -= 2
    elif content_type == "product":
        if wc >= 300:
            sc += 1

    # Markdown / plain-text numbered or bulleted lists
    has_numbered = bool(re.search(r"^\s*\d+[.)]\s", text, re.MULTILINE))
    has_bullets = bool(re.search(r"^\s*[-*•]\s", text, re.MULTILINE))
    if has_numbered or has_bullets:
        sc = min(10, sc + 1)

    sc = max(0, min(10, sc))

    if sc >= 8:
        st = "✅ EXPERT"
    elif sc >= 6:
        st = "✅ SOLID"
    elif sc >= 3:
        st = "⚠️  THIN"
    else:
        st = "❌ SHALLOW"

    cats = list(found.keys())
    note = f"Word count: {wc:,}  |  Depth signals: {', '.join(cats) if cats else 'none'}"
    if cats:
        bits = [f"{c} ({', '.join(hits)})" for c, hits in found.items()]
        note += "\n     Found: " + "; ".join(bits)
    else:
        note += (
            "\n     Tip: add real examples, statistics, numbered steps,"
            " or code blocks"
        )

    return make_result("Content Depth & Expertise", sc, 10,
                       f"[{st}] {note}", raw=wc)


# ─────────────────────────────────────────────────────────────
#  GRADING
# ─────────────────────────────────────────────────────────────

def compute_grade(checks, content_type):
    total = sum(c["score"] for c in checks)
    maxi = sum(c["max"] for c in checks)
    pct = round((total / maxi) * 100, 1) if maxi else 0

    if content_type == "short":
        pct = min(100, pct * 1.08)

    if pct >= 85:
        g = "A"
    elif pct >= 72:
        g = "B"
    elif pct >= 58:
        g = "C"
    elif pct >= 42:
        g = "D"
    else:
        g = "F"

    return g, pct, total, maxi


# ─────────────────────────────────────────────────────────────
#  SUGGESTIONS
# ─────────────────────────────────────────────────────────────

def top_suggestions(checks, content_type):
    sorted_checks = sorted(checks, key=lambda c: c["score"] / c["max"])
    tips, used = [], set()

    for chk in sorted_checks:
        if len(tips) >= 4:
            break
        lbl = chk["label"]
        if lbl in used or lbl not in SUGGESTION_BANK:
            continue
        tips.append((lbl, SUGGESTION_BANK[lbl]))
        used.add(lbl)

    while len(tips) < 4:
        tips.append(("Evergreen Tip 🎁", UNIVERSAL_TIP))

    return tips[:4]


# ─────────────────────────────────────────────────────────────
#  OUTPUT HELPERS
# ─────────────────────────────────────────────────────────────

def print_banner(title_line, subtitle=""):
    print()
    print("╔" + SEP2 + "╗")
    print("║" + title_line.center(64) + "║")
    if subtitle:
        print("║" + subtitle.center(64) + "║")
    print("╚" + SEP2 + "╝")
    print()


def print_check(idx, chk):
    sb = score_bar(chk["score"], chk["max"])
    print(f"  [{idx:02d}] {chk['label']}")
    print(f"       Score : {chk['score']}/{chk['max']}  {sb}")
    for ln in chk["detail"].split("\n"):
        print(f"       {ln}")
    print()


def print_grade_panel(g, pct, total, maxi):
    comment = random.choice(GRADE_COMMENTS[g])
    art = GRADE_ART.get(g, "")

    print(SEP)
    print()
    print("  ── FINAL GRADE ──")
    for ln in art.split("\n"):
        print(ln)
    print()
    print(f"  Score : {total} / {maxi} points   ({pct}%)")
    print()
    print("  " + "─" * 58)
    print()
    for ln in comment.split("\n"):
        print(f"  {ln}")
    print()


def print_suggestions_panel(tips):
    print(SEP)
    print()
    print("  💡  TOP 4 INNOVATIVE SEO SUGGESTIONS")
    print()
    for i, (label, tip) in enumerate(tips, 1):
        print(f"  ┌─ #{i}  Based on: {label}")
        for ln in tip.split("\n"):
            print(f"  │  {ln}")
        print("  └" + "─" * 60)
        print()


def print_footer():
    print(SEP)
    print()
    print("  Checks:  Keyword Density · Passive Voice · Duplicates")
    print("           Headings · Title · Meta Description · Links")
    print("           Image Alt Text · Schema · Content Depth")
    print()
    print("  Built with 100% pure Python. No APIs. No libraries. No mercy.")
    print()
    print("╚" + SEP2 + "╝")
    print()


# ─────────────────────────────────────────────────────────────
#  INTERACTIVE PROMPT
# ─────────────────────────────────────────────────────────────

# Recognised content file extensions — anything else is ignored
_CONTENT_EXTS = ('.md', '.txt', '.html', '.htm', '.markdown')


def parse_args():
    """
    Parse optional CLI arguments. Returns (filepath, keyword).

    Only accepts a positional argument as a content filepath when it ends in
    a recognised content extension (.md, .txt, .html, .htm, .markdown).
    This prevents Jupyter / IPython kernel args (e.g. kernel-xxxx.json,
    --ip=..., --stdin=...) from being silently grabbed as the file path.
    """
    args, keyword, filepath = sys.argv[1:], "", None
    idx = 0
    while idx < len(args):
        arg = args[idx]

        if arg in ("--keyword", "-k") and idx + 1 < len(args):
            keyword = args[idx + 1]
            idx += 2

        elif arg.startswith("--keyword="):
            keyword = arg.split("=", 1)[1]
            idx += 1

        elif not arg.startswith("-"):
            # Only accept as content file if it has a known extension.
            # Silently skips Jupyter kernel .json files, notebook paths, etc.
            if any(arg.lower().endswith(ext) for ext in _CONTENT_EXTS):
                filepath = arg
            idx += 1

        else:
            # Skip all other flags (--ip, --stdin, --transport, etc.)
            idx += 1

    return filepath, keyword


def unquote(raw):
    """Strip surrounding quotes the user may have copy-pasted or drag-dropped."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] in ('"', "'") and raw[0] == raw[-1]:
        raw = raw[1:-1].strip()
    return raw


def show_welcome():
    """Always-on startup welcome screen shown every time the tool runs."""
    print()
    print("=" * 66)
    print("  SEO AUDIT HEALTH CHECKER  v2.0")
    print("  Brutal honesty. Zero APIs. Pure Python.")
    print("-" * 66)
    print("  Supports : .md (Markdown)  |  .txt (Notepad)  |  .html")
    print("  Runs     : 10 SEO checks, grades A-F, 4 top suggestions")
    print("=" * 66)
    print()


def _open_file_dialog():
    """
    Try to open a native OS file-picker dialog via tkinter (standard library).
    Returns the chosen path string, or None if unavailable / cancelled.
    Works on Windows, macOS, and Linux (when a display is present).
    Falls back to None silently so the caller can use a text prompt instead.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()                        # hide the empty root window
        root.wm_attributes("-topmost", True)   # bring dialog to front
        root.lift()
        root.focus_force()

        chosen = filedialog.askopenfilename(
            title="SEO Audit — Select your content file",
            filetypes=[
                ("Content files", "*.md *.txt *.html *.htm *.markdown"),
                ("Markdown", "*.md *.markdown"),
                ("Plain text", "*.txt"),
                ("HTML", "*.html *.htm"),
                ("All files", "*.*"),
            ],
        )
        root.destroy()
        return chosen if chosen else None     # empty string when cancelled

    except Exception:
        # tkinter not available (headless server, CI, etc.) — fall through
        return None


def ask_for_file(filepath_cli):
    """
    STEP 1 — Get and validate the content file.
    Priority:
      1. Valid CLI / drag-drop argument already parsed
      2. Native OS file-picker dialog  (tkinter — zero extra deps)
      3. Manual text input fallback    (for headless / CI environments)
    """
    print("  STEP 1 of 2  -  YOUR CONTENT FILE")
    print("  " + "-" * 54)
    print()

    # ── 1. Already provided via CLI ───────────────────────────
    if filepath_cli:
        path = unquote(filepath_cli)
        if os.path.exists(path) and not os.path.isdir(path):
            print("  [OK] File supplied via command line:")
            print("       " + os.path.abspath(path))
            print()
            return path
        print("  [!] CLI path not found: '" + path + "'")
        print("      Falling through to file picker...")
        print()

    # ── 2. Native file-picker dialog ──────────────────────────
    print("  Opening file picker dialog...")
    print("  (A window should appear — browse to your content file and click Open.)")
    print()

    chosen = _open_file_dialog()

    if chosen:
        print("  [OK] File selected via picker:")
        print("       " + os.path.abspath(chosen))
        print()
        return chosen

    # Dialog was cancelled or unavailable — tell user why
    print("  [i] File picker unavailable or cancelled.")
    print("      Running in a terminal / headless environment?")
    print("      No problem — type or paste the path below instead.")
    print()

    # ── 3. Manual text fallback ───────────────────────────────
    print("  Accepted formats:")
    print("    blog_post.md       <-- Markdown blog / article")
    print("    article.txt        <-- Plain text / Notepad file")
    print("    page.html          <-- HTML web page")
    print()
    print("  Tips:")
    print("    * Drag-and-drop the file onto this terminal window")
    print("    * Relative paths work:  posts/my-blog.md")
    print("    * Absolute paths work:  C:\\Users\\you\\blog.md")
    print("    * Surrounding quotes are stripped automatically")
    print()

    while True:
        raw = unquote(input("  >> File path: "))

        if not raw:
            print()
            print("  [!] Nothing entered. Type or paste the file path.")
            print()
            continue

        if not os.path.exists(raw):
            print()
            print("  [!] File not found: '" + raw + "'")
            print("      Check the path, spelling, and extension.")
            print()
            continue

        if os.path.isdir(raw):
            print()
            print("  [!] That is a folder, not a file: '" + raw + "'")
            print("      Select a specific .md, .txt, or .html file.")
            print()
            continue

        print()
        print("  [OK] File confirmed: " + os.path.abspath(raw))
        print()
        return raw


def ask_for_keyword(keyword_cli):
    """
    STEP 2 - Get the target SEO keyword (optional).
    Uses CLI value if given; otherwise prompts interactively.
    """
    print("  STEP 2 of 2  -  TARGET SEO KEYWORD  (optional)")
    print("  " + "-" * 54)
    print()

    # Already provided via CLI
    if keyword_cli:
        kw = keyword_cli.strip()
        print("  [OK] Keyword from command line: '" + kw + "'")
        print()
        return kw

    # Interactive prompt
    print("  What is the main keyword this content should rank for?")
    print()
    print("  Examples:")
    print("    content marketing")
    print("    python tutorial for beginners")
    print("    teacher growth and development")
    print()
    print("  Press Enter to skip.")
    print("  (Density check will use a neutral 5/10 baseline if skipped.)")
    print()

    raw = unquote(input("  >> Keyword: ")).strip()

    if raw:
        print()
        print("  [OK] Keyword set: '" + raw + "'")
    else:
        print()
        print("  [-] No keyword. Density check will be neutral.")

    print()
    return raw


def show_preflight(filepath, keyword, type_label):
    """Confirmation panel shown right before checks run."""
    print("  " + "=" * 58)
    print("  READY  -  HERE IS WHAT WE ARE ABOUT TO SCAN")
    print("  " + "=" * 58)
    print()
    fname = os.path.basename(filepath)
    fpath = os.path.abspath(filepath)
    kw_disp = ("'" + keyword + "'") if keyword else "(none - density check neutral)"
    print("  File    :  " + fname)
    print("  Path    :  " + fpath)
    print("  Type    :  " + type_label)
    print("  Keyword :  " + kw_disp)
    print()
    print("  Running 10 SEO checks...")
    print()


# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

def main():
    # Always show the startup welcome screen
    show_welcome()

    # Parse any CLI arguments
    filepath_cli, keyword_cli = parse_args()

    # STEP 1: get and validate the file
    filepath = ask_for_file(filepath_cli)

    # Read file immediately (needed for type detection before step 2)
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        print("\n[!] Cannot read file: " + str(exc))
        sys.exit(1)

    if not text.strip():
        print("\n[!] File is empty: '" + filepath + "'")
        print("    Choose a file that has content in it.")
        sys.exit(1)

    # Detect content type early so preflight can show it
    type_label, type_key, is_plain = detect_type(text, filepath)

    # STEP 2: get the keyword
    keyword = ask_for_keyword(keyword_cli)

    # Preflight confirmation screen
    show_preflight(filepath, keyword, type_label)

    # Run 10 checks
    print(SEP)
    print("  RUNNING 10 SEO CHECKS ...")
    print(SEP)
    print()

    checks = [
        check_keyword_density(text, keyword),
        check_passive_voice(text),
        check_duplicates(text),
        check_headings(text, is_plain),
        check_title(text, keyword, is_plain),
        check_meta_desc(text, is_plain),
        check_links(text),
        check_images(text),
        check_schema(text, filepath, type_key),
        check_depth(text, type_key),
    ]

    for idx, chk in enumerate(checks, 1):
        print_check(idx, chk)

    print(SEP)

    # Grade
    g, pct, total, maxi = compute_grade(checks, type_key)
    print_grade_panel(g, pct, total, maxi)

    # Suggestions
    tips = top_suggestions(checks, type_key)
    print_suggestions_panel(tips)

    print_footer()


if __name__ == "__main__":
    main()