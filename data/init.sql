DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS groups;

CREATE TABLE groups (
       id SERIAL PRIMARY KEY,
       title TEXT NOT NULL,
       gateway_id BIGINT UNIQUE NOT NULL,
       moderate_id BIGINT UNIQUE NOT NULL,
       private_group_id BIGINT UNIQUE NOT NULL,
       admins BIGINT[] DEFAULT ARRAY[]::BIGINT[] NOT NULL,
       invite_link TEXT DEFAULT '' NOT NULL,
       clean_interval INTEGER DEFAULT 1440 NOT NULL,
       prompt TEXT DEFAULT 'Tell me your interest in joining the group' NOT NULL,
       refresh_interval INTEGER DEFAULT 5 NOT NULL,
       CONSTRAINT sane_values CHECK ((clean_interval > 0) AND (LENGTH(TRIM(prompt)) > 0) AND (refresh_interval > 0))
);

CREATE TABLE users (
       id INTEGER REFERENCES groups ON DELETE CASCADE NOT NULL,
       user_id BIGINT NOT NULL,
       joined TIMESTAMP DEFAULT NOW() NOT NULL,
       in_gateway BOOL DEFAULT FALSE NOT NULL,
       in_private_group BOOL DEFAULT FALSE NOT NULL,
       approved BOOL DEFAULT FALSE NOT NULL,
       restricted BOOL DEFAULT FALSE NOT NULL,
       PRIMARY KEY (id, user_id)
);
