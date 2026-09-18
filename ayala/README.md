# Ayala Foundation — 90-Day Content Programme (self-hosted dashboard)

A single static page. No build step, no server-side code, no external requests
at runtime — every style and script is inlined and the 96 creative renders are
plain JPEGs in `img/`. Drop the folder on any web host and it works.

```
index.html      the whole dashboard (457 KB) — 5 views: Overview, Pillars,
                Calendar, Creative library, Articles
img/            96 progressive JPEGs, 400x600, ~41 KB each (4.1 MB total)
robots.txt
sitemap.xml
set_base.py     one-shot canonical-URL rewriter (see step 1)
```

## 1. Set the canonical URL before you publish  ← do this first

The build ships with a placeholder base of `https://ayalafoundation.org/programme`.
That string appears in the canonical link, the Open Graph / Twitter tags, the
JSON-LD graph, `robots.txt` and `sitemap.xml`. If it is left pointing at a URL
you don't control, search engines will attribute the page there and social
unfurls will fetch images that don't exist.

```bash
python3 set_base.py https://your-domain.org/whatever-path
```

Run it once, in the unzipped folder, before uploading. It rewrites all three
files in place and is safe to re-run.

## 2. Upload

Any static host: S3 + CloudFront, Netlify, Vercel, GitHub Pages, Cloudflare
Pages, or a plain nginx/Apache directory. Keep `img/` as a sibling of
`index.html` — the page references `img/PP1-T-01.jpg` and so on relatively.

Recommended headers, if your host lets you set them:

```
index.html   Cache-Control: public, max-age=300
img/*.jpg    Cache-Control: public, max-age=31536000, immutable
```

Nothing else is required. The page needs no HTTPS-only APIs, but serve it over
HTTPS anyway so the social crawlers will index it.

## 3. What the page does on its own

- **Hash routing.** `#overview`, `#pillars`, `#calendar`, `#library`,
  `#article` are shareable and survive a reload; the back button works.
- **Print/PDF.** `Ctrl/Cmd+P` gives a clean print layout with nav chrome and
  filters dropped.
- **Accessibility.** Skip link to `<main>`, semantic headings, focus styles,
  `prefers-color-scheme` honoured for both themes.
- **Mobile.** Single-column below 720 px, 16 px gutters, no horizontal scroll.

## 4. If you want the SEO/AEO value from the three articles

The Articles view renders all three long-form pieces inside this page, which is
fine for internal review. For search and for answer engines (AI Overviews,
Perplexity, ChatGPT search) each article should also live at its own URL — one
page, one topic, one canonical:

| Slug | Piece |
|---|---|
| `/livelihood-programmes-philippines-measuring-income-not-reach` | Livelihood: programmes count reach, not income |
| `/filipino-students-aspiration-navigation-gap-guidance-counsellors` | Students: a navigation gap, not an aspiration gap |
| `/volunteering-philippines-what-a-first-day-is-like` | Volunteering: what a first day actually looks like |

The full text, the per-article `<title>`/meta description, the 40–60-word
answer box, the question-form H2s, the FAQ blocks and the ready-made
Schema.org JSON-LD are all in `Ayala_longform_pack.md` (delivered separately).
The JSON-LD in this page already declares those three slugs as `Article` and
`FAQPage` nodes against the base you set in step 1, so publish them at exactly
those paths or update both places together.

## 5. Two things to check before this is public-facing

1. **Every trend figure on this page is UNVERIFIED against the prior year.**
   The platform held 9 comparable Ayala posts in the prior-year window against
   1,006 in the current one, which is too thin a base to confirm direction.
   The page says so in the method note — keep that note if you republish the
   numbers anywhere else.
2. **Whitespace verdicts are capped at "POSSIBLE WHITESPACE — UNVERIFIED".**
   They come from a two-cohort content read (274 Ayala-set posts vs 762
   competitor-set posts), not from an audience-demand panel. The page never
   claims audience demand, and rewording it to do so would not be supportable.

No impact statistics appear anywhere on the page: Ayala's own public counters
render as placeholders, so there was nothing verifiable to cite. If the
Foundation supplies audited figures, they can be dropped into the Overview
view — but they should be sourced on the page itself.

---
Prepared with SOMIN · data pulled 2026-09-18 · 12 monthly windows to Sep 2026
