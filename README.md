# YBoterDR

## TODO

- [ ] commands:
    - [ ] start:
        - [ ] welcome message
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
    - [ ] arrived
        мы приехали 

- [ ] admin:
    - [ ] change track queue 
        изменить порядок треков в очереди
    - [ ] block user 
        заблокировать пользователя

- [ ] media messages:
    - [ ] photo
    - [ ] video
    - [ ] mugs

- [ ] database:
    - [ ] user
        telegram id: int
        name: str 
        date: datetime 
        number of tracks: int 
        number of media: int
        on the party: bool

    - [ ] media 
        id: int 
        user_id: user.telegram_id
        simlink: path

    - [ ] gifts
        id: int 
        name: str 
        done: bool 

    - [ ] tracks 
        id: int 
        name: str 
        author: str 
        number of calls: int

    - [ ] block
        id: int 
        user_id: user.telegram_id
        start: datetime 
        delta: time

    - [ ] meal
        id: int 
        name: str 
        price: int

## IDEAS

1. 

## LINKS

- [sqlitetutorial](https://www.sqlitetutorial.net)
- [yandex-music-api docs](https://yandex-music.readthedocs.io/en/main/index.html)

