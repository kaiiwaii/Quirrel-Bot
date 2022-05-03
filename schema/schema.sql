CREATE TABLE IF NOT EXISTS warns (
  id serial PRIMARY KEY,
  user_id bigint NOT NULL,
  moderator_id bigint NOT NULL,
  moderator_name text NOT NULL,
  reason text,
  created_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS market (
  id serial PRIMARY KEY,
  name text NOT NULL,
  description text NOT NULL,
  price integer NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  id BIGINT PRIMARY KEY,
  balance INTEGER NOT NULL DEFAULT 0,
  inventory JSONB NOT NULL DEFAULT '{}'
);