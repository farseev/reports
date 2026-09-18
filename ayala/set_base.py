#!/usr/bin/env python3
"""Point the packaged dashboard at the URL you are actually publishing it on.

The build ships with a canonical base of

    https://ayalafoundation.org/programme

and that string is baked into the canonical link, the Open Graph and Twitter
tags, the JSON-LD graph, the copy-paste JSON-LD shown beside each article,
robots.txt and sitemap.xml. Absolute URLs are what search engines and social
crawlers read, so they have to point at the real location before the page goes
live.

    python3 set_base.py https://ayalafoundation.org/programme
    python3 set_base.py https://insights.example.org/ayala/90-day

Rewrites index.html, robots.txt and sitemap.xml in place. Safe to re-run.

What it deliberately does NOT touch:
  * the Foundation's own homepage (https://ayalafoundation.org/) wherever it
    appears as a fact about the organisation - the NGO node's `url` and the
    cited CreativeWork entries;
  * the volunteer./donate. sign-up routes quoted in the post captions.
Those are facts about Ayala Foundation, not publishing paths.

The three articles are declared at site-root slugs (/volunteering-...,
/livelihood-..., /filipino-students-...). If you publish them somewhere else,
edit those paths too - see README.md, section 5.
"""
import re
import sys
import pathlib

OLD_BASE = "https://ayalafoundation.org/programme"
OLD_ROOT = "https://ayalafoundation.org"
SENTINEL = "\x00SETBASE_PROTECTED_%d\x00"

# Exact strings that must survive the rewrite untouched.
PROTECTED = [
    '"url": "https://ayalafoundation.org/"',
    '"url": "https://ayalafoundation.org/",',
]

FILES = ("index.html", "robots.txt", "sitemap.xml")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)

    new_base = sys.argv[1].rstrip("/")
    host = re.match(r"^(https?://[^/\s]+)", new_base)
    if not host:
        sys.exit("set_base: need an absolute http(s) URL, e.g. https://example.org/ayala")
    new_root = host.group(1)

    here = pathlib.Path(__file__).resolve().parent
    touched = False

    for name in FILES:
        path = here / name
        if not path.exists():
            print("set_base: %s not found, skipping" % name)
            continue

        src = path.read_text(encoding="utf-8")
        text = src

        # 1. park the protected strings so the blanket replace cannot reach them
        parked = []
        for frag in PROTECTED:
            while frag in text:
                token = SENTINEL % len(parked)
                text = text.replace(frag, token, 1)
                parked.append((token, frag))

        # 2. longest pattern first, so /programme paths are not clipped by the root swap
        n_base = text.count(OLD_BASE)
        text = text.replace(OLD_BASE, new_base)
        # only root URLs that carry a path, a fragment or a closing quote - never a
        # subdomain such as volunteer.ayalafoundation.org, and never bare prose
        root_re = re.compile(re.escape(OLD_ROOT) + r'(?=[/#"\'])')
        n_root = len(root_re.findall(text))
        text = root_re.sub(new_root, text)

        # 3. put the protected strings back
        for token, frag in parked:
            text = text.replace(token, frag)

        if text != src:
            path.write_text(text, encoding="utf-8")
            touched = True
            print("set_base: %-12s %3d base URL(s), %2d root URL(s) rewritten, "
                  "%d protected" % (name, n_base, n_root, len(parked)))
        else:
            print("set_base: %-12s no change" % name)

    if touched:
        print("set_base: canonical base is now %s" % new_base)
        if new_root != OLD_ROOT:
            print("set_base: note - the three article slugs now sit at %s/<slug>. "
                  "Publish them there or edit the paths by hand." % new_root)
    else:
        print("set_base: nothing changed - has this copy already been pointed elsewhere?")


if __name__ == "__main__":
    main()
