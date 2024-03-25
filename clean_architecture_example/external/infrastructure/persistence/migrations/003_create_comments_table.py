from yoyo import step

up_sql = """
CREATE TABLE IF NOT EXISTS comments (
    id UUID PRIMARY KEY,
    content VARCHAR NOT NULL,
    post_id UUID NOT NULL,
    owner_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (owner_id) REFERENCES users(id)
);
"""


down_sql = """DROP TABLE IF EXISTS comments;"""


steps = [
    step(up_sql, down_sql),
]
