DROP TABLE IF EXISTS password_history;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email_address TEXT NOT NULL,
    pass_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    password_created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE password_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    pass_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    prep_time INTEGER,
    cook_time INTEGER,
    servings INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE likes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (recipe_id) REFERENCES recipes (id),
    UNIQUE(user_id, recipe_id)
);
