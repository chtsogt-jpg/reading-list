from datetime import date
from typing import Any
import streamlit as st
from supabase import create_client, Client

USER_ID = "tsogt"


@st.cache_resource
def get_client() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


def list_books(status: str | None = None, search: str | None = None) -> list[dict[str, Any]]:
    q = get_client().table("books").select("*").eq("user_id", USER_ID)
    if status:
        q = q.eq("status", status)
    if search:
        term = f"%{search}%"
        q = q.or_(f"title.ilike.{term},author.ilike.{term}")
    return q.order("created_at", desc=True).execute().data


def add_book(title: str, author: str, status: str) -> None:
    get_client().table("books").insert({
        "user_id": USER_ID,
        "title": title.strip(),
        "author": author.strip(),
        "status": status,
    }).execute()


def update_book(book_id: int, **fields: Any) -> None:
    if "status" in fields and fields["status"] == "finished" and "finished_at" not in fields:
        fields["finished_at"] = date.today().isoformat()
    get_client().table("books").update(fields).eq("id", book_id).execute()


def delete_book(book_id: int) -> None:
    get_client().table("books").delete().eq("id", book_id).execute()


def get_goal(year: int) -> int:
    res = get_client().table("goals").select("target").eq("user_id", USER_ID).eq("year", year).execute()
    return res.data[0]["target"] if res.data else 0


def set_goal(year: int, target: int) -> None:
    client = get_client()
    existing = client.table("goals").select("id").eq("user_id", USER_ID).execute().data
    if existing:
        client.table("goals").update({"year": year, "target": target}).eq("user_id", USER_ID).execute()
    else:
        client.table("goals").insert({"user_id": USER_ID, "year": year, "target": target}).execute()


def count_finished_this_year(year: int) -> int:
    res = (
        get_client()
        .table("books")
        .select("id", count="exact")
        .eq("user_id", USER_ID)
        .eq("status", "finished")
        .gte("finished_at", f"{year}-01-01")
        .lte("finished_at", f"{year}-12-31")
        .execute()
    )
    return res.count or 0
