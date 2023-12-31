from dataclasses import dataclass


@dataclass
class User:
    telegram_id: int
    name: str
    number_of_tracks: int = 0
    number_of_media: int = 0
    on_the_party: int = 0


@dataclass
class Media:
    id: int
    user_id: int
    simlink: str


@dataclass
class Gift:
    id: int
    name: str
    done: int = 0


@dataclass
class Track:
    track_id: int
    name: str
    author: str
    number_of_calls: int = 0

    def track_path(self) -> str:
        return ""


@dataclass
class Block:
    id: int
    user_id: int
    start: str
    block_duration: str


@dataclass
class Meal:
    id: int
    name: str
    price: int


@dataclass
class Like:
    id: int
    track_id: int
    user_id: int
