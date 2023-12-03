# DATA BASE

## Users Table

> Purpose: Stores information about users.

Columns:
  - telegram_id: INTEGER, Primary Key. Unique identifier for each user.
  - name: TEXT. The name of the user.
  - number_of_tracks: INTEGER, Default 0. The number of tracks associated with the user.
  - number_of_media: INTEGER, Default 0. The number of media items associated with the user.
  - on_the_party: INTEGER, Default 0. Indicates whether the user is on the party (0 = no, 1 = yes).

## Media Table

> Purpose: Stores information about media items.

Columns:
  - id: INTEGER, Primary Key. Unique identifier for each media item.
  - user_id: INTEGER. Foreign key reference to Users(telegram_id).
  - simlink: TEXT. Symbolic link or reference to the media item.

## Gifts Table

> Purpose: Stores information about gifts.

Columns:
  - id: INTEGER, Primary Key. Unique identifier for each gift.
  - name: TEXT. Name of the gift.
  - done: INTEGER, Default 0. Indicates whether the gift is done (0 = no, 1 = yes).

## Tracks Table
> Purpose: Stores information about music tracks.

Columns:
  - id: INTEGER, Primary Key. Unique identifier for each track.
  - name: TEXT. Name of the track.
  - author: TEXT. Author of the track.
  - genre: TEXT. Genre of the track.
  - duration: INTEGER. Duration of the track.
  - explicit: INTEGER, Default 0. Indicates whether the track contains explicit content (0 = no, 1 = yes).
  - number_of_calls: INTEGER, Default 0. Number of times the track has been called.

## Block Table

> Purpose: Stores information about user blocks.

Columns:
  - id: INTEGER, Primary Key. Unique identifier for each block.
  - user_id: INTEGER. Foreign key reference to Users(telegram_id).
  - start: TEXT. Start time or date of the block.
  - block_duration: TEXT. Duration of the block.

## Meal Table

> Purpose: Stores information about meals.

Columns:
  - id: INTEGER, Primary Key. Unique identifier for each meal.
  - name: TEXT. Name of the meal.
  - description: TEXT. Description of the meal.
  - dietary_info: TEXT. Dietary information of the meal.
  - price: INTEGER. Price of the meal.

## Likes Table

> Purpose: Stores information about likes.

Columns:
  - id: INTEGER, Primary Key. Unique identifier for each like.
  - track_id: INTEGER. Foreign key reference to Tracks(id).
  - user_id: INTEGER. Foreign key reference to Users(telegram_id).

