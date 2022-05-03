CREATE TABLE IF NOT EXISTS warns (
  id serial PRIMARY KEY,
  user_id bigint NOT NULL,
  moderator_id bigint NOT NULL,
  moderator_name text NOT NULL,
  reason text,
  created_at timestamp NOT NULL DEFAULT now()
);