-- Reading List schema. Run this in Supabase SQL Editor.

create table if not exists books (
    id bigserial primary key,
    user_id text not null default 'tsogt',
    title text not null,
    author text not null,
    status text not null default 'to_read' check (status in ('to_read', 'reading', 'finished')),
    rating int check (rating between 1 and 5),
    review text,
    finished_at date,
    created_at timestamptz not null default now()
);

create table if not exists goals (
    id bigserial primary key,
    user_id text not null unique default 'tsogt',
    year int not null,
    target int not null check (target > 0),
    updated_at timestamptz not null default now()
);

create index if not exists books_user_status_idx on books (user_id, status);
create index if not exists books_user_finished_idx on books (user_id, finished_at);
