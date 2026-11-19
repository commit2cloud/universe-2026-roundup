# GitHub Universe 2026 announcement roundup

A customer-facing static guide to the 35 GitHub Changelog entries published during Universe week, October 26-November 1, 2026. Includes official links, short summaries, release-stage labels, plan and billing caveats, and the keynote and Octoverse report.

The event took place October 28-29. Public sources were reviewed November 19, 2026. Later corrections are explicitly noted; the guide does not imply that every feature was generally available at the event.

## Run locally

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000`. The complete guide is also readable directly from `index.html`, with or without JavaScript.

## Test

The browser check uses Python Playwright and Chromium:

```bash
python3 test_site.py
```

It checks search and category combinations, empty states, reset, deep links, mobile layout, theme switching, and no-JavaScript access to every announcement.

## GitHub Pages

Publish the `main` branch's root directory through GitHub Pages. `.nojekyll` keeps the site a plain static page. No build system, secrets, analytics, or external runtime dependencies are needed.

The HTML contains all styles and scripts. Its only outbound requests are the official links a reader chooses to open.

## Editorial scope

- One list item per changelog entry returned for October 26 through November 1, 2026, inclusive.
- Additional links to the keynote summary, Octoverse, and official event recap.
- Release stages are based on the announcement, with subsequent corrections noted. Documentation is linked for selected adoption-sensitive topics.
- No internal information, account details, unannounced features, or customer data.
- This is an editorial guide, not an official GitHub release document or contractual statement.

To update the guide, check the original announcements and relevant GitHub Docs, amend the review date and any availability notes, and run the browser check. Do not silently add later releases to the Universe-week list.
