# 📚 My Reading List

A personal reading tracker built as my Project 3 capstone. Add books, rate them, write short reviews, set a yearly goal, and watch your progress fill up.

**Live app:** https://reading-list-f9nhkkcntybdbjyqcs25nh.streamlit.app/

## Features

- **Library** — Browse all books in a card grid. Filter by status, search by title or author.
- **Add Book** — Quick form with title, author, and reading status.
- **Status tracking** — Move books between *To Read → Reading → Finished*. The status switch auto-stamps the finish date.
- **Star rating + review** — 1-5 stars and a short review per book.
- **Reading goal** — Set a yearly target. A progress bar tracks finished books for the current year.
- **AI recommendations** — Export your library as JSON and feed it to the bundled `book-recommender` Claude Code skill for tailored suggestions.

## Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| Database | Supabase (Postgres) |
| AI feature | Custom Claude Code Skill (`book-recommender`) |
| Deployment | streamlit.app |

## Architecture

```
reading-list/
├── app.py                    # Streamlit UI (tabs, forms, cards)
├── db.py                     # Supabase client + all DB queries
├── schema.sql                # Database tables (books, goals)
├── requirements.txt
├── .streamlit/
│   ├── config.toml           # Theme (warm parchment palette)
│   └── secrets.toml          # Supabase credentials (gitignored)
└── .claude/skills/book-recommender/
    └── SKILL.md              # AI recommendation skill
```

`app.py` handles only presentation. All database access is isolated in `db.py` so the UI never touches Supabase directly.

## Setup (local)

1. Clone this repo.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a Supabase project at [supabase.com](https://supabase.com).
4. In the Supabase SQL Editor, run the contents of `schema.sql`.
5. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in:
   ```toml
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-anon-public-key"
   ```
6. Run:
   ```bash
   streamlit run app.py
   ```

## Deployment

1. Push to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app.
3. Pick your repo and `app.py` as the entrypoint.
4. Under **Advanced settings → Secrets**, paste the same TOML from `.streamlit/secrets.toml`.
5. Deploy.

## Using the AI recommender

1. In the running app, go to the **AI Recs** tab and download `library.json`.
2. Drop the file into a folder where Claude Code can see it (or paste it inline).
3. Run `/book-recommender` in Claude Code (the skill auto-loads from `.claude/skills/`).
4. Get 3-5 recommendations tied directly to books you rated 4-5 stars.

## How Claude Code was used

- Scaffolded the Streamlit + Supabase boilerplate.
- Built the `book-recommender` skill as the required "advanced Claude Code feature."
- Iterated on UI polish (card layout, status badges, progress bar).

## Lessons learned

_To fill in after Week 16 demo: what worked, what didn't, what I'd do differently._
