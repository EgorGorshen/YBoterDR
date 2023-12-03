CREATE TABLE IF NOT EXISTS Users (
    telegram_id INTEGER PRIMARY KEY,
    name TEXT,
    number_of_tracks INTEGER DEFAULT 0, -- Установлено значение по умолчанию
    number_of_media INTEGER DEFAULT 0, -- Установлено значение по умолчанию
    on_the_party INTEGER DEFAULT 0 -- INTEGER для BOOLEAN, 0 = нет, 1 = да
);

CREATE TABLE IF NOT EXISTS Media (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    simlink TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(telegram_id) ON DELETE CASCADE -- Добавлено каскадное удаление
);

CREATE TABLE IF NOT EXISTS Gifts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    done INTEGER DEFAULT 0 -- INTEGER для BOOLEAN, 0 = нет, 1 = да
);

CREATE TABLE IF NOT EXISTS Tracks (
    id INTEGER PRIMARY KEY,
    name TEXT,
    author TEXT,
    number_of_calls INTEGER DEFAULT 0 -- Установлено значение по умолчанию
);

CREATE TABLE IF NOT EXISTS Block (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    start TEXT,
    block_duration TEXT, -- Переименовано для ясности
    FOREIGN KEY (user_id) REFERENCES Users(telegram_id) ON DELETE CASCADE -- Добавлено каскадное удаление
);

CREATE TABLE IF NOT EXISTS Meal (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price INTEGER
);

CREATE TABLE IF NOT EXISTS Likes (
    id INTEGER PRIMARY KEY,
    track_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (track_id) REFERENCES Tracks(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(telegram_id) ON DELETE CASCADE
);
