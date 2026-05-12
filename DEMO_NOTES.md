# Week 16 Demo — 10-15 min outline

## 1. Hook (30 sec)
> "I read a lot but I never remember which books I loved. So I built a reading tracker that doubles as an AI book recommender."

## 2. Live demo (5 min)
- Open deployed app on streamlit.app
- Add a new book (form clears, appears in library)
- Change status To-Read → Finished (auto-stamps date)
- Rate it 5 stars + short review
- Show search: type author's surname → grid filters
- Show reading goal: progress bar updates
- Open **AI Recs** tab → download library.json
- Switch to terminal → `/book-recommender` in Claude Code → show 3-5 tailored picks

## 3. Architecture (2 min)
- Show repo tree
- Explain `app.py` (UI only) vs `db.py` (data layer) — clean separation
- Schema: two tables, `books` and `goals`, both keyed by `user_id` so social mode is a future flip

## 4. Git history (1 min)
- `git log --oneline` — show feature-branch commits

## 5. AI collaboration (2 min)
- Used Claude Code to scaffold + iterate
- Built a real Claude Code Skill (`book-recommender`) as the required advanced feature
- Skill lives in `.claude/skills/` — graders can run `/book-recommender` themselves on the included `library.json`

## 6. Lessons learned (1 min)
- What worked: starting with deployment on day 1
- What I'd change: ___ (fill in after building for real)
- What surprised me: ___

## 7. Q&A
