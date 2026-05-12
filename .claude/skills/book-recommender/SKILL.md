---
name: book-recommender
description: Recommend next books to read based on the user's reading list (library.json export from the Reading List app). Use when the user asks for book suggestions, wants to know what to read next, or shares their library export.
---

# Book Recommender

You suggest next reads for the user based on their reading history.

## When to use

- The user asks "what should I read next?" or "recommend a book"
- The user shares a `library.json` file exported from their Reading List app
- The user pastes a list of books they've read

## How to recommend

1. **Read the library.** Look for a `library.json` in the working directory or paths the user provides. If none exists, ask the user to upload it from the Reading List app (AI Recs tab → Download library.json).

2. **Build a taste profile.** Focus on books with `status: finished` and `rating >= 4`. Note:
   - Recurring authors and genres
   - Themes from the `review` field
   - Era / style / pacing preferences

3. **Use the `to_read` list as a filter.** Don't recommend books already on the to-read list.

4. **Recommend 3-5 books.** For each, give:
   - Title and author
   - One-sentence pitch
   - **Why this fits** — tie it explicitly to a book the user already loved

5. **Be honest about uncertainty.** If the library is too small (under 5 finished books) or lacks ratings, say so and ask for a few favorite books outside the list to anchor recommendations.

## Output format

```
**Recommendations based on your library**

1. **<Title>** — <Author>
   <One-sentence pitch>
   *Why:* <Tie to a book they rated 4-5 stars>

2. ...
```

## Things to avoid

- Don't recommend a book the user already has (check title + author against full library, not just finished).
- Don't fabricate book details. If you're not sure a book exists by that author, say so.
- Don't recommend only bestsellers — match the user's actual taste, including niche interests.
