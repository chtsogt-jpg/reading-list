from datetime import date
import json
import streamlit as st
import db

st.set_page_config(page_title="My Reading List", page_icon="📚", layout="wide")

STATUS_LABELS = {"to_read": "📖 To Read", "reading": "👀 Reading", "finished": "✅ Finished"}
STATUS_OPTIONS = list(STATUS_LABELS.keys())


def render_book_card(book: dict) -> None:
    with st.container(border=True):
        top = st.columns([4, 1])
        with top[0]:
            st.markdown(f"### {book['title']}")
            st.caption(f"by *{book['author']}*")
        with top[1]:
            st.markdown(f"**{STATUS_LABELS[book['status']]}**")

        if book.get("rating"):
            st.markdown("⭐" * book["rating"] + "☆" * (5 - book["rating"]))
        if book.get("review"):
            st.markdown(f"> {book['review']}")

        with st.expander("Edit"):
            new_status = st.selectbox(
                "Status",
                STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(book["status"]),
                format_func=lambda s: STATUS_LABELS[s],
                key=f"status_{book['id']}",
            )
            new_rating = st.slider(
                "Rating", 0, 5, value=book.get("rating") or 0, key=f"rating_{book['id']}"
            )
            new_review = st.text_area(
                "Short review", value=book.get("review") or "", key=f"review_{book['id']}"
            )
            cols = st.columns(2)
            if cols[0].button("Save", key=f"save_{book['id']}", use_container_width=True):
                db.update_book(
                    book["id"],
                    status=new_status,
                    rating=new_rating or None,
                    review=new_review or None,
                )
                st.success("Saved")
                st.rerun()
            if cols[1].button("Delete", key=f"del_{book['id']}", type="secondary", use_container_width=True):
                db.delete_book(book["id"])
                st.rerun()


def page_library() -> None:
    st.subheader("📚 My Library")

    filter_cols = st.columns([2, 1])
    search = filter_cols[0].text_input("Search by title or author", placeholder="e.g. Tolkien, 1984...")
    status_filter = filter_cols[1].selectbox(
        "Filter by status",
        [None] + STATUS_OPTIONS,
        format_func=lambda s: "All" if s is None else STATUS_LABELS[s],
    )

    books = db.list_books(status=status_filter, search=search or None)
    if not books:
        st.info("No books yet. Add one in the **Add Book** tab.")
        return

    st.caption(f"{len(books)} book{'s' if len(books) != 1 else ''}")
    for i in range(0, len(books), 2):
        cols = st.columns(2)
        for j, book in enumerate(books[i:i + 2]):
            with cols[j]:
                render_book_card(book)


def page_add() -> None:
    st.subheader("➕ Add a Book")
    with st.form("add_book", clear_on_submit=True):
        title = st.text_input("Title", placeholder="The Hobbit")
        author = st.text_input("Author", placeholder="J.R.R. Tolkien")
        status = st.selectbox(
            "Status", STATUS_OPTIONS, format_func=lambda s: STATUS_LABELS[s]
        )
        if st.form_submit_button("Add Book", type="primary", use_container_width=True):
            if not title.strip() or not author.strip():
                st.error("Title and author are required.")
            else:
                db.add_book(title, author, status)
                st.success(f"Added **{title}** by *{author}*")


def page_goal() -> None:
    st.subheader("🎯 Reading Goal")
    year = date.today().year
    current_goal = db.get_goal(year)
    finished = db.count_finished_this_year(year)

    if current_goal:
        progress = min(finished / current_goal, 1.0)
        st.markdown(f"### {finished} / {current_goal} books read in {year}")
        st.progress(progress)
        remaining = max(current_goal - finished, 0)
        if remaining == 0:
            st.success(f"🎉 You hit your goal! {finished} books finished.")
        else:
            st.caption(f"{remaining} to go — {int(progress * 100)}% there")
    else:
        st.info(f"No goal set for {year}. Set one below to start tracking.")

    with st.expander("Set or update goal"):
        target = st.number_input(
            "Books to read this year",
            min_value=1, max_value=500,
            value=current_goal or 12,
        )
        if st.button("Save goal", type="primary"):
            db.set_goal(year, int(target))
            st.success(f"Goal set: {target} books in {year}")
            st.rerun()


def page_export() -> None:
    st.subheader("🤖 AI Recommendations")
    st.markdown(
        "This app ships with a **`book-recommender`** Claude Code skill. "
        "Export your library below, then run `/book-recommender` in Claude Code "
        "to get reads tailored to your taste."
    )
    books = db.list_books()
    if not books:
        st.info("Add some books first — the recommender needs your taste profile.")
        return

    export = [
        {
            "title": b["title"],
            "author": b["author"],
            "status": b["status"],
            "rating": b.get("rating"),
            "review": b.get("review"),
        }
        for b in books
    ]
    st.download_button(
        "📥 Download library.json",
        data=json.dumps(export, indent=2),
        file_name="library.json",
        mime="application/json",
        use_container_width=True,
    )
    with st.expander("Preview"):
        st.json(export)


def main() -> None:
    st.title("📚 My Reading List")
    tabs = st.tabs(["Library", "Add Book", "Reading Goal", "AI Recs"])
    with tabs[0]:
        page_library()
    with tabs[1]:
        page_add()
    with tabs[2]:
        page_goal()
    with tabs[3]:
        page_export()


if __name__ == "__main__":
    main()
