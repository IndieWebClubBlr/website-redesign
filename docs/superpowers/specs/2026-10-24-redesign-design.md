# IndieWebClub Bangalore — Website Redesign

**Date:** 2026-10-24
**Status:** Design for review
**Repo:** `iwcb-website-redesign`

## Intent

The current site is a long, dense feed page with no global navigation. A first-time visitor sees a decorative header, a wall of links, and a collection of posts, but no clear answer to “where do I start?”. The club’s real destinations—events, member writing, the member directory, and basic information about the club—are buried inside section link lists.

This redesign turns the site into a clear community front door while keeping the playful, handmade personality of the current design. The visual direction is a riso-print zine: electric blue, cream, orange, and yellow; condensed display type; typewriter labels; hard rules and offset shadows. It is deliberately raw, but not at the expense of readability or accessibility.

## Goals

- Give the site one obvious top-level structure: **Events · Writings · Members · About**, plus a **Join us** action.
- Make the homepage orient a newcomer, show the next event, and surface the latest member writing without becoming a feed dump.
- Create a dedicated Events page and a dedicated Writings page.
- Keep the archive, search, member directory, newsletter, webring, topics, prompts, and code of conduct, restyled into the same system.
- Preserve all existing feed, calendar, OPML, archive, search, and webring URLs.
- Work from 320px phones to large desktop displays.
- Work in automatic light and dark mode with WCAG AA contrast for text.
- Remove the current wobble animation and dense link lists.

## Non-goals

- No JavaScript framework, build step, or client-side router.
- No backend, database, or server-side search.
- No change to feed fetching, feed parsing, event fetching, search indexing, or webring generation.
- No manual theme toggle; the site follows `prefers-color-scheme`.
- No change to `/archive/` URLs or per-year archive URLs.
- No change to Atom, iCalendar, OPML, or webring redirect URLs.
- No redesign of the WhatsApp redirect page; it stays a redirect.
- No content migration beyond the new About page and the rewritten homepage/events/writings copy.

## Anti-goals

- A generic minimal blog theme that loses the club’s character.
- A “retro” skin that is noisy, low-contrast, or hard to read.
- Keeping every existing homepage section and merely re-skinning it.
- Adding a hero image or stock photography.
- Adding motion, marquees, or animated backgrounds.
- Hiding important links behind hover-only interactions.

## Constraints

- The generator uses Pystache (logic-less Mustache). Computed values and navigation state must be prepared in Python.
- GitHub Pages serves static files; there is no server runtime.
- One stylesheet (`assets/style.css`) drives the public site.
- Fonts must be self-hosted for visual consistency across macOS, Windows, Linux, and Android.
- Event data comes from the existing Discourse event fetcher (`src/events.py`).
- Member writing comes from the existing feed pipeline (`src/feeds.py`).
- Search, archive, members, newsletter, and webring keep their existing generation logic and JavaScript.
- No test suite exists. Verification is `basedpyright`, `black`, a full build, and a manual browser pass.
- Markup stays semantic and simple: native landmarks, headings, lists, articles, forms, and `<details>`; no presentational wrapper divs and no div soup. CSS carries the visual design.

## Approaches Considered

### 1. Reskin only

Keep the existing page structure, rewrite `style.css`, add a sticky nav.

**Why rejected:** It fixes the colour and typography but not the stated problem. The homepage would still be a long feed dump, and Events, Writings, Members, and About would still be buried. It also cannot remove the repeated subscribe/OPML/calendar link clusters without restructuring templates.

### 2. Restructure and restyle the whole generated site

Introduce four top-level destinations, add `/events/` and `/writings/`, add `/about/`, reduce the homepage to four sections, and apply one visual system to every generated page.

**Why chosen:** It solves the findability problem and the visual problem together. It preserves the generator, feeds, and URLs. It is more work than a reskin but the work is mostly template and CSS work, not new infrastructure.

### 3. Rebuild as a JavaScript site

Move to Astro/Next/etc.

**Why rejected:** The current site already works as a static generator. A framework rewrite adds build complexity, new dependencies, and risk without improving the content or the navigation. The redesign can be done inside the current stack.

## Decisions

### Navigation

Top-level navigation:

- **Events** → `/events/`
- **Writings** → `/writings/`
- **Members** → `/members/`
- **About** → `/about/`
- **Join us** → `/whatsapp` (existing redirect to the WhatsApp group)

The logo links to `/`. The archive stays at `/archive/` and is linked from Writings, the footer, and the sitemap; it is not a fifth top-level item.

Current-section mapping for `aria-current="page"`:

| Section | Pages |
|---|---|
| Events | `/events/`, `/topics/`, `/prompts/` |
| Writings | `/writings/`, `/archive/`, `/search/` |
| Members | `/members/`, `/webring/` |
| About | `/about/`, `/coc/` |

Desktop: logo left, nav links and Join us right. The header is sticky with a solid background and a 2px bottom rule.

Mobile: the same single `<nav>` wraps below the logo. The four links stay visible and the Join us button becomes full width. No disclosure, no duplicate nav, no JavaScript. This is simpler and more robust than a mobile menu, and it keeps one `Main` navigation landmark.

### Page Map

| URL | Status | Purpose |
|---|---|---|
| `/` | Rewritten | Homepage: orient, next event, latest writing, newsletter |
| `/events/` | New | Upcoming and past events, calendar/feed links, topics/prompts |
| `/writings/` | New | Recent member writing, links to archive/search/feeds |
| `/members/` | Restyled | Existing directory and membership requirements |
| `/about/` | New | What the club is, how to join, community standards |
| `/archive/` | Restyled | Existing year-based archive; URL unchanged |
| `/archive/<year>/` | Restyled | Existing per-year archive; URL unchanged |
| `/search/` | Restyled | Existing tinysearch page |
| `/newsletter/` | Restyled | Existing newsletter form and past issues |
| `/webring/` | Restyled | Existing webring tool |
| `/topics/` | Restyled | Existing event topics |
| `/prompts/` | Restyled | Existing writing prompts |
| `/coc/` | Restyled | Existing code of conduct |
| `/whatsapp/` | Unchanged | Redirect to WhatsApp |
| `/2026-se/` | Unchanged | Standalone special-edition campaign page; intentionally outside the main shell |
| `/indiewebclub-blr-website/` | Unchanged | Redirect to `/` |

Standalone campaign pages such as `/2026-se/` are a deliberate exception. They keep their own full-bleed layouts, styles, and JavaScript. The shared shell applies to generated site pages, not to one-off campaign pages. Future campaign pages follow the same rule.

### Homepage

Four sections only:

1. **Hero**
   - Eyebrow: “Bangalore · since 2023”
   - H1: “A home for people who make the web.”
   - One short paragraph explaining the club.
   - Primary CTA: **Come to an event** → `/events/`
   - Secondary CTA: **Join the WhatsApp group** → `/whatsapp`
   - Event card:
     - If an upcoming event exists: kicker “Next event”, title, date/time, venue, ticket link when available, and “See all events →”.
     - If no upcoming event exists: kicker “Next events”, “1st and 3rd Saturdays”, “Underline Center, Indiranagar”, “See past events →”. This replaces the current dead-end “No Upcoming Events” block.

2. **Latest from members**
   - Six posts, using the current “Recent Posts” fairness rule: group by feed and show at most one latest post per member, then take the first six.
   - This is the same source and grouping as the current homepage’s “Recent Posts by Members”, just shorter.
   - Each item: title (link), author, date. No summaries.
   - Link: “All writings →” → `/writings/`.

3. **Newsletter**
   - One short line: “Get the weekly digest of member writing.”
   - Existing email form, restyled.
   - Link to `/newsletter/` for past issues.

4. **Footer**
   - Code of Conduct, Source, RSS, “Last generated”, IndieWeb badge.
   - No CoC or webring body sections on the homepage.

Removed from the homepage: weeknotes, on-this-day, random posts, previous events, webring, CoC section, and the long list of subscribe/download/OPML links.

### Events Page (`/events/`)

- H1 “Events”.
- Intro: meetups happen on the 1st and 3rd Saturdays at Underline Center, Indiranagar; everyone is welcome; no tech background needed.
- Upcoming event cards, using the existing Discourse event data:
  - Title, date/time, location, agenda summary, ticket link.
  - If none: the same “1st and 3rd Saturdays” fallback as the homepage.
- Subscribe strip: Events Atom, webcal, download `.ics`, topics, prompts.
- Past events: every past event the fetcher returns. The fetcher currently caps past events at 10, so the page shows what is available rather than adding pagination or changing the fetch.
- The page is generated by a new `events_page` build rule depending on the existing `events` rule.
- New template: `templates/events.html`.

### Writings Page (`/writings/`)

- H1 “Writings”.
- Intro: “Recent posts from members of IndieWebClub Bangalore.”
- This page takes over the editorial content that used to live on the homepage, using **exactly the current homepage logic**:
  - **Recent Posts by Members** — current per-feed grouping, one latest post per member, up to `MAX_SHOWN_POSTS`.
  - **Day/Week/Month Notes by Members** — the current weeknote stream, up to `MAX_SHOWN_WEEK_NOTES`.
  - **On This Day in Previous Years** — the current same-day historical entries.
  - **Some Random Posts** — the current one-per-feed random selection, up to `MAX_SHOWN_RANDOM_POSTS`.
- The section markup, entry context, microformats, headings, and “years ago” badges move over unchanged in meaning.
- A utility row at the top replaces the old scattered subscribe/download lists: RSS with links, RSS with content, weeknotes feed, replay feed, OPML, archive, search, newsletter, member directory.
- The existing `/archive/` remains the complete year-by-year view.
- Do not duplicate the homepage logic in a second implementation: extract a shared context builder that both pages use. The homepage takes only the six-post recent list; Writings takes the full context.
- New template: `templates/writings.html`.

### About Page (`/about/`)

New Markdown page written from existing site copy. Sections:

- What IndieWebClub is.
- Who it is for (bloggers, tinkerers, people with no tech background).
- When and where we meet.
- What happens at a meetup.
- How to join: WhatsApp, Discourse, newsletter, email.
- Community standards: Code of Conduct link and moderation contact.
- Webring link.

The page uses the standard prose layout and standard shell.

### Members, Archive, Search, Newsletter, Webring, Topics, Prompts, CoC

Functionality is unchanged. Each page gets the new shell, typography, palette, focus states, and responsive rules.

- **Members:** directory becomes a two-column list on desktop and one column on mobile. Favicon, name, RSS link, and optional badges remain. Badges use high-contrast chips.
- **Archive:** year list, bar chart, and per-year details keep their behaviour. Chart colours come from the new palette. Search input and result counts remain.
- **Search:** input, status text, and results use the new typography and focus ring. Results remain title + metadata + link.
- **Newsletter:** form and past-issues list use the new form styles.
- **Webring:** form, result panel, and code block use the new styles. No logic change.
- **Topics/Prompts:** table of contents and prose sections use the standard prose layout.
- **CoC:** prose layout only.

### Special Edition Page (`/2026-se/`)

The standalone campaign page is **not changed**. It keeps its black/neon palette, Google-hosted fonts, layout, canvas animation, countdown, schedule, and content.

This is a deliberate exception, not an oversight: campaign pages are allowed to have their own visual identity. The shared redesign applies to the generated site shell and its pages. Future standalone campaign pages follow the same rule.

## Visual System

### Palette

The colours are intentionally limited. Light mode uses cream paper with blue ink; dark mode swaps paper and ink. Orange and yellow stay as accents in both.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#f6efdd` | `#1230b8` | Page background |
| `--ink` | `#1230b8` | `#f7f0da` | Body text, rules, header |
| `--muted` | `#5260a8` | `#c7d1f4` | Secondary metadata |
| `--accent-bg` | `#e7441e` | `#ff5a36` | Buttons, footer, large headline accent |
| `--accent-text` | `#a82a0d` | `#f2d64b` | Small links and labels |
| `--highlight` | `#f2d64b` | `#f2d64b` | Join button, event card, emphasis |
| `--card-bg` | `#f2d64b` | `#f2d64b` | Event card |
| `--on-accent` | `#111` | `#111` | Text on orange/yellow surfaces |
| `--focus` | `#1230b8` | `#f2d64b` | Focus outline |

Measured contrast:

- Blue on cream: 8.55:1
- Cream on blue: 8.61:1
- Small link orange on cream (`#a82a0d`): 6.10:1
- Small link yellow on blue (`#f2d64b`): 6.77:1
- Black on orange: 4.71:1 (light) / 6.09:1 (dark)
- Black on yellow: 13.03:1

Orange `#e7441e` / `#ff5a36` is used for large display text and as a background with black text, never as small text on cream or blue.

### Typography

Self-hosted, with system fallbacks:

- **Display:** Anton (SIL OFL), fallback `Impact, "Arial Narrow Bold", sans-serif`.
  - H1 hero: `clamp(2.6rem, 6vw, 4.4rem)`, line-height 0.92, uppercase.
  - Section headings: `clamp(1.6rem, 3vw, 2.1rem)`, uppercase.
  - Wordmark: two lines, uppercase, static offset shadows.
- **Body:** Gelasio (SIL OFL), fallback `Georgia, "Times New Roman", serif`.
  - 17–18px, line-height 1.6.
  - Body measure max 68ch.
- **Mono:** Courier Prime (SIL OFL), fallback `"Courier New", monospace`.
  - Navigation, buttons, labels, metadata, dates, footer.
  - Minimum 11px for metadata; 12px for nav/buttons; no 9px text.

Font files requested from the site owner:

- `anton-regular.woff2`
- `gelasio-regular.woff2`
- `gelasio-bold.woff2`
- `courier-prime-regular.woff2`
- `courier-prime-bold.woff2`

Place them in `assets/fonts/`, include the OFL licences, and list them in `src/generator.py` `ASSETS`. Use `font-display: swap`.

### Layout

- Page background is full-bleed; content is constrained to `max-width: 76rem` with responsive inline padding.
- Header and footer use the full-width background, with inner content aligned to the same grid.
- Desktop homepage hero: two columns, text left, event card right.
- Tablet: hero stacks; event card moves below the text.
- Mobile: single column everywhere; nav collapses to Menu; post dates move under titles.
- No card grid for posts. Posts are rows separated by rules.
- Event card is the one deliberately “pasted-on” object: yellow, 2px border, offset shadow, 1° rotation. On mobile the rotation is reduced to 0.4°.
- Decorative halftone dot texture is very low opacity and sits behind content; it never reduces text contrast.

### Components

- **Buttons:** rectangular, mono uppercase, 44px minimum height. Primary is orange with black text and a hard ink shadow. Secondary is underlined text.
- **Links:** underlined on hover/focus; small links use `--accent-text`.
- **Rules:** 2px ink borders between major sections; 1px muted rules between list rows.
- **Forms:** labelled, 44px inputs, visible focus ring, no placeholder-only labels.
- **Code blocks:** existing Pygments themes remain, adjusted to the new background.
- **Archive chart:** bars use `--accent-bg`; labels use `--ink`; count text uses `--on-accent`. If a count still fails contrast against a particular bar, move it above the bar rather than forcing a colour.
- **Member badges:** high-contrast chips; never colour-only.
- **Footer:** orange bar with black text; links underlined.

### Motion

No animation. The old logo wobble is removed. The static offset wordmark carries the personality. If any transition is added, it must respect `prefers-reduced-motion`.

## Accessibility Requirements

- Semantic landmarks: `<header>`, `<nav aria-label="Main">`, `<main id="main">`, `<footer>`.
- Skip link to `#main`.
- Exactly one `<h1>` per page.
- `aria-current="page"` on the current nav item, computed in Python from `page_url`.
- Focus visible: 3px outline, 3px offset, in `--focus`.
- All interactive targets at least 44×44 CSS px.
- Links are underlined as well as coloured.
- Text contrast meets WCAG AA: 4.5:1 for normal text, 3:1 for large text.
- The mobile menu is a native `<details>`/`<summary>` disclosure; the summary has a visible label and a 44px target.
- No information conveyed by colour alone. Event dates, “Next”, badges, and current nav all have text labels.
- `<time datetime="…">` for event and post dates.
- Forms keep visible `<label>` elements.
- The archive chart has a caption; the year links remain text links.
- No animation; `prefers-reduced-motion` respected if transitions are introduced.

### IndieWeb Semantics

The redesign preserves and extends the current microformats and Bridgy Fed markup:

- **Club `h-card`** — keep `p-name`, `u-url u-uid`, `u-photo`, and `rel="me"` links. Move it to the About page, where the club description now lives. The homepage hero can also carry the `h-card` if it remains a single unobtrusive wrapper.
- **Posts** — keep `h-entry`, `p-name`, `u-url u-uid`, `p-author h-card`, `dt-published`, and `p-summary` where summaries are shown. Apply to the homepage six, the Writings sections, and On This Day.
- **Events** — keep `h-event h-entry`, `p-name`, `u-url`, `dt-start`, `dt-end`, `p-location`, `e-content`, and the hidden `u-bridgy-fed` link. Apply on both the homepage event card and `/events/`.
- **Feeds and rel=me** — keep the existing `rel="me"` links and feed autodiscovery.
- **Visible text** — microformat classes are added to the visible elements; do not create hidden duplicate content except for the existing `u-bridgy-fed` and `u-photo` patterns.

## Technical Design

### Templates

- `templates/default.html`
  - Skip link, header, desktop nav, mobile `<details>` nav, main, footer.
  - Uses `nav_*` booleans from Python for active state.
  - Adds `scroll-padding-top` for the sticky header.
- `templates/index.html`
  - New four-section homepage.
  - Event card handles upcoming and empty states.
- `templates/events.html` (new)
  - Upcoming/past event lists and subscription strip.
- `templates/writings.html` (new)
  - The current homepage’s recent/weeknotes/on-this-day/random sections, moved over with their existing entry context and microformats.
  - Utility row for feeds, OPML, archive, search, newsletter, and members.
- `templates/members.html`
  - Same data, new list layout and badges.
- `templates/archive-index.html`, `templates/archive-year.html`
  - New classes; preserve `details`, search input, chart.
- `templates/search.html`, `templates/nl-subsribe.html`, `templates/nl-form.html`, `templates/webring.html`
  - New classes and form styles; logic unchanged.
- `templates/topics.html`, `templates/prompts.html`
  - New prose/TOC classes; logic unchanged.
- `templates/webring-redirect.html`
  - Unchanged or only minor meta styling.

### Python

- `src/utils.py`
  - `render_and_save_html` computes `nav_home`, `nav_events`, `nav_writings`, `nav_members`, `nav_about` from `page_url`.
  - Pass them to `default.html`.
- `src/generator.py`
  - Extract a shared `build_entry_context(...)` helper that produces the current recent/weeknotes/on-this-day/random data and entry contexts.
  - `generate_homepage`: use the helper, take the first six recent posts, and build only the new homepage context (next event, empty-event fallback, newsletter).
  - `generate_writings_page`: use the same helper and render the full current-homepage content sections.
  - Add `generate_events_page(events, output_dir)`.
  - Add build rules `events_page` (needs `events`) and `writings_page` (needs `feeds`). `writings_page` also needs `search_page` if it renders the current search link.
  - Add both to `sitemap` dependencies and `website` demand.
  - Add new templates to `read_template` calls.
- `src/config.py`
  - `MAX_SHOWN_HOMEPAGE_POSTS = 6`
  - Keep `MAX_SHOWN_POSTS`, `MAX_SHOWN_WEEK_NOTES`, and `MAX_SHOWN_RANDOM_POSTS` as the Writers page limits.
  - Keep `MAX_SHOWN_EVENTS` as the fetcher’s past-event cap; the Events page shows whatever the fetcher returns.
- `pages/about.md`
  - New content.
- `pages/coc.md`
  - No content change expected; prose styling only.

### Assets

- `assets/style.css`
  - Full rewrite around design tokens, components, responsive rules, and existing component styles (archive, members, webring, search, code highlighting).
  - Keep existing class names where templates rely on them, or update both together.
- `assets/fonts/*.woff2`, `assets/fonts/OFL-*.txt`
  - New self-hosted fonts and licences.
- `assets/favicon.svg`
  - Update to the new palette: blue field, cream “IWCB”, orange/yellow offset.
- `assets/preview.png`
  - Optional but recommended: update the Open Graph image to the new palette. Not a blocker.
- `src/generator.py` `ASSETS`
  - Add fonts and any new assets.

### Data Flow

- Events page uses `cache.events` from the existing `events` rule.
- Writings page uses `cache.entries`, `cache.weeknote_entries`, and `cache.on_this_day_entries` from the existing `feeds` rule, with the current homepage logic.
- Homepage uses the same recent-post data, limited to six entries with the existing one-per-feed grouping.
- Search, archive, members, newsletter, and webring code paths are unchanged.
- No new network requests.

### URL and Feed Compatibility

All existing URLs remain:

- `/`, `/archive/`, `/archive/<year>/`, `/members/`, `/search/`, `/newsletter/`, `/webring/`, `/topics/`, `/prompts/`, `/coc/`, `/whatsapp/`, `/2026-se/`
- `/blogroll.atom`, `/blogroll-latest.atom`, `/blogroll-weeknotes.atom`, `/events.atom`, `/topics.atom`, `/prompts.atom`, `/events.ics`, `/blogroll.opml`
- `/webring/previous.html`, `/webring/next.html`, per-member redirects and embeds

New URLs: `/events/`, `/writings/`, `/about/`.

### Responsive Breakpoints

- `>= 1024px`: full desktop header, two-column hero, two-column member list.
- `760–1023px`: header may still be full; hero stacks; event card below text; content padding reduces.
- `<= 759px`: mobile header with `<details>` menu; single-column everything; post dates stack; event card rotation reduces; footer stacks.
- `<= 420px`: type scales down via `clamp`; buttons go full width where appropriate.
- `>= 1600px`: content remains at 76rem; no stretched line lengths.

### Verification

- `basedpyright src/`
- `black src/*.py`
- Full build: `nix-shell --run 'make build'` (or `make build CACHE_FALLBACK=true` if network is available)
- Serve `_site/` and check:
  - Home, Events, Writings, Members, About, Archive, Search, Newsletter, Webring, Topics, Prompts, CoC.
  - Desktop at 1440px, tablet at 900px, mobile at 390px and 320px.
  - Light and dark system themes.
  - Keyboard tab order, skip link, mobile menu, focus ring.
  - Nav active state on each section.
  - No horizontal overflow.
  - Event card both with and without upcoming events.
  - Members badges, archive chart, search results, newsletter form, webring form.
  - `/2026-se/` still renders unchanged as a standalone page.
- Link check generated HTML for broken internal links.
- Confirm Atom/ICS/OPML files still generate.
- Confirm sitemap includes `/events/`, `/writings/`, `/about/`.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| New fonts change wrapping and break the hero | Test at 320/390/768/1440; use `clamp()`; keep fallback stacks |
| Sticky header covers anchor targets | `scroll-padding-top` equal to header height; test in-page anchors |
| Pystache strict mode fails on new tags | Build early after template changes; add nav flags in Python |
| Removing homepage sections breaks links | Keep `#upcoming-events` style anchors? Add redirects or update all internal links; grep for old anchors |
| Archive chart colours become illegible | Use palette tokens and test in both themes |
| Event page duplicates homepage logic | Extract a small event-context helper in Python |
| Writings page duplicates homepage logic | Extract a shared entry-context helper used by both pages |
| Standalone campaign pages drift | Keep `/2026-se/` and future campaign pages out of the shared shell by design |
| Font files not ready | Build with fallbacks; add `@font-face` once files are present |
| Overly busy zine texture hurts readability | Keep dot texture very low opacity; no texture behind body copy |

## Open Items for the Builder

- Obtain and add the five WOFF2 font files and OFL licences.
- Write the final About page copy from the existing intro/CoC/moderation text.
- Decide whether to update `preview.png`; not a blocker.
- Run the full build against live feeds once, then use cached builds for iteration.

## Approval

This document is the design of record once approved. The implementation plan will be written after approval.
