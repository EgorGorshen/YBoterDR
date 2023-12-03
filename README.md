# YBoterDR

## TODO

- [ ] commands:
    - [ ] start:
        - [x] welcome message
        - [ ] open menu
    - [ ] add_track_queue
        добавлять трек в очередь [command] [track name]
    - [ ] like
        если пользователю понравилось то он может добавить трек в избранное
    - [ ] delete
        удолить помледний свой трек из очереди
    - [ ] find_track 
        поиск трека и по нахождении его отправить снипет
    - [ ] toast
        когда человек хочет сказать тост, музыка начинает затухать
    - [ ] choose_gift
        выбор подарка
    - [ ] next_tracks
        список следующих треков
    - [ ] we_left
        мы ушли показывает что человек ушёл или ещё здесь
    - [x] arrived
        мы приехали 

- [ ] admin:
    - [ ] change track queue 
        изменить порядок треков в очереди
    - [ ] block user 
        заблокировать пользователя
    - [x] info about user ariv and left 
        сообщать о подходе или уезеде пользователя

- [ ] media messages:
    - [ ] photo
    - [ ] video
    - [ ] mugs

```sql
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
```



## IDEAS

1. 

## LINKS

- [sqlitetutorial](https://www.sqlitetutorial.net)
- [yandex-music-api docs](https://yandex-music.readthedocs.io/en/main/index.html)
- [aiogram](https://docs.aiogram.dev/en/dev-3.x/)
- [test data mockaroo](https://www.mockaroo.com)
- [pytest-asyncio](https://tonybaloney.github.io/posts/async-test-patterns-for-pytest-and-unittest.html)
- [Faker](https://pypi.org/project/Faker/)
