from yoyo import step

up_sql = """
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);
"""

down_sql = """DROP TABLE IF EXISTS users;"""

steps = [
    step(up_sql, down_sql),
]
