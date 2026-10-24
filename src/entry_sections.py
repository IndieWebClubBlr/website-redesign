"""Shared entry sections for the homepage and writings page."""

from __future__ import annotations

import random
from dataclasses import dataclass

from src import config
from src.feeds import FeedEntry, entry_ctx, group_feed_entries


@dataclass(frozen=True)
class EntrySections:
    """Template-ready entry groups used by the homepage and writings page."""

    recent: list[dict[str, str | bool]]
    week_notes: list[dict[str, str | bool]]
    random_posts: list[dict[str, str | bool]]
    on_this_day: list[dict[str, str | bool]]
    has_random_posts: bool
    has_on_this_day: bool


def _past_entry_ctx(entry: FeedEntry, current_year: int) -> dict[str, str | bool]:
    """Build entry context with "N years ago" fields for on-this-day.

    Args:
        entry: Entry from a previous year.
        current_year: Current year in the site timezone.

    Returns:
        Entry context with years_ago and years_text keys added.
    """
    ctx = entry_ctx(entry)
    years_ago = current_year - entry.published.year
    ctx.update(
        {
            "years_ago": f"{years_ago}",
            "years_text": (
                f"{years_ago} year" if years_ago == 1 else f"{years_ago} years"
            ),
        }
    )
    return ctx


def build_entry_sections(
    all_entries: list[FeedEntry],
    weeknote_entries: list[FeedEntry],
    other_entries: list[FeedEntry],
    on_this_day_entries: list[FeedEntry],
    current_year: int,
    rng: random.Random | None = None,
) -> EntrySections:
    """Build the shared recent, weeknote, on-this-day, and random sections.

    The homepage takes only the first few recent entries; the writings page
    renders the full result. Keeping both on this function means the two
    pages cannot drift apart.

    Args:
        all_entries: Every fetched entry, including the ones already shown.
        weeknote_entries: Entries classified as weeknotes.
        other_entries: Entries that are not weeknotes.
        on_this_day_entries: Entries published on this day in earlier years.
        current_year: Current year in the site timezone.
        rng: Optional random source, useful for deterministic builds/tests.

    Returns:
        Template-ready entry groups and their presence flags.
    """
    shown_entries = group_feed_entries(other_entries)[: config.MAX_SHOWN_POSTS]
    shown_weeknotes = group_feed_entries(weeknote_entries)[
        : config.MAX_SHOWN_WEEK_NOTES
    ]
    shown_on_this_day = on_this_day_entries

    shown_links = {
        entry.link for entry in shown_entries + shown_weeknotes + shown_on_this_day
    }
    available_for_random = [e for e in all_entries if e.link not in shown_links]

    feeds_seen: set[str] = set()
    random_posts: list[FeedEntry] = []
    random_source = rng or random.Random()
    random_source.shuffle(available_for_random)
    for entry in available_for_random:
        if entry.feed_home_url not in feeds_seen:
            feeds_seen.add(entry.feed_home_url)
            random_posts.append(entry)
            if len(random_posts) >= config.MAX_SHOWN_RANDOM_POSTS:
                break

    return EntrySections(
        recent=[entry_ctx(entry) for entry in shown_entries],
        week_notes=[entry_ctx(entry) for entry in shown_weeknotes],
        random_posts=[entry_ctx(entry) for entry in random_posts],
        on_this_day=[
            _past_entry_ctx(entry, current_year) for entry in shown_on_this_day
        ],
        has_random_posts=len(random_posts) > 0,
        has_on_this_day=len(shown_on_this_day) > 0,
    )
